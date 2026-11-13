# Leo Agent Kit

面向 AI 产品经理的本地开发工具箱：学习 Harness、推导产品架构，再把 PRD 和方案交给编码助手按阶段实现。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square)

## 三个工作入口

| 入口 | 解决的问题 | 交付 |
|---|---|---|
| Learn · Harness 学习 | 是否需要 Agent、选哪些组件 | 17 章示例、选型指南与判断练习 |
| Workshop · 架构工坊 | 如何把需求变成可实现的方案 | PRD、组件选型、架构方案与验证设计 |
| Delivery · 项目交付 | 如何衔接方案、开发与验收 | 独立工作区、六阶段流程与证据包 |

## 快速开始

```bash
git clone https://github.com/leo-ai-pm/leo-agent-kit.git
cd leo-agent-kit
python3 leo.py doctor
python3 leo.py learn
python3 leo.py init my-agent
python3 leo.py delivery my-agent task
```

`learn` 打印本地课程地址，复制到浏览器打开。`init` 为每个产品创建独立的 `workspace/<产品名>/`，包括交付规则、手册和阶段管理器；已存在的工作区不会被覆盖。用编码助手打开这个目录，按里面的规则开始需求讨论。

需要架构引擎时，在独立虚拟环境安装依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r vendor/agent-workshop/requirements.txt
python leo.py workshop -- --help
```

模型配置、引擎子命令和费用设置参见 `vendor/agent-workshop/使用引导.md`。运行课程代码也可能安装依赖和调用模型；浏览课程、初始化与文档交接不调用模型。

## 从方案到交付

取得工坊输出目录中的 `PRD.md` 与 `方案.md` 后：

```bash
python3 leo.py handoff my-agent /绝对路径/工坊输出目录
python3 leo.py delivery my-agent task
python3 leo.py delivery my-agent check
python3 leo.py delivery my-agent status
```

交接会检查两份文档都存在且非空，保留 SHA-256 摘要，拒绝覆盖已有文档。后续改稿在工作区完成；摘要记录的是导入时的版本。只有用户实际验收通过后才运行 `delivery my-agent accept --confirmed`，底层管理器仍会检查自检结果。该标志记录操作者的确认，不是身份认证或防篡改审批。

## 产品能力

- 一个 Python 命令行连接三个入口，统一入口参数与退出码。
- 每个产品独立复制交付环境，避免多个项目共用流程状态。
- PRD / 方案成对交接、输入校验、版本摘要和覆盖保护。
- 源码版本锁定、基础资源检查与跨模块回归测试。

当前提供命令行工作流，覆盖学习、方案推导与项目交付。三个入口分别配置模型和运行环境，通过文档完成交接。统一网页界面尚未提供；真实模型生成和部署需要按项目单独验收。

## 验证

```bash
python3 -m unittest discover -s tests -v
python3 leo.py doctor
```
