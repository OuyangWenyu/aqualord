import "cesium/Build/Cesium/Widgets/widgets.css";
import "./globals.css";

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "遥感卫星潜在覆盖查询",
  description: "基于 TLE 和传感器幅宽的对地观测卫星潜在覆盖查询 MVP"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
