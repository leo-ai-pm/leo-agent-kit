# 广告营销视频产品：从需求到交付

[返回项目首页](../../README.md) · [查看需求输入](brief.md)

本示例规划一个面向电商运营的视频广告产品。演示结果是需求与方案、独立交付工作区和当前阶段任务；实际的视频生成服务仍需后续实现。

## 准备

在工具箱根目录创建虚拟环境并安装工坊依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r vendor/agent-workshop/requirements.txt
python leo.py doctor
```

## 1. 用需求文件生成离线示例方案

```bash
python leo.py workshop -- init ad-video ../../examples/marketing-video/brief.md --plan --mock
```

工坊以自身目录为工作目录，所以示例文件路径前面有 `../../`。结果位于 `vendor/agent-workshop/out/ad-video/`，包括 `PRD.md`、`方案.md` 和 `plan.json` 等文件。

`--mock` 使用启发式占位内容，只用于检查流程和文件交接。不要把它直接视为经过真实模型推导、业务确认的可执行方案。

## 2. 初始化并交接

```bash
python leo.py init ad-video
python leo.py handoff ad-video vendor/agent-workshop/out/ad-video
python leo.py delivery ad-video task
python leo.py delivery ad-video status
```

应看到：

- `workspace/ad-video/leo-project.json` 中有两份文档的摘要。
- `workspace/ad-video/projects/ad-video/docs/PRD/` 中有两份文档。
- 当前阶段为 `阶段0`，任务是需求体检与补全。
- `docs/本阶段任务.md` 列出当前需要读取和提交的文件。

这是初始化完成，不代表阶段 0 已验收。再次运行时换一个产品名，避免与已有结果混淆。

## 3. 转入真实产品工作

先在工坊配置模型，使用新产品名去掉 `--mock` 重新推导，确认方案后再交接。然后用编码助手打开对应的 `workspace/<产品名>/`。

```text
请读取工作区根目录的 AGENTS.md 和当前产品的 PRD、方案。
先完成需求体检，确认视频生成接口、预算、素材保存和第一版范围。
核心链路按“输入商品资料 → 确认脚本与分镜 → 确认预算 → 生成素材 → 查看与重试”推进。
只实现当前阶段，提供可运行结果与验收证据。
```

## 需要逐项验证的产品行为

| 场景 | 应检查的行为 |
|---|---|
| 用户没有提供关键商品信息 | 先追问，不虚构功效与规格 |
| 用户尚未确认脚本 | 不进入付费素材生成 |
| 外部生成接口失败 | 保留成功镜头与任务状态，允许重试 |
| 用户刷新或重启服务 | 能重新获取项目和任务进度 |
| 用户只修改一个镜头 | 只重做相关素材，并记录用量 |
| 用户准备导出 | 检查顺序、文案、素材引用与人工确认 |

这些是该示例产品的需求与验收方向，不是工具箱已经实现的视频功能。
