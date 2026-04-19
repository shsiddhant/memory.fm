// Types and Interfaces

import type { DateValue } from "@chakra-ui/react";

export interface TopChart {
    name: string,
    scrobbles: number
    [key: string]: string | number; 
}

export interface Dates {
    from_ts: DateValue;
    to_ts: DateValue;
}

// Period Selection Mode
export type Mode = number | "all_time" | "custom";

export interface ModeOption {
  value: Mode;
  label: string;
}

// Kind
export type KindType = "track" | "artist" | "album"

// Analytics Parameters (for analytics such as Top Charts, Attachment Index, Streaks etc)
export type AnalyticsParams = {
  limit: number
  mode: Mode
  kind: KindType
}

