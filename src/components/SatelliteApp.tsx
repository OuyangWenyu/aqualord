"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import dynamic from "next/dynamic";

import type { CoverageWindow, CuratedSatellite, GeoPoint, SensorType, TleRecord } from "@/domain/satellites/types";
import { isValidGeoPoint } from "@/domain/coverage/distance";
import { nowCoveringCount, predictCoverageWindows } from "@/domain/coverage/predictCoverage";

const EarthViewer = dynamic(() => import("./EarthViewer"), {
  ssr: false,
  loading: () => <div className="boot">正在加载 Cesium 3D 地球...</div>
});

type CuratedResponse = {
  satellites: CuratedSatellite[];
  cache: string;
  warning?: string;
};

type EoResponse = {
  records: TleRecord[];
  cache: string;
  warning?: string;
};

type SensorFilter = "all" | SensorType;
type PlaybackMultiplier = 1 | 10 | 60 | 300;

const DEFAULT_POINT: GeoPoint = { lat: 31.2304, lon: 121.4737 };
const PLAYBACK_MULTIPLIERS: PlaybackMultiplier[] = [1, 10, 60, 300];

export default function SatelliteApp() {
  const [token, setToken] = useState<string | null>(null);
  const [configError, setConfigError] = useState<string | null>(null);
  const [curated, setCurated] = useState<CuratedSatellite[]>([]);
  const [eoCatalog, setEoCatalog] = useState<TleRecord[]>([]);
  const [dataWarning, setDataWarning] = useState<string | null>(null);
  const [selectedPoint, setSelectedPoint] = useState<GeoPoint>(DEFAULT_POINT);
  const [latInput, setLatInput] = useState(String(DEFAULT_POINT.lat));
  const [lonInput, setLonInput] = useState(String(DEFAULT_POINT.lon));
  const [windows, setWindows] = useState<CoverageWindow[]>([]);
  const [nowCount, setNowCount] = useState<number | null>(null);
  const [sensorFilter, setSensorFilter] = useState<SensorFilter>("all");
  const [activeWindow, setActiveWindow] = useState<CoverageWindow | null>(null);
  const [showAllFootprints, setShowAllFootprints] = useState(false);
  const [playbackMultiplier, setPlaybackMultiplier] = useState<PlaybackMultiplier>(1);
  const [isPredicting, setIsPredicting] = useState(false);

  useEffect(() => {
    async function loadConfig() {
      const response = await fetch("/api/config/cesium");
      const body = await response.json();

      if (!response.ok) {
        setConfigError(body.error ?? "Cesium Ion token 配置缺失");
        return;
      }

      setToken(body.token);
    }

    loadConfig().catch((error) => {
      setConfigError(error instanceof Error ? error.message : "Cesium 配置加载失败");
    });
  }, []);

  useEffect(() => {
    async function loadData() {
      const [curatedResponse, eoResponse] = await Promise.all([
        fetch("/api/tle/curated"),
        fetch("/api/tle/eo-catalog")
      ]);
      const curatedBody = (await curatedResponse.json()) as CuratedResponse;
      const eoBody = (await eoResponse.json()) as EoResponse;

      setCurated(curatedBody.satellites ?? []);
      setEoCatalog(eoBody.records ?? []);

      const warnings = [curatedBody.warning, eoBody.warning].filter(Boolean).join("；");
      setDataWarning(warnings || null);
    }

    loadData().catch((error) => {
      setDataWarning(error instanceof Error ? error.message : "TLE 数据加载失败");
    });
  }, []);

  const queryableSatellites = useMemo(() => curated.filter((sat) => sat.tle), [curated]);

  const filteredWindows = useMemo(() => {
    if (sensorFilter === "all") {
      return windows;
    }

    return windows.filter((window) => window.satellite.sensorType === sensorFilter);
  }, [sensorFilter, windows]);

  const runCoverage = useCallback(
    (point: GeoPoint) => {
      if (!isValidGeoPoint(point) || queryableSatellites.length === 0) {
        return;
      }

      setIsPredicting(true);
      setActiveWindow(null);

      window.setTimeout(() => {
        const startTime = new Date();
        setNowCount(nowCoveringCount(queryableSatellites, point, startTime));
        setWindows(
          predictCoverageWindows(queryableSatellites, point, {
            startTime,
            horizonHours: 72,
            stepSeconds: 60
          })
        );
        setIsPredicting(false);
      }, 20);
    },
    [queryableSatellites]
  );

  useEffect(() => {
    if (queryableSatellites.length > 0 && windows.length === 0 && nowCount === null) {
      runCoverage(selectedPoint);
    }
  }, [nowCount, queryableSatellites.length, runCoverage, selectedPoint, windows.length]);

  function handleEarthPoint(point: GeoPoint) {
    const rounded = {
      lat: Number(point.lat.toFixed(5)),
      lon: Number(point.lon.toFixed(5))
    };
    setSelectedPoint(rounded);
    setLatInput(String(rounded.lat));
    setLonInput(String(rounded.lon));
    runCoverage(rounded);
  }

  function handleManualRun() {
    const point = {
      lat: Number(latInput),
      lon: Number(lonInput)
    };

    if (!isValidGeoPoint(point)) {
      setDataWarning("请输入合法经纬度：纬度 -90 到 90，经度 -180 到 180。");
      return;
    }

    setSelectedPoint(point);
    setDataWarning(null);
    runCoverage(point);
  }

  async function copyResults() {
    const payload = {
      selectedPoint,
      nowCovering: nowCount,
      horizonHours: 72,
      windows: filteredWindows
    };
    await navigator.clipboard.writeText(JSON.stringify(payload, null, 2));
  }

  return (
    <main className="app-shell">
      <section className="viewer-panel">
        {token ? (
          <EarthViewer
            token={token}
            curated={queryableSatellites}
            eoCatalog={eoCatalog}
            selectedPoint={selectedPoint}
            windows={filteredWindows}
            activeWindow={activeWindow}
            showAllFootprints={showAllFootprints}
            playbackMultiplier={playbackMultiplier}
            onSelectPoint={handleEarthPoint}
          />
        ) : (
          <div className="boot">{configError ?? "正在读取 Cesium Ion token..."}</div>
        )}
        <div className="viewer-overlay">
          <span className="status-dot" />
          <span>
            精选卫星 {queryableSatellites.length}/{curated.length || 0} 可查询 · EO catalog{" "}
            {eoCatalog.length} 颗用于视觉展示
          </span>
        </div>
      </section>

      <aside className="side-panel">
        <header className="side-header">
          <h1>遥感卫星潜在覆盖查询</h1>
          <p>点选地球或输入经纬度，查询未来 72 小时精选对地观测卫星的几何潜在覆盖。</p>
        </header>

        <div className="panel-body">
          {configError ? <div className="notice error">{configError}</div> : null}
          {dataWarning ? <div className="notice error">{dataWarning}</div> : null}

          <section className="section">
            <div className="section-title">Selected point</div>
            <div className="input-grid">
              <div className="field">
                <label htmlFor="lat">Lat</label>
                <input id="lat" value={latInput} onChange={(event) => setLatInput(event.target.value)} />
              </div>
              <div className="field">
                <label htmlFor="lon">Lon</label>
                <input id="lon" value={lonInput} onChange={(event) => setLonInput(event.target.value)} />
              </div>
            </div>
            <div className="actions">
              <button className="button primary" onClick={handleManualRun} disabled={isPredicting}>
                {isPredicting ? "计算中..." : "Run coverage"}
              </button>
              <button className="button" onClick={copyResults} disabled={filteredWindows.length === 0}>
                Copy results
              </button>
            </div>
          </section>

          <section className="section">
            <div className="metrics">
              <div className="metric">
                <span>当前覆盖</span>
                <strong>{nowCount ?? "-"}</strong>
              </div>
              <div className="metric">
                <span>未来窗口</span>
                <strong>{filteredWindows.length}</strong>
              </div>
            </div>
          </section>

          <section className="section">
            <div className="section-title">
              <span>Filters</span>
              <label>
                <input
                  type="checkbox"
                  checked={showAllFootprints}
                  onChange={(event) => setShowAllFootprints(event.target.checked)}
                />{" "}
                全部 footprint
              </label>
            </div>
            <div className="field">
              <select
                value={sensorFilter}
                onChange={(event) => setSensorFilter(event.target.value as SensorFilter)}
              >
                <option value="all">All sensors</option>
                <option value="multispectral">Multispectral</option>
                <option value="optical">Optical</option>
                <option value="sar">SAR</option>
                <option value="weather">Weather</option>
              </select>
            </div>
          </section>

          <section className="section">
            <div className="section-title">Time playback</div>
            <div className="segmented-control" aria-label="Time playback speed">
              {PLAYBACK_MULTIPLIERS.map((multiplier) => (
                <button
                  key={multiplier}
                  className={playbackMultiplier === multiplier ? "active" : ""}
                  type="button"
                  onClick={() => setPlaybackMultiplier(multiplier)}
                  aria-pressed={playbackMultiplier === multiplier}
                >
                  {multiplier}x
                </button>
              ))}
            </div>
          </section>

          <div className="notice">
            结果仅表示几何潜在覆盖；未评估云量、昼夜条件、侧摆成像、任务排程和数据实际可用性。
          </div>

          <section className="section">
            <div className="section-title">未来 72 小时潜在过境</div>
            <div className="results">
              {filteredWindows.length === 0 ? (
                <div className="empty">{isPredicting ? "正在计算..." : "暂无覆盖窗口"}</div>
              ) : (
                filteredWindows.slice(0, 80).map((window) => (
                  <button
                    key={`${window.satellite.noradId}-${window.closestTime}`}
                    className={`result-card ${activeWindow === window ? "active" : ""}`}
                    onClick={() => setActiveWindow(window)}
                  >
                    <div className="result-top">
                      <div className="result-title">{window.satellite.name}</div>
                      <span className="tag">{window.satellite.sensorType}</span>
                    </div>
                    <div className="result-meta">
                      {formatTime(window.startTime)} - {formatTime(window.endTime)}
                      <br />
                      Closest: {formatTime(window.closestTime)} · {window.minDistanceKm} km
                      <br />
                      {window.satellite.resolutionM}m · {window.satellite.swathKm}km swath
                    </div>
                  </button>
                ))
              )}
            </div>
          </section>
        </div>
      </aside>
    </main>
  );
}

function formatTime(value: string) {
  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "UTC",
    hour12: false
  }).format(new Date(value));
}
