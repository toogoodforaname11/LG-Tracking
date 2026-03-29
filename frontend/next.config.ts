import type { NextConfig } from "next";

const isStaticExport = process.env.STATIC_EXPORT === "true";

const nextConfig: NextConfig = {
  ...(isStaticExport
    ? { output: "export", distDir: "out" }
    : {
        async rewrites() {
          const API_URL =
            process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
          return [
            {
              source: "/api/:path*",
              destination: `${API_URL}/api/:path*`,
            },
          ];
        },
      }),
};

export default nextConfig;
