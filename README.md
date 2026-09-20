# 职业战略教练

一个面向职业路径分析、转岗与跳槽决策、职业规划和定期复盘的 Codex 项目级 Skill。它以证据为基础区分事实、推断和未知，帮助用户诊断职业阶段与资产、比较可行路线，并把结论转化为可验证的行动计划。

## 核心能力

- 分析职业阶段、当前约束和关键决策，而不是按年龄或职级套用固定结论。
- 盘点方向、能力、成果、杠杆、资源和自由六类职业资产。
- 比较多条职业路线的收益、成本、风险、可逆性和验证方式。
- 生成职业策略、90 天行动计划、决策记录和周期性复盘。
- 在用户确认后创建独立的 Markdown 职业档案，不把个人信息写入 Skill。

## 快速开始

克隆并在 Codex 中打开本仓库：

```powershell
git clone https://github.com/a3125837/career-strategy-coach.git
cd career-strategy-coach
```

然后可以直接使用自然语言：

```text
帮我分析一下职业路径
```

也可以使用项目级文本别名：

```text
/ZhiYeJiaoLian
/ZhiYeJiaoLian 帮我比较继续做产品经理和转向 AI 产品经理两条路线
```

> `/ZhiYeJiaoLian` 是本仓库通过 `AGENTS.md` 定义的项目级文本别名，不是 Codex 原生自定义斜杠命令。只输入别名时，教练会先询问本次想解决的职业问题；别名后有文本时，该文本会作为本次问题。

自然语言中的职业规划、职业发展、跳槽、转岗、转型、路线比较和职业复盘等意图，也会触发 `.agents/skills/career-strategy-coach/SKILL.md`。

## 创建个人职业档案

当前项目配置的默认档案根目录是：

```text
F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles
```

用户也可以明确指定其他绝对路径。默认路径只是提案，不代表写入授权。创建流程固定为：

1. 用户提供一个单层文件夹名称；可以使用中性化名，不必包含姓名或邮箱。
2. 教练运行只读 `propose`，校验名称并展示目标绝对路径。
3. `propose` 展示且只展示以下五项内容：
   - `career-profile.md`
   - `career-strategy.md`
   - `plans/`
   - `reviews/`
   - `decisions/`
4. 用户明确确认后，教练才运行 `init` 创建档案。
5. 创建完成后运行 `validate` 校验结构。

文件夹名称去除首尾空白后不能为空，不能包含路径分隔符、Windows 非法文件名字符、控制字符或保留设备名，也不能是 `.`、`..` 或以点、空白结尾的名称。

## 命令行工具

以下命令从 Skill 根目录运行：

```powershell
cd .agents\skills\career-strategy-coach
```

只读提案，不创建目录或文件：

```powershell
py -3.11 scripts\career_workspace.py propose `
  --root "F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles" `
  --name "职业档案-A"
```

用户明确确认后初始化档案：

```powershell
py -3.11 scripts\career_workspace.py init `
  --path "F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\职业档案-A"
```

校验已有档案：

```powershell
py -3.11 scripts\career_workspace.py validate `
  --path "F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\职业档案-A"
```

脚本要求绝对路径，并拒绝与 Skill 目录重叠的目标、路径逃逸以及路径链中的符号链接或重解析点。

## 目录结构

```text
.
├── .agents/skills/career-strategy-coach/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/workspace-template/
│   │   ├── career-profile.md
│   │   └── career-strategy.md
│   └── scripts/career_workspace.py
├── docs/superpowers/
│   ├── plans/
│   └── specs/
├── tests/
│   ├── behavior/
│   ├── test_career_workspace.py
│   └── test_skill_discovery.py
├── AGENTS.md
└── README.md
```

- `.agents/skills/career-strategy-coach/`：仓库内的权威 Skill 源。
- `AGENTS.md`：项目调用规则、存储位置和隐私约束。
- `tests/`：工作区脚本、Skill 发现规则和行为证据测试。
- `docs/superpowers/`：设计说明与实施计划。

## 隐私与存储

- Skill 本身不保存个人信息、职业数据或最近使用路径。
- 个人职业信息只保存在用户明确确认的独立职业档案目录。
- `career-profiles/` 已加入 `.gitignore`，不会作为仓库内容提交。
- 创建或更新档案前必须展示绝对路径和拟写入内容，并取得明确确认。
- Skill 不会主动把职业档案同步到云端或外部服务。

## 验证状态

在 Windows 环境使用 Python 3.11 验证：

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
py -3.11 -m unittest discover -s tests -p 'test_*.py'
py -3.11 C:\Users\45458\.codex\skills\.system\skill-creator\scripts\quick_validate.py `
  .agents\skills\career-strategy-coach
```

当前结果：

- 共运行 33 项测试：29 项通过，4 项因当前 Windows 环境不允许创建测试所需的符号链接而跳过，0 项失败。
- 仓库 Skill 和 F 盘安装副本均通过官方 `quick_validate.py` 校验。
- 跳过的测试用于真实符号链接场景；不依赖符号链接权限的路径链安全测试仍会执行。

## 许可证

本仓库目前没有 `LICENSE` 文件，因此没有声明开源许可证。复制、修改、分发或再许可前，请先取得仓库所有者授权。

