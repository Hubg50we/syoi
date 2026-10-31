"use client";

import dynamic from "next/dynamic";
import { useEffect } from "react";

import LandingPage from "@/components/landing-page";
import { useSession } from "@/lib/auth-client";
import { isLandingOnlyModeEnabled } from "@/lib/app-flags";

const HomeApp = dynamic(() => import("@/components/home-app"), {
  ssr: false,
});

export function HomeRouter() {
  const { data: session, isPending } = useSession();

  useEffect(() => {
    if (!isPending && !session?.user && typeof window !== "undefined") {
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get("landing") !== "true") {
        window.location.href = "/api/auth/guest";
      }
    }
  }, [isPending, session]);

  if (!isLandingOnlyModeEnabled && !isPending && session?.user) {
    return <HomeApp />;
  }

  return <LandingPage />;
}
