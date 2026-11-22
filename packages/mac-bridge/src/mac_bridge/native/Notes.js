// osascript 从标准输入接收 JSON；调用者的文字只作为数据传给 Notes。
ObjC.import("Foundation");

function escapeHTML(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;")
        .replace(/>/g, "&gt;").replace(/\r\n?|\n/g, "<br>");
}

function run() {
    const data = $.NSFileHandle.fileHandleWithStandardInput.readDataToEndOfFile;
    const request = JSON.parse(ObjC.unwrap($.NSString.alloc.initWithDataEncoding(data, $.NSUTF8StringEncoding)));
    const notes = Application("com.apple.Notes");
    switch (request.operation) {
    case "notes_search": {
        const matches = request.query
            ? notes.notes.whose({name: {_contains: request.query}})()
            : notes.notes();
        return JSON.stringify({notes: matches.slice(request.offset, request.offset + request.limit).map(
            note => ({id: note.id(), title: note.name()})
        ), next_offset: matches.length > request.offset + request.limit ? request.offset + request.limit : null});
    }
    case "notes_read": {
        const note = notes.notes.byId(request.id);
        if (!note.exists()) throw Error("找不到该备忘录");
        if (note.passwordProtected()) throw Error("备忘录已加锁");
        const body = Array.from(note.plaintext());
        return JSON.stringify({id: note.id(), title: note.name(),
            text: body.slice(request.offset, request.offset + request.limit).join(""),
            next_offset: request.offset + request.limit < body.length ? request.offset + request.limit : null});
    }
    case "notes_create": {
        const folder = notes.defaultAccount().defaultFolder();
        const note = notes.Note({body: "<div><b>" + escapeHTML(request.title) +
            "</b></div><div>" + escapeHTML(request.body) + "</div>"});
        folder.notes.push(note);
        return JSON.stringify({id: note.id(), title: note.name()});
    }
    default:
        throw Error("未知的备忘录操作");
    }
}
