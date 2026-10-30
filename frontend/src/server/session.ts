import { headers } from "next/headers";

import { auth } from "@/lib/auth";
import prisma from "@/lib/prisma";

export async function getServerSession() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (session?.user?.id) {
    return session;
  }

  // In local self-hosted/dev mode, if no session cookie was passed,
  // fall back to the active local user so local requests never 401.
  try {
    const localUser = await prisma.user.findFirst();
    if (localUser) {
      return {
        user: {
          id: localUser.id,
          name: localUser.name,
          email: localUser.email,
          image: localUser.image,
          createdAt: localUser.createdAt,
          updatedAt: localUser.updatedAt,
        },
        session: {
          id: "local_dev_session",
          userId: localUser.id,
          expiresAt: new Date(Date.now() + 86400000 * 30),
        },
      } as unknown as typeof session;
    }
  } catch {
    // Database unreachable
  }

  return session;
}
