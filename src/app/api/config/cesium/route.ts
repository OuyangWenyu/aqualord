import { NextResponse } from "next/server";

export function GET() {
  const token = process.env.CESIUM_TOKEN;

  if (!token) {
    return NextResponse.json(
      {
        error: "Missing CESIUM_TOKEN. Create .env.local from .env.example and add a Cesium Ion token."
      },
      { status: 500 }
    );
  }

  return NextResponse.json({ token });
}
