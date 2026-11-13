# Harness 组件库

[文档导航](README.md) · [完整源码](../vendor/claude-code-harness-study/)

Harness 是模型外侧的运行机制：执行工具、控制权限、保存状态、组织上下文，并判断任务何时结束。本模块提供可分别查看和运行的实现，不要求把所有机制同时装进一个产品。

## 组件索引

| 目录 | 能力 | 实现关注点 |
|---|---|---|
| [s01_agent_loop](../vendor/claude-code-harness-study/s01_agent_loop/) | 模型与工具循环 | 消息历史、调用工具、返回执行结果 |
| [s02_tool_use](../vendor/claude-code-harness-study/s02_tool_use/) | 工具分发 | 工具定义与执行函数映射 |
| [s03_permission](../vendor/claude-code-harness-study/s03_permission/) | 权限控制 | 判断允许、拒绝或需要确认 |
| [s04_hooks](../vendor/claude-code-harness-study/s04_hooks/) | 钩子 | 工具执行前后的扩展点 |
| [s05_todo_write](../vendor/claude-code-harness-study/s05_todo_write/) | 待办 | 明确步骤并记录完成情况 |
| [s06_subagent](../vendor/claude-code-harness-study/s06_subagent/) | 子 Agent | 独立消息上下文、结果返回 |
| [s07_skill_loading](../vendor/claude-code-harness-study/s07_skill_loading/) | 技能加载 | 先加载索引，再按需读取内容 |
| [s08_context_compact](../vendor/claude-code-harness-study/s08_context_compact/) | 上下文压缩 | 预算、工具结果整理与历史摘要 |
| [s09_memory](../vendor/claude-code-harness-study/s09_memory/) | 记忆 | 筛选、提取、整理 |
| [s10_task_system](../vendor/claude-code-harness-study/s10_task_system/) | 任务系统 | 依赖图与文件持久化 |
| [s11_background_tasks](../vendor/claude-code-harness-study/s11_background_tasks/) | 后台任务 | 慢操作执行与完成通知 |
| [s12_cron_scheduler](../vendor/claude-code-harness-study/s12_cron_scheduler/) | 定时调度 | 定时触发与调度状态 |
| [s13_agent_teams](../vendor/claude-code-harness-study/s13_agent_teams/) | Agent 团队 | 任务认领、消息与工作目录 |
| [s14_mcp_plugin](../vendor/claude-code-harness-study/s14_mcp_plugin/) | MCP | 工具发现与工具池扩展 |
| [s15_integrated_harness](../vendor/claude-code-harness-study/s15_integrated_harness/) | 集成 Harness | 将多种机制放进同一运行系统 |
| [s16_workflow_runtime](../vendor/claude-code-harness-study/s16_workflow_runtime/) | 工作流 | 固定编排、生命周期事件与 journal 续跑 |
| [s17_goal_loop](../vendor/claude-code-harness-study/s17_goal_loop/) | 目标循环 | 完成判断、续轮和停止边界 |

## 启动

在仓库根目录运行：

```bash
python3 leo.py learn web
```

本地服务提供说明、代码对比、机制回放和运行入口。只浏览不需要模型 Key；在网页执行代码则需要对应环境和模型配置。

直接运行组件：

```bash
python3 leo.py learn s01
python3 leo.py learn s03
```

组件运行器可能创建自己的虚拟环境、安装依赖并提示配置模型。配置模板位于 [`.env.example`](../vendor/claude-code-harness-study/.env.example)。模型运行会调用工具，Bash 工具拥有当前进程的系统权限，不能把示例当作完整沙箱。

不带参数的 `python3 leo.py learn` 只打印本地文件地址；浏览器通过 `file://` 打开时可能限制资源读取，优先使用 `learn web`。

## 依赖关系

- s01 → s02 → s03 → s04 逐步扩展基础循环。
- s05–s12、s14 分别基于 s04；彼此不会自动合并。
- s13 基于 s10 的任务系统。
- s15 组合前述机制，并加入错误恢复；s16 在 s15 上增加工作流。
- s17 是基于 s04 的独立目标判断实现。

因此，查看记忆机制可直接进入 s09；需要同时运行记忆、任务和工具时应检查 s15 的集成实现。

## 文件入口

| 位置 | 内容 |
|---|---|
| 各组件的 `code.py` | 具体执行逻辑 |
| 各组件的 `README.md`、`images/` | 机制说明与图示 |
| [guide/](../vendor/claude-code-harness-study/guide/) | 组件选型、概念与案例 |
| [skills/](../vendor/claude-code-harness-study/skills/) | 按需加载的技能文件 |
| [web/](../vendor/claude-code-harness-study/web/) | 本地界面、回放与执行事件支持 |
| [tests/](../vendor/claude-code-harness-study/tests/) | 组件相关测试 |

工坊会根据需求决定组件取舍。组件库提供参考实现，正式产品还需要根据自身的数据、权限、预算和部署环境做适配与验证。
