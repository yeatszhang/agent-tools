# Learning Loop

## Capture

仅在用户明确要求记录学习样例时执行。输入先脱敏，输出目录显式指定；真实样例存放在仓库外，脚本不执行脱敏或自动学习。下面从本仓库根目录运行，替换示例路径：

```bash
python3 skills/writing-editor/scripts/capture_edit.py \
  --original /path/to/original.md \
  --final /path/to/final.md \
  --context technical \
  --output-dir /path/outside-repo/writing-observations
```

脚本会写入：

```text
<output-dir>/YYYYMMDD-HHMMSS-<unique>/
├── meta.json
├── original.md
├── final.md
└── diff.patch
```

## Learn

Agent 阅读多个 observations 后，只输出候选规则。

不要自动修改 `references/voice.md`。

规则阈值统一维护在 [rules.yaml](rules.yaml)，不要在其他文件另存一组数字。推荐升级过程：

```text
独立观察 → candidate → 足够的同类证据 → emerging → 人工评审与评测 → stable
```

阈值只是默认值；规则影响越大，越应提高证据要求。

重复保存同一对输入不算新增观察；事实、日期或数字纠正不应转化为表达偏好。仓库中的 `examples/` 只保留适合共享且已脱敏的精选样例。
