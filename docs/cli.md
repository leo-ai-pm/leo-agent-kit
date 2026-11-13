# 命令参考

[文档导航](README.md)

以下命令从工具箱根目录执行。只使用初始化和文档交接时，Python 标准库即可；工坊命令还需要安装工坊依赖。

## 全局参数

```bash
python3 leo.py --help
python3 leo.py --workspace /绝对路径/我的工作区 init my-agent
```

`--workspace` 必须放在子命令之前，默认值是工具箱根目录下的 `workspace/`。创建、交接和交付操作都应使用同一个值。

项目名限 1–64 个中文、字母、数字、下划线或连字符，建议使用容易输入的短名称。

## 工具箱命令

| 命令 | 参数 | 行为 |
|---|---|---|
| `doctor` | 无 | 检查锁定模块中的关键文件、输出 Python 与 Bash 信息 |
| `learn` | 可选 `web`、`s01`–`s17` 等运行器入口 | 不带参数只打印本地地址；带参数调用组件运行器 |
| `workshop` | `--` 后跟引擎参数 | 转发给 `python -m blueprint` |
| `init` | 产品名 | 复制交付模板，建立独立工作区，拒绝覆盖 |
| `handoff` | 产品名、来源目录 | 检查并导入 PRD / 方案，保存摘要 |
| `delivery` | 产品名、`task/status/check/accept` | 调用工作区中的阶段管理器 |

`delivery accept` 需要 `--confirmed`；`--next-stage` 用于阶段管理器要求的分支选择，不是跳过自检的开关。

## 工坊子命令

```bash
python leo.py workshop -- --help
python leo.py workshop -- init --help
python leo.py workshop -- audit --help
```

| 子命令 | 用途 | 常用选项 |
|---|---|---|
| `ui` | 本地网页 | `--mock`、`--port`、`--no-browser` |
| `init NAME IDEA` | 建立产品工作区 | `--plan`、`--mock` |
| `plan INPUT` | 推导方案 | `-o`、`--mock`、`--resume` |
| `revise WORKSPACE REQUIREMENT` | 新需求与 PRD 升版 | `--quick`、`--no-plan`、`--mock` |
| `verify WORKSPACE` | 对照 PRD 检查骨架 | `--fast`、`--mock` |
| `audit PROJECT` | 检查外部项目 | `--prd`、`-o`、`--fast`、`--rejudge`、`--resume` |
| `handoff WORKSPACE` | 导出 ZIP 交接包 | `-o` |
| `eval` | 运行评估案例 | 默认离线；真实模型模式需额外选项 |

需要模型的命令通常支持 `--model`、`--max-calls`、`--max-tokens`。以相应 `--help` 为准，参数并非在所有命令中通用。

## 路径基准

| 参数所在位置 | 相对路径以哪里为起点 | 示例 |
|---|---|---|
| `leo.py handoff` 的来源目录 | 当前终端目录 | 根目录下用 `vendor/agent-workshop/out/my-agent` |
| `leo.py --workspace` | 当前终端目录 | 推荐用绝对路径 |
| `workshop --` 后的输入、工作区与 `-o` | `vendor/agent-workshop/` | `out/my-agent` |
| 工坊的 `.env` | 固定的工坊模块目录 | `vendor/agent-workshop/.env` |

例如从仓库根目录给工坊读取示例文件：

```bash
python leo.py workshop -- init ad-video ../../examples/marketing-video/brief.md --plan --mock
python leo.py handoff ad-video vendor/agent-workshop/out/ad-video
```

第二条命令要求先运行 `python leo.py init ad-video`。外部文件建议使用绝对路径，路径含空格时加引号。

## 两个 handoff 的区别

- `python leo.py workshop -- handoff out/my-agent`：工坊导出 ZIP，包括需求、方案与参考材料。
- `python leo.py handoff my-agent vendor/agent-workshop/out/my-agent`：把两份 Markdown 文档导入已初始化的交付工作区。

前者接收工坊工作区，后者接收产品名和包含两份文档的目录，不能把 ZIP 直接传给后者。

## 常见问题

| 现象 | 原因与处理 |
|---|---|
| 缺少 `dotenv`、`anthropic` 等模块 | 激活根目录虚拟环境，并安装工坊 `requirements.txt` |
| 网页显示 mock 模式 | 去掉 `--mock`，在工坊目录配置模型后重新启动 |
| 模型 Key 配好了仍不生效 | 检查是否误放到根目录 `.env`，或有环境变量覆盖 |
| 工坊找不到需求文件 | 工坊相对路径从模块目录计算；改用绝对路径 |
| `项目已存在` | 初始化拒绝覆盖；使用新名称，或继续原工作区 |
| `缺少普通文件：方案.md` | 来源目录缺文件或文件是符号链接；先完成方案推导 |
| `已有 PRD.md` | 工作区已有文档；先明确版本并归档，不自动覆盖 |
| 自检提示缺少阶段产物 | 完成当前任务要求的文档或证据，再运行 `check` |
| 自检通过但阶段没有变化 | 仍等待实际验收，确认后运行 `accept --confirmed` |
| `file://` 页面内容不完整 | 使用 `python3 leo.py learn web` 启动本地服务 |

## 检查范围

`doctor` 是关键文件检查，不是逐文件完整性校验，也不测试模型或云平台。工具箱自身的可重复检查为：

```bash
python3 -m unittest discover -s tests -v
python3 leo.py doctor
```

工坊、组件与具体应用有各自的测试。通过工具箱测试并不等于所有模型接口、应用功能和部署环境均已验证。
