# Auto Test Guard

中文说明在前，English version below.

## 中文简介

`auto-test-guard` 是一个给 Codex 用的 skill，目标不是“AI 自动写一堆测试”，而是让 AI 在改完代码后，做更靠谱的稳定性收口。

它会推动 Codex 去判断：

- 这次改动到底值不值得补测试
- 应该补单测、集成测试，还是只跑现有命令
- 什么时候网页流程真的值得用 Playwright 跑一下
- 最后哪些地方已经验证过，哪些地方其实还没法证明

核心思路是：

`不是盲目加测试，而是做比例合适、真实执行、诚实汇报的验证。`

## 适合谁

这个 skill 特别适合：

- 刚开始让 AI 帮自己写代码的新手
- 希望每次改功能后都顺手做一轮自动验证的人
- 想把“写完代码再跑一下”这件事半自动化的人

## 它会教 Codex 做什么

1. 先判断改动风险，再决定要不要补测试。
2. 优先复用仓库已有测试体系，而不是重新发明一套。
3. 优先补最小但高价值的测试，不堆低信号用例。
4. 前端只在关键浏览器行为有风险时才使用 Playwright。
5. 测试必须真实运行，不能只生成文件就算完成。
6. 最后明确说明哪些地方已验证、哪些地方未验证、剩余风险多大。

更细的规则在 [references/validation-strategy.md](references/validation-strategy.md)。

## 安装

安装到本地 Codex skills 目录：

```bash
python install.py
```

安装到自定义 skills 目录：

```bash
python install.py --target /path/to/skills
```

覆盖已有安装：

```bash
python install.py --force
```

## 使用示例

```text
Use $auto-test-guard after this feature change. Add the smallest high-value validation, run the relevant tests, and tell me what is still unverified.
```

## 仓库结构

- `SKILL.md`: skill 主说明和触发描述
- `agents/openai.yaml`: UI 元数据
- `references/validation-strategy.md`: 更细的验证策略
- `prompt-guard.txt`: 最后的自检清单
- `install.py`: 本地安装脚本

## 可靠性边界

这个 skill 可以提升稳定性下限，但不能保证绝对正确：

- AI 可能会按自己的错误理解去写测试
- Playwright 这类浏览器测试会有 flaky 风险
- 有些改动离不开真实服务、密钥、数据或人工验收
- 测试通过只能说明“有证据支持”，不能说明“绝对没问题”

所以它更像一个稳定性护栏，而不是正确性保证器。

---

## English

`auto-test-guard` is a Codex skill that improves the validation pass after code changes.

It is not designed to blindly generate tests for every edit. Instead, it teaches Codex to decide:

- whether the change deserves new automated coverage
- which existing test command should be reused
- when a focused unit or integration test is enough
- when a small Playwright flow is justified
- how to report remaining risk honestly

The core idea is:

`Use proportional validation, run it for real, and describe confidence honestly.`

## What it teaches Codex to do

1. Inspect the change before deciding whether tests are needed.
2. Reuse the repository's existing validation stack first.
3. Prefer focused, high-signal coverage over broad speculative suites.
4. Use Playwright only when browser behavior is part of the real risk.
5. Run verification commands for real instead of stopping at file generation.
6. Report what was validated, what was skipped, and what risk remains.

## Install

Install into the default Codex skills directory:

```bash
python install.py
```

Install into a custom skills directory:

```bash
python install.py --target /path/to/skills
```

Overwrite an existing installation:

```bash
python install.py --force
```

## Example prompt

```text
Use $auto-test-guard after this feature change. Add the smallest high-value validation, run the relevant tests, and tell me what is still unverified.
```

## Reliability boundaries

This skill improves the odds of catching regressions, but it still has limits:

- AI can write tests that mirror its own mistaken assumptions.
- Browser automation can be flaky.
- Some changes cannot be validated without real services, secrets, or human review.
- Green tests are evidence, not proof.

That is why the skill is opinionated about honest reporting and proportional validation.
