import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["cesium"],
  webpack(config) {
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      path: false,
      url: false
    };
    return config;
  }
};

export default nextConfig;
