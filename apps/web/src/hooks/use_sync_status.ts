import { useMemo } from "react";
import { useSyncWebSocket } from "@/hooks/use_sync_websocket";
import type { SyncStatus } from "@/hooks/use_sync_websocket";


export function useSyncStatus(username: string) {

  const { lastJsonMessage, } = useSyncWebSocket(username);

   const syncStatus: SyncStatus | null = useMemo(() => {
    if (!lastJsonMessage) return null;
    return lastJsonMessage;
  }, [lastJsonMessage]);


  const isSyncActive =
    lastJsonMessage?.status === "started" ||
    lastJsonMessage?.status === "progress" ||
    lastJsonMessage?.status === "retry";


  return {
    syncStatus,
    isSyncActive,
  };
}
