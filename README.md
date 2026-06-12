# 遥感卫星潜在覆盖查询 MVP

一个基于 Next.js、CesiumJS、CelesTrak TLE 和 `satellite.js` 的 3D 遥感卫星潜在覆盖查询工具。

核心交互：

- 点选 3D 地球或输入经纬度
- 查询当前有多少精选卫星几何覆盖该点
- 查询未来 72 小时潜在过境窗口
- 在 Cesium 地球上高亮相关卫星、轨道和 footprint
- 淡化显示 CelesTrak earth resources catalog，用于视觉探索

## 配置

Cesium Ion token 是 MVP 必需配置。

```bash
cp .env.example .env.local
```

然后填写：

```bash
CESIUM_TOKEN=your_cesium_ion_token_here
```

## 运行

```bash
npm install
npm run dev
```

打开 `http://localhost:3000`。

## 模型边界

结果仅表示几何潜在覆盖；未评估云量、昼夜条件、侧摆成像、任务排程和数据实际可用性。

MVP 覆盖判断使用近似模型：

```txt
轨下点到查询点的大圆距离 <= 传感器幅宽 / 2
```

默认预测：

```txt
未来 72 小时
60 秒时间步长
按窗口开始时间升序
```

## 数据策略

可信查询层：

- 10-20 颗精选遥感卫星
- 人工维护传感器类型、幅宽和分辨率
- 参与覆盖查询

视觉探索层：

- CelesTrak `GROUP=resource`
- 仅用于轨道/点位视觉展示
- 不参与覆盖查询

## 主要目录

```txt
src/app/api/tle/curated       精选卫星 TLE API
src/app/api/tle/eo-catalog    EO catalog 视觉层 API
src/components                Cesium 和查询 UI
src/domain/coverage           覆盖预测
src/domain/orbits             SGP4 传播
src/domain/satellites         卫星配置和类型
src/domain/tle                TLE 解析
```
