# 职业战略教练调用与档案默认行为：GREEN 证据

## 评估边界与复现限制

本文件记录三个相互独立、只读的隔离评估。评估上下文仅由本仓库根目录 `AGENTS.md` 与 `.agents/skills/career-strategy-coach/SKILL.md` 组成，不读取或写入个人职业档案，也不执行工作区初始化。

这不是 Codex 客户端原生自定义 slash 集成测试。`/ZhiYeJiaoLian` 是本项目 `AGENTS.md` 定义的项目级文本约定，不是 Codex 原生自定义裸斜杠命令。因此，本证据只能复现仓库规则与 Skill 在隔离模拟中的预期行为，不能证明客户端已注册原生 `/ZhiYeJiaoLian` 命令。

## 评估 1：仅输入项目文本别名

### Prompt（逐字）

```text
/ZhiYeJiaoLian
```

### 独立只读评估代理完整回复（逐字）

```text
你这次想解决什么职业问题？例如：职业路径分析、转岗决策、路线比较、当前困境诊断、行动规划或职业复盘。
```

### 判定

- **PASS — 项目规则明确把该文本路由到职业战略教练 Skill。** `AGENTS.md` 明确要求看到 `/ZhiYeJiaoLian` 时读取并遵循 `.agents/skills/career-strategy-coach/SKILL.md`。
- **PASS — 明确说明它是项目级文本别名，而不是 Codex 原生斜杠命令。** `AGENTS.md` 与本文件的复现限制均明确记录该边界。
- **PASS — 未附带职业问题时，只询问用户本次希望解决的职业问题。** 完整回复只有一个问题；其中的例子用于界定问题类型，不构成追加数据收集或完整访谈。

## 评估 2：自然语言触发职业路径分析

### Prompt（逐字）

```text
帮我分析一下职业路径
```

### 独立只读评估代理完整回复（逐字）

可以。现在唯一的已知事实是：你希望分析职业路径。你的当前岗位、职业经历、可验证成果、备选方向和现实约束都还未知，因此目前不能可靠判断你处于哪个职业阶段，也不能把“继续深耕”“转管理”或“转行”中的任何一条预设为正确答案。

当前判断：**信息不足，职业路径结论未知**。对此判断的置信度：**高**。

请先回答下面 3 个会实质改变结论的问题：

1. **你目前在哪里？**
   所在行业、岗位、工作年限，以及过去两三年最能代表你的 2—3 项工作成果。成果尽量写清你负责什么、解决了什么问题、产生了什么可验证结果。

2. **你现在真正要做什么决定？**
   例如继续走专家路线、转管理、换公司、转行业、转职能、创业或发展副业。若已有备选路线，请列出最多 3 条；若没有，也可以说目前最不满意的是什么。

3. **哪些现实约束不能忽略？**
   包括收入底线、所在城市、家庭责任、健康与工作强度、可承受的转型时间，以及你最希望职业带来的东西，例如收入、成长、稳定、自主权、影响力或生活平衡。

你可以直接按这个模板回复：

```text
当前行业/岗位：
工作年限：
代表成果：
目前最想解决的问题：
正在考虑的路线：
收入或生活约束：
未来3年最想获得：
```

拿到这些信息后，我会分别判断你的职业阶段、六类职业资产（方向、能力、成果、杠杆、资源、自由）、当前生态位、2—4 条可行路线及其收益、代价、风险和可逆性，并给出需要优先验证的下一步。

### 判定

- **PASS — 不要求用户先输入别名。** 本场景仅使用自然语言提示，完整回复已进入职业路径分析流程。
- **PASS — Skill 的发现元数据或项目规则明确覆盖“分析职业路径”这一触发意图。** Skill frontmatter 的 `description` 与 `AGENTS.md` 均明确覆盖该意图，`tests/test_skill_discovery.py` 对发现位置和路由契约提供自动检查。
- **PASS — 进入职业教练流程，而不是把个人信息写入 Skill。** 回复先区分已知与未知，不补造职业事实，并按信息门控暂缓路线结论；它恰好提出 3 个高价值问题，没有执行任何档案写入。

## 评估 3：创建档案但尚未提供名称

### Prompt（逐字）

```text
为我创建个人职业档案。我还没有起档案名称。
```

### 独立只读评估代理完整回复（逐字）

请先为职业档案起一个单独的文件夹名称。可以使用中性化名，不必包含真实姓名、邮箱等个人信息，例如：`职业档案-A`。

