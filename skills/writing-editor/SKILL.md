---
name: writing-editor
description: 按请求润色或去模板化中文技术文档、管理沟通、消息和长文，保留原意并匹配个人 Voice；用户明确要求学习修改时提炼候选偏好。普通技术问答、代码注释和仅校对错字不默认触发完整改写。
---

# Writing Editor

仓库共享约束见 [AGENTS.md](../../AGENTS.md)。

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
4. 保留原判断及不确定程度，不把“可能”“初步”改成确定结论
5. Match personal voice
6. Improve rhythm and readability

## Learning

用户提供人工修改，可以用于当前文本的调整；只有明确要求记录或学习偏好时，才进入持久化学习：

1. 提取与表达风格有关的修改，区分事实修正和偏好；一次业务事实纠正不是写作规则。
2. 如需保存证据，先脱敏，并按[记录流程](learning/README.md)指定输出目录；不自动把全文写入 Skill 源码目录。
3. 只提出 candidate rules，不直接修改 stable voice。同一处修改的重复保存只算一次观察。
4. 按[规则记录](learning/rules.yaml)中的阈值检查独立观察；次数仅是必要证据之一，不触发自动晋级。
5. 经人工 review 与[评测案例](evals/README.md)验证后，才更新稳定 Voice。

没有学习请求时，完成当前改写即可，不建立用户文本档案。
