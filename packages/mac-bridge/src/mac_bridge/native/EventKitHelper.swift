import EventKit
import Foundation

struct Request: Decodable {
    let operation: String
    let kind: String?
    let id: String?
    let calendar_id: String?
    let title: String?
    let start: Date?
    let end: Date?
    let due: Date?
    let query: String?
    let offset: Int?
    let limit: Int?
}

struct BridgeError: LocalizedError {
    let message: String
    init(_ message: String) { self.message = message }
    var errorDescription: String? { message }
}

func require<T>(_ value: T?, _ message: String) throws -> T {
    guard let value else { throw BridgeError(message) }
    return value
}

func accessStatus(_ type: EKEntityType) -> String {
    switch EKEventStore.authorizationStatus(for: type) {
    case .notDetermined: return "notDetermined"
    case .restricted: return "restricted"
    case .denied: return "denied"
    case .fullAccess: return "fullAccess"
    case .writeOnly: return "writeOnly"
    @unknown default: return "unknown"
    }
}

func destination(_ request: Request, _ store: EKEventStore, _ type: EKEntityType) throws -> EKCalendar {
    let calendar: EKCalendar?
    if let id = request.calendar_id {
        calendar = store.calendars(for: type).first { $0.calendarIdentifier == id }
    } else {
        calendar = type == .event ? store.defaultCalendarForNewEvents : store.defaultCalendarForNewReminders()
    }
    let result = try require(calendar, "找不到目标日历或提醒清单")
    guard result.allowsContentModifications else { throw BridgeError("目标只读") }
    return result
}

func execute(_ request: Request) async throws -> [String: Any] {
    if request.operation == "status" {
        return ["events": accessStatus(.event), "reminders": accessStatus(.reminder)]
    }
    let store = EKEventStore()
    let isEvent = request.operation.hasPrefix("events_") || request.kind == "events"
    let granted = isEvent ? try await store.requestFullAccessToEvents() : try await store.requestFullAccessToReminders()
    guard granted else { throw BridgeError("请在系统设置的隐私与安全性中允许访问相应应用") }

    let formatter = ISO8601DateFormatter()
    switch request.operation {
    case "containers":
        let calendars = store.calendars(for: isEvent ? .event : .reminder)
        return ["items": calendars.map { ["id": $0.calendarIdentifier, "title": $0.title,
                                           "account": $0.source.title, "writable": $0.allowsContentModifications] }]
    case "events_list":
        let predicate = store.predicateForEvents(withStart: try require(request.start, "缺少开始时间"),
                                                  end: try require(request.end, "缺少结束时间"), calendars: nil)
        let events = store.events(matching: predicate).sorted {
            ($0.startDate!, $0.calendarItemIdentifier) < ($1.startDate!, $1.calendarItemIdentifier)
        }
        let limit = try require(request.limit, "缺少返回数量")
        let offset = request.offset ?? 0
        return ["items": events.dropFirst(offset).prefix(limit).map { ["id": $0.calendarItemIdentifier, "title": $0.title ?? "",
                    "calendar_id": $0.calendar.calendarIdentifier, "all_day": $0.isAllDay,
                    "start": formatter.string(from: $0.startDate), "end": formatter.string(from: $0.endDate)] },
                "truncated": events.count > offset + limit]
    case "events_create":
        let event = EKEvent(eventStore: store)
        event.calendar = try destination(request, store, .event)
        event.title = try require(request.title, "缺少标题")
        event.startDate = try require(request.start, "缺少开始时间")
        event.endDate = try require(request.end, "缺少结束时间")
        try store.save(event, span: .thisEvent)
        return ["id": event.calendarItemIdentifier, "title": event.title ?? ""]
    case "reminders_list":
        let predicate = store.predicateForIncompleteReminders(withDueDateStarting: nil, ending: nil, calendars: nil)
        let items: [EKReminder]? = await withCheckedContinuation { continuation in
            _ = store.fetchReminders(matching: predicate) { continuation.resume(returning: $0) }
        }
        let query = request.query ?? ""
        let reminders = try require(items, "读取提醒事项失败")
            .filter { query.isEmpty || ($0.title ?? "").localizedCaseInsensitiveContains(query) }
            .sorted { ($0.title ?? "", $0.calendarItemIdentifier) < ($1.title ?? "", $1.calendarItemIdentifier) }
        let limit = try require(request.limit, "缺少返回数量")
        let offset = request.offset ?? 0
        return ["items": reminders.dropFirst(offset).prefix(limit).map { reminder -> [String: Any] in
            var item: [String: Any] = ["id": reminder.calendarItemIdentifier, "title": reminder.title ?? "",
                                       "calendar_id": reminder.calendar.calendarIdentifier]
            if let parts = reminder.dueDateComponents {
                var calendar = parts.calendar ?? Calendar.current
                if let zone = parts.timeZone { calendar.timeZone = zone }
                if let date = calendar.date(from: parts) { item["due"] = formatter.string(from: date) }
            }
            return item
        }, "truncated": reminders.count > offset + limit]
    case "reminders_create":
        let reminder = EKReminder(eventStore: store)
        reminder.calendar = try destination(request, store, .reminder)
        reminder.title = try require(request.title, "缺少标题")
        if let due = request.due {
            reminder.dueDateComponents = Calendar.current.dateComponents(
                [.calendar, .timeZone, .year, .month, .day, .hour, .minute, .second], from: due)
        }
        try store.save(reminder, commit: true)
        return ["id": reminder.calendarItemIdentifier, "title": reminder.title ?? ""]
    case "reminders_complete":
        let id = try require(request.id, "缺少提醒事项 ID")
        let reminder = try require(store.calendarItem(withIdentifier: id) as? EKReminder, "找不到该提醒事项")
        if !reminder.isCompleted {
            reminder.isCompleted = true
            try store.save(reminder, commit: true)
        }
        return ["id": id, "completed": true]
    default:
        throw BridgeError("未知的 EventKit 操作")
    }
}

@main struct Helper {
    static func main() async {
        do {
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            let request = try decoder.decode(Request.self, from: FileHandle.standardInput.readDataToEndOfFile())
            let result = try await execute(request)
            FileHandle.standardOutput.write(try JSONSerialization.data(withJSONObject: result))
        } catch {
            FileHandle.standardError.write(Data(error.localizedDescription.utf8))
            exit(1)
        }
    }
}
