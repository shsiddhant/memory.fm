// Doesn't work. Known issue in Vite 8: import useWebSocket from "react-use-websocket";

// Workaround
import useWebSocketModule from "react-use-websocket";
const useWebSocket = (
  (useWebSocketModule as unknown as { default: typeof useWebSocketModule }).default || 
  useWebSocketModule
);


import { useMemo, useRef, useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";

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

export const useSyncStatus = (username: string, isSyncActive: boolean) => {
    const queryClient = useQueryClient();

    const socketUrl = useMemo(
      () => {
        if (!isSyncActive) return null;
        return `${WEBSOCKET_URL}/ws/sync-progress?username=${username}`;
      },
      [username, isSyncActive]
    );

    const lastHandledRef = useRef<string | null>(null);

    const { lastJsonMessage, readyState } = useWebSocket<SyncStatus>(
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
    },
    isSyncActive
  );

  useEffect(() => {
    if (!lastJsonMessage) return;
    const { status, fetched_scrobbles } = lastJsonMessage;

    const key = `${username}-${status}-${fetched_scrobbles ?? 0}`;

    if (lastHandledRef.current === key) return;

    lastHandledRef.current = key;

    console.log("WS EVENT:", lastJsonMessage);
  
    // Refresh if completed
    if (status == "completed") {
      queryClient.invalidateQueries({
        queryKey: ["summaryQuery", username],
        refetchType: "active",
      });
    }
  }, [lastJsonMessage?.fetched_scrobbles, username]);

  return {
    syncStatus: lastJsonMessage,
    readyState,
  };
};
