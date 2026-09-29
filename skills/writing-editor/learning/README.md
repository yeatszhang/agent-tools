# Learning Loop

## Capture

```bash
python scripts/capture_edit.py \
  --original /path/to/original.md \
  --final /path/to/final.md \
  --context technical
```

脚本会写入：

```text
observations/YYYYMMDD-HHMMSS/
├── meta.json
├── original.md
├── final.md
└── diff.patch
```

## Learn

Agent 阅读多个 observations 后，只输出候选规则。

不要自动修改 `references/voice.md`。

推荐升级过程：

```text
1 observation  -> candidate
3+ similar     -> emerging
5+ + eval      -> stable
```

阈值只是默认值；规则影响越大，越应提高证据要求。
