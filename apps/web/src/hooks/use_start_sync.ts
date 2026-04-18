import { syncUserScrobbles } from "@/api/user";

export function useStartSync() {

  return async (username: string) => {

    await syncUserScrobbles(username);
  };
}