import { useSyncWebSocket } from "./use_sync_websocket";

export function useSync(username: string) {

  const { lastJsonMessage, } = useSyncWebSocket(
    username,
  );

  const isSyncing = lastJsonMessage?.status == "progress";


  return {
    syncStatus: lastJsonMessage ?? null,
    isSyncing,
  };
}