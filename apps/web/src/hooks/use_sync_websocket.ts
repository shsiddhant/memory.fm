// Doesn't work. Known issue in Vite 8: import useWebSocket from "react-use-websocket";

// Workaround
import useWebSocketModule from "react-use-websocket";
const useWebSocket = (
  (useWebSocketModule as unknown as { default: typeof useWebSocketModule }).default || 
  useWebSocketModule
);
import { useMemo } from "react";

import { WEBSOCKET_URL } from "@/api/urls";

export type SyncStatusType = 
  | "started"
  | "progress"
  | "completed"
  | "retry"
  | "error"
  | "warning";

export interface SyncStatus {
    status: SyncStatusType | null;
    page: number | null;
    totalpages: number | null;
    fetched_scrobbles: number | null;
    total_scrobbles: number | null;
    retry: number | null;
    total_retries: number | null;
    error: string | null;
    phase: string | null;
}

export function useSyncWebSocket(username: string) {

  const shouldConnect = !!username?.trim();
  const socketUrl = useMemo(
    () => {
      if (!shouldConnect) return null;
      return `${WEBSOCKET_URL}/ws/sync-progress?username=${username}`;
    }, [username, shouldConnect] );

  const { lastJsonMessage } = useWebSocket<SyncStatus>(
    socketUrl,
    {
      shouldReconnect: () => true,
      share: true,
      
      onOpen: () => {
        console.log("WS OPEN");
      },
      onError: (e) => {
        console.log("WS ERROR", e);
      },
      onClose: () => {
        console.log("WS CLOSE");
      },
    }, shouldConnect );

  return { lastJsonMessage };
}