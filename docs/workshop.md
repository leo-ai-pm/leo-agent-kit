# 产品架构工坊

[文档导航](README.md) · [引擎源码](../vendor/agent-workshop/blueprint/)

工坊将需求整理、组件选择、架构推导、代码检查和产品迭代组织在一个本地工作区中。可以通过网页完成主要操作，也可以在终端调用引擎。

## 安装与网页入口

在工具箱根目录执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r vendor/agent-workshop/requirements.txt
python leo.py workshop -- ui --mock
```

默认监听本机 `127.0.0.1:8765`，端口被占用时向后查找。以终端打印的地址为准。停止服务使用 `Ctrl+C`。

网页支持以下流程：

1. 配置模型，或先用 `--mock` 查看离线演示。
2. 新建产品，输入想法并回答需求问题。
3. 查看方案中的组件选型、架构与待确认清单。
4. 回答问题后更新 PRD 并重新推导。
5. 通过模拟试玩检查交互思路；这不是已生成的应用。
6. 导出交接包，交给编码助手实现。
7. 新需求进入迭代流程，保留 PRD 历史与选型变化。
8. 对已有项目发起检查，查看差距报告。

## 模型配置

工坊读取 `vendor/agent-workshop/.env`，也可读取进程环境变量；根目录 `.env` 不是工坊默认配置文件。环境变量优先于文件中的同名值。

首次配置时，可将该目录的 [`.env.example`](../vendor/agent-workshop/.env.example) 复制为 `.env`，再填写当前服务商的参数。不要覆盖已有配置。

Anthropic 格式：

```dotenv
ANTHROPIC_API_KEY=填入你的密钥
MODEL_ID=填入可用模型ID
# 使用兼容服务时填写对应地址；官方接口可省略
# ANTHROPIC_BASE_URL=https://你的服务地址
```

OpenAI 格式：

```dotenv
API_FORMAT=openai
OPENAI_API_KEY=填入你的密钥
MODEL_ID=填入可用模型ID
# 使用兼容服务时填写对应地址；官方接口可省略
# OPENAI_BASE_URL=https://你的服务地址/v1
```

模型是否可用、是否支持工具调用，取决于所选接口和模型。配置完成后，使用网页中的连接测试；去掉 `--mock` 才会调用真实模型。

```bash
python leo.py workshop -- ui
```

## 产品循环

下列命令从工具箱根目录执行。工坊参数中的相对路径以 `vendor/agent-workshop/` 为基准，所以产品路径写作 `out/my-agent`。

```bash
# 创建产品与方案
python leo.py workshop -- init my-agent "给客服人员整理工单并提出处理建议，发出回复前确认" --plan

# 新需求：升级 PRD 并重新推导
python leo.py workshop -- revise out/my-agent "加入人工转接，并保存处理记录"

# 编码助手实现 skeleton/ 后，对照需求检查
python leo.py workshop -- verify out/my-agent

# 导出文档与参考代码交接包
python leo.py workshop -- handoff out/my-agent
```

`init` 创建的 PRD 含待补齐项，不表示所有需求已经定稿。引擎不会替编码助手写好 `skeleton/`。生成代码前应先确认需求与方案。

`revise --quick` 只重算需求拆解与选型，不更新完整 `方案.md`；要交接最新完整方案，请使用完整推导。

## 单独推导与项目检查

```bash
# 单次方案，不建立完整产品循环
python leo.py workshop -- plan "根据用户上传的文档回答问题，并给出引用" -o out/document-plan

# 检查现有项目，目标路径建议使用绝对路径
python leo.py workshop -- audit /绝对路径/目标项目 -o out/project-audit

# 使用明确的 PRD 对照代码
python leo.py workshop -- audit /绝对路径/目标项目 --prd /绝对路径/需求.md -o out/project-audit-with-prd
```

`plan` 主要产出方案；需要通过工具箱的 `handoff` 交接时，目录中必须同时有 `PRD.md` 与 `方案.md`，因此优先使用 `init --plan`。

检查默认由 Agent 阅读代码并附证据；`--fast` 切换到关键词扫描，结果可能误判。报告不能替代实际运行和业务验收。

## 预算与中断恢复

```bash
python leo.py workshop -- plan "产品需求" -o out/limited-plan --max-calls 12 --max-tokens 200000

# 对支持恢复的 plan / audit 命令保留原参数与输出目录，加 --resume
python leo.py workshop -- plan "产品需求" -o out/limited-plan --max-calls 12 --max-tokens 200000 --resume
```

调用次数与 token 上限约束运行用量，不是货币价格承诺。恢复使用已保存阶段结果；并非所有子命令都支持 `--resume`，可通过子命令的 `--help` 确认。

## 输出结构

```text
vendor/agent-workshop/out/my-agent/
├── PRD.md             # 当前需求、回答和待消化的新需求
├── 方案.md             # 选型、架构、工具与验证设计
├── plan.json          # 结构化方案
├── stages/            # 推导中间结果
├── prd/               # 升版时保留历史 PRD 快照
├── skeleton/          # 编码助手实现的应用骨架
├── verify/            # verify 命令生成的检查结果
└── 迭代记录.md         # 新需求、组件变化与人工验证记录
```

部分文件随相应命令运行后生成，并非初始化时全部存在。`BLUEPRINT_OUT` 环境变量可以修改工坊输出根目录，建议设置为绝对路径。

## 实现导航

| 位置 | 职责 |
|---|---|
| [cli.py](../vendor/agent-workshop/blueprint/cli.py) | 命令与参数 |
| [forward.py](../vendor/agent-workshop/blueprint/forward.py)、[rules.py](../vendor/agent-workshop/blueprint/rules.py) | 正向方案推导与组件规则 |
| [reverse.py](../vendor/agent-workshop/blueprint/reverse.py)、[audit_agent.py](../vendor/agent-workshop/blueprint/audit_agent.py) | 反向检查与代码证据 |
| [workspace.py](../vendor/agent-workshop/blueprint/workspace.py) | PRD 快照、迭代与骨架验证 |
| [handoff.py](../vendor/agent-workshop/blueprint/handoff.py) | ZIP 交接包 |
| [llm.py](../vendor/agent-workshop/blueprint/llm.py) | 模型配置、预算与结果校验 |
| [blueprint/web/](../vendor/agent-workshop/blueprint/web/) | 网页服务与任务管理 |
| [web/](../vendor/agent-workshop/web/) | 前端源码 |
| [docs/examples/](../vendor/agent-workshop/docs/examples/) | 方案和检查报告示例 |
| [evals/](../vendor/agent-workshop/evals/)、[tests/](../vendor/agent-workshop/tests/) | 评估案例与自动化测试 |
