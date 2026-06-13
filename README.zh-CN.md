# Aqualord

[English](README.md) | 简体中文

Aqualord 是一个面向遥感与水资源工作流的 AOI 元数据查询项目。当前产品边界是：输入 Query GeoJSON，输出理论 Observation Opportunity，并通过整理过的任务/平台/传感器元数据连接未来的历史资产查询路径。

它不是通用流域注册表，也还不是历史影像归档或 STAC Item 搜索引擎。

参考背景：

- [Satellite Remote Sensing for Water Resources Management: Potential for Supporting Sustainable Development in Data-Poor Regions](https://doi.org/10.1029/2017WR022437)
- [Applied Remote Sensing Training](https://arset.gsfc.nasa.gov/)
- [FrontierDevelopmentLab/sat-extractor](https://github.com/FrontierDevelopmentLab/sat-extractor)

## 内容结构

- `aqualord/`：Python 包和 CLI，包含 opportunity query、catalog 加载、轨道 provider、tracking index 和 provenance。
- `src/`：Next.js + CesiumJS 前端，用于交互式卫星覆盖探索。
- `tests/`：Python 回归测试，覆盖 CLI、catalog 生成、provenance 和 orbit provider。
- `examples/`：GeoJSON 输入样例和 opportunity 输出样例。
- `docs/`：MVP 边界、ADR、agent 文档和历史资料整理策略。
- `reference/`：历史数据源笔记，作为知识来源和 provenance 材料保留。
- `scripts/`：生成和维护脚本。
- `skills/`：把自然语言观测机会问题路由到 CLI 的 Codex skill。

历史数据源笔记已经从根目录迁移到 `reference/`。这些笔记不是运行时产品事实；查询使用的结构化事实位于 `aqualord/data/*.json`。

## Python 环境

Python 项目使用 `uv`：

```shell
uv sync --dev
uv run pytest
```

将 CLI 安装为全局 uv tool：

```shell
uv tool install --editable D:\Code\aqualord --force
aqualord opportunities --geo examples\query-dalian.geojson --hours 48 --format json
```

## JavaScript 环境

前端使用 npm 脚本：

```shell
npm install
npm run dev
npm test
npm run lint
npm run build
```

在 Windows PowerShell 中，如果 `npm.ps1` 被执行策略拦截，可以使用 `npm.cmd`。

## Observation Opportunity MVP

Aqualord 包含一个 Python CLI 和一个 Next.js + CesiumJS MVP，用于潜在遥感卫星覆盖查询。它使用整理过的任务元数据、CelesTrak TLE 数据和 `satellite.js`，估算选定地面点或查询几何的理论覆盖。

核心流程：

- 在 3D 地球上选择点，或手动输入经纬度。
- 查询当前潜在覆盖的地球观测卫星。
- 预测未来 72 小时的潜在覆盖窗口。
- 在 Cesium 中可视化卫星、轨道环、地面轨迹、幅宽带和足迹。

配置 Cesium Ion token：

```shell
cp .env.example .env.local
```

然后设置：

```shell
CESIUM_TOKEN=your_cesium_ion_token_here
```

运行 Web 应用：

```shell
npm install
npm run dev
```

打开 `http://localhost:3000`。

MVP 只报告几何意义上的潜在覆盖。它不评估云量、昼夜条件、离轴成像、SAR 成像模式、调度约束，也不确认真实数据可用性。

## 历史知识来源

历史 WRM 笔记保留在 `reference/` 下作为资料来源。见 `reference/README.md` 查看来源索引，见 `docs/legacy-knowledge-sources.md` 查看迁移策略。

## 贡献

1. Fork 本仓库。
2. 创建 feature branch。
3. 提交变更。
4. 打开 pull request。
