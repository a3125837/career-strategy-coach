# 职业战略教练快捷调用与默认档案目录设计

日期：2026-09-19

## 目标

在不向 C 盘写入任何内容的前提下，让职业战略教练在项目任务中更容易被发现和调用，并为新建个人职业档案提供安全、明确的 F 盘默认位置。

## 产品约束

- Codex 的标准 Skill 显式调用保持为 `$career-strategy-coach`。
- Codex 不支持注册任意裸自定义斜杠命令；官方自定义 Prompt 形式是 `/prompts:<name>`。
- 本项目把 `/ZhiYeJiaoLian` 作为项目级文本触发别名，而不把它表述为系统原生斜杠命令。
- 不改变 `CODEX_HOME`，不在 C 盘安装 Prompt、Skill、插件、缓存或配置。
- Skill 本身不保存个人资料、用户选择的档案名称或最近使用路径。

## 方案

### 1. 项目级 Skill 发现

将 Skill 的权威源码从项目根目录下的 `career-strategy-coach/` 移至 Codex 官方支持的仓库级位置：

```text
.agents/skills/career-strategy-coach/
```

F 盘安装副本继续保留在：

```text
F:\AIPro\Codex\skills\career-strategy-coach
```

项目源码是唯一权威源。每次修改后，只有在确认安装副本未被用户修改时才能同步，并在同步后比较完整相对路径集合与 SHA-256。

### 2. 快捷触发

项目根目录 `AGENTS.md` 增加以下路由规则：

- 用户输入 `/ZhiYeJiaoLian` 时，加载并使用 `.agents/skills/career-strategy-coach/SKILL.md`。
- `/ZhiYeJiaoLian` 后面的文本视为本轮职业问题；只有命令本身时，进入职业教练入口并询问用户本次要解决的问题。
- 该别名仅是项目级文本约定，不冒充 Codex 原生命令。

Skill 的 `description` 增加清晰的自然语言触发条件，包括：分析职业路径、职业发展、职业规划、跳槽或转型决策、职业路线比较、职业复盘。`agents/openai.yaml` 保持允许默认的隐式调用，并更新默认提示以兼容快捷入口。

### 3. 默认个人档案目录

新建档案时，默认基础目录固定为项目根目录下的：

```text
career-profiles/
```

用户必须提供一个单层文件夹名称。最终路径为：

```text
F:\AIPro\Career Strategy Coach  职业战略教练\career-profiles\<用户起的名字>
```

名称规则：

- 去除首尾空白后不能为空；
- 必须是单层名称，不允许 `/` 或 `\`；
- 不允许 `.`、`..` 或 Windows 保留设备名；
- 不把姓名、邮箱或其他个人身份信息强制作为名称；用户可以使用中性代号。

`career-profiles/` 必须加入 `.gitignore`，职业档案不得进入版本控制。

### 4. 写入确认闸门

默认路径不等于默认授权。创建前仍必须：

1. 询问用户档案文件夹名称；
2. 解析并展示最终绝对路径；
3. 展示将创建的五项：`career-profile.md`、`career-strategy.md`、`plans/`、`reviews/`、`decisions/`；
4. 等待用户明确确认；
5. 确认后才执行初始化。

若用户主动提供其他绝对路径，则尊重该路径，不强制使用默认根目录。更新已有档案时仍按用户指定工作区和章节执行。

### 5. 确定性脚本接口

在现有 `career_workspace.py` 中增加根据根目录与名称构造目标路径的能力，避免模型手工拼接产生目录穿越或多层路径。建议接口：

```powershell
python scripts/career_workspace.py propose --root <absolute-root> --name <single-folder-name>
```

该命令只输出解析后的目标路径和标准五项清单，不创建文件。实际写入仍使用：

```powershell
python scripts/career_workspace.py init --path <absolute-target>
python scripts/career_workspace.py validate --path <absolute-target>
```

### 6. 测试与验收

- RED：验证当前 `/ZhiYeJiaoLian` 与“帮我分析一下职业路径”没有明确的项目级路由；验证当前 helper 没有安全的名称提议接口。
- GREEN：快捷别名与自然语言均路由到该 Skill。
- `propose` 接受中文、英文、数字和常规空格名称，输出项目根目录下的规范绝对路径及五项清单，且不创建任何文件。
- `propose` 拒绝空名称、路径分隔符、`.`、`..`、Windows 保留设备名及会逃逸默认根目录的输入。
- 新建档案仍需明确确认；未经确认不得运行 `init`。
- 全部单元测试、官方 Skill validator、行为场景、隐私扫描通过。
- 权威源码与 F 盘安装副本的文件集合及 SHA-256 完全一致。

## 非目标

- 不向 C 盘创建全局 Prompt 或全局 Skill。
- 不修改 `CODEX_HOME`。
- 不创建插件。
- 不把 `/ZhiYeJiaoLian` 声称为 Codex 原生自定义命令。
- 不自动创建个人档案，也不保存最近一次档案路径。
