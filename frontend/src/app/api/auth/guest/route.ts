import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import prisma from "@/lib/prisma";
import crypto from "crypto";

export async function GET(request: Request) {
  try {
    let user = await prisma.user.findFirst();
    if (!user) {
      user = await prisma.user.create({
        data: {
          id: "user-1",
          name: "Creator",
          email: "creator@local.test",
          emailVerified: true,
          createdAt: new Date(),
          updatedAt: new Date(),
        },
      });
    }

    const token = crypto.randomUUID();
    const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000);

    await prisma.session.create({
      data: {
        id: crypto.randomUUID(),
        userId: user.id,
        token: token,
        expiresAt: expiresAt,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    });

    const cookieStore = await cookies();
    const isHttps = request.url.startsWith("https:");
    cookieStore.set("better-auth.session_token", token, {
      path: "/",
      httpOnly: true,
      secure: isHttps,
      sameSite: "lax",
      maxAge: 30 * 24 * 60 * 60,
    });
    if (isHttps) {
      cookieStore.set("__Secure-better-auth.session_token", token, {
        path: "/",
        httpOnly: true,
        secure: true,
        sameSite: "lax",
        maxAge: 30 * 24 * 60 * 60,
      });
    }

    const incomingUrl = new URL(request.url);
    const redirectUrl = incomingUrl.searchParams.get("redirect") || "/";
    return NextResponse.redirect(new URL(redirectUrl, request.url));
  } catch (error) {
    console.error("Guest login failed:", error);
    return NextResponse.redirect(new URL("/", request.url));
  }
}