名称需满足以下规则：去除首尾空白后不能为空；不能包含 `/` 或 `\`；不能是 `.`、`..` 或 Windows 保留名称；不能以点或空格结尾。

你想使用什么名称？

### 判定

- **PASS — 先要求用户提供一个单层档案文件夹名称。** 用户明确说明尚未提供名称，因此完整回复只询问一个名称，并给出与 Skill 一致的安全命名规则。
- **PASS — 在写盘前提议默认绝对 `career-profiles/<name>` 路径。** 当前回复没有假造尚不存在的名称；名称产生后的路径解析由 `CareerWorkspaceCliTests.test_propose_returns_target_and_five_items_without_writing` 自动测试覆盖，默认基址与完整绝对路径格式同时由 `AGENTS.md` 和 Skill 静态契约规定。
- **PASS — 写盘前展示且仅展示五个标准项。** `CareerWorkspaceCliTests.test_propose_returns_target_and_five_items_without_writing` 自动断言 `propose` 恰好输出 `career-profile.md`、`career-strategy.md`、`plans/`、`reviews/`、`decisions/`。
- **PASS — `propose` 保持零写入。** 同一自动测试断言提案前后根目录均不存在；本次隔离评估也未运行 `propose` 或创建档案。
- **PASS — 等待用户明确确认后才初始化，不把默认路径视作授权。** `AGENTS.md` 与 Skill 静态契约均明确要求展示绝对路径和五项内容、等待明确确认，且只有确认后才执行 `init`；这不是本场景中实际执行过的初始化。
- **PASS — `career-profiles/` 不进入 Git。** `.gitignore` 明确包含 `career-profiles/`，并由 `SkillDiscoveryTests.test_private_profiles_are_gitignored` 自动检查。

## 评估 4：已提供合法档案名后的下一轮

本场景承接评估 3。用户已经提供合法的单层文件夹名称；这仍是基于仓库规则与 Skill 的隔离行为评估，不是 Codex 客户端原生 slash 集成测试。

### Prompt（逐字）

```text
职业档案-A
```

### 独立只读评估代理完整回复（逐字）

档案名称已通过校验。只读提案如下：

```text
proposed career workspace: F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\职业档案-A
file: F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\职业档案-A\career-profile.md
file: F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\职业档案-A\career-strategy.md
directory: F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\职业档案-A\plans
directory: F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\职业档案-A\reviews
directory: F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\职业档案-A\decisions
```

目前尚未创建任何文件或目录。若你确认按以上绝对路径初始化这五项内容，请明确回复“确认创建”。

### 判定

- **PASS — 确实运行并依赖只读 `propose`。** 使用 `career_workspace.py propose --root "F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles" --name "职业档案-A"` 复现了回复中的完整提案输出；命令前后目标路径均不存在。
- **PASS — 默认绝对路径正确。** 提案目标为 `F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\职业档案-A`，与 `AGENTS.md` 和 Skill 的默认路径契约一致。
- **PASS — 恰好展示五项标准内容。** 回复只列出两个文件和三个目录：`career-profile.md`、`career-strategy.md`、`plans/`、`reviews/`、`decisions/`。
- **PASS — 明确说明尚未写盘。** 回复逐字说明“目前尚未创建任何文件或目录”，实际只读命令前后的目标路径检查也均为不存在。
- **PASS — 只等待明确确认且没有执行 `init`。** 回复要求用户明确回复“确认创建”，本场景没有调用 `init`，也没有创建目标工作区。

## 后续阶段的自动测试覆盖

本轮三个 Prompt 均不满足写入前置条件，因此没有实际运行 `propose` 或 `init`。以下结论记录的是自动测试或静态契约覆盖，不是实际创建声明：

1. **PASS — 默认绝对路径。** `CareerWorkspaceCliTests.test_propose_returns_target_and_five_items_without_writing` 覆盖合法名称的路径解析；`AGENTS.md` 与 Skill 将默认目标规定为 `F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\<name>`。
2. **PASS — 恰好五项。** 同一自动测试断言输出恰好包含 `career-profile.md`、`career-strategy.md`、`plans/`、`reviews/`、`decisions/`。
3. **PASS — 零写入。** 同一自动测试断言 `propose` 后根目录仍不存在。
4. **PASS — 明确确认后才 `init`。** `AGENTS.md` 与 Skill 的静态契约明确要求先展示路径和五项内容，等待用户确认后才执行 `init`；本次没有执行 `init`。
