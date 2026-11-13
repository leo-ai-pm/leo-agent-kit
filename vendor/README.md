# 模块源码导航

[返回项目首页](../README.md) · [使用文档](../docs/README.md)

这里保存三个模块的完整代码、资源、文档和测试。各模块有自己的内部目录与运行环境；工具箱通过根目录 `leo.py` 调用它们。

| 模块 | 代码入口 | 资源与文档 | 工具箱操作说明 |
|---|---|---|---|
| Harness 组件库 | [s01–s17 实现目录](claude-code-harness-study/) | [机制与选型](claude-code-harness-study/guide/)、[浏览界面](claude-code-harness-study/web/)、[测试](claude-code-harness-study/tests/) | [组件索引](../docs/harness.md) |
| 产品架构工坊 | [blueprint/](agent-workshop/blueprint/) | [前端](agent-workshop/web/)、[示例输出](agent-workshop/docs/examples/)、[评估案例](agent-workshop/evals/)、[测试](agent-workshop/tests/) | [工坊操作](../docs/workshop.md) |
| 项目交付 | [kit.sh](idea-to-launch-kit/kit.sh)、[verify.sh](idea-to-launch-kit/verify.sh) | [技术手册](idea-to-launch-kit/docs/手册/)、[产品模板](idea-to-launch-kit/projects/) | [交付流程](../docs/delivery.md) |

## 运行入口

以下命令从工具箱根目录执行：

```bash
python3 leo.py learn web
python leo.py workshop -- ui --mock
python3 leo.py init my-agent
```

前两个命令分别启动组件界面和工坊界面，需要在不同终端运行；工坊需要先安装依赖。第三个命令创建交付工作区，不会启动应用。

正式产品的交付代码写入 `workspace/<产品名>/`，避免直接修改交付模板。工坊生成的方案与迭代资料默认写入 `agent-workshop/out/`。
