---
name: writing-editor
description: 润色中文文本，降低模板化 AI 写作痕迹，并逐步匹配用户个人 Voice。适用于技术文档、管理沟通、日常消息和长文。
---

# Writing Editor

## Goal

把文本从“通用 AI 写作”编辑成自然、具体、有判断、符合个人表达习惯的成稿。

目标不是欺骗 AI Detector，也不要为了“像人”而故意制造错别字、虚构经历或加入无关情绪。

## Workflow

1. 判断场景：`technical` / `management` / `casual` / `longform`。
2. 阅读 `references/humanizer-zh.md`。
3. 阅读 `references/voice.md`。
4. 阅读 `references/scenarios.md` 中对应场景。
5. 必要时读取 `examples/` 中的相关样例。
6. Pass 1：Humanize。
7. Pass 2：Voice Match。
8. 自检：
   - 是否保持事实、数据和原始立场？
   - 是否删除了空话而没有删除有效信息？
   - 是否保留了作者的判断和取舍？
   - 是否出现为了“自然”而虚构的内容？

## Editing Priorities

优先级从高到低：

1. Preserve facts and intent
2. Remove empty / generic language
3. Make claims concrete
4. Preserve or strengthen explicit judgement
5. Match personal voice
6. Improve rhythm and readability

## Learning

当用户对输出进行了人工修改：

1. 保存 original 和 final。
2. 生成 diff。
3. 只提出 candidate rules，不直接修改 stable voice。
4. 同类修改多次出现后，提升为 emerging。
5. 经人工 review / eval 后再写入 stable voice。

规则生命周期见 `learning/rules.yaml`。
