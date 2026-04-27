import { useState } from "react"
import { type AnalyticsParams } from "@/typing"
import { useQuery } from "@tanstack/react-query"
import { fetchYearRange } from "@/api/user"

export default function useAnalyticsParams(initial: AnalyticsParams) {
  const [params, setParams] = useState(initial)

  const setParam =
    <K extends keyof AnalyticsParams>(key: K) =>
    (value: AnalyticsParams[K]) => {
      setParams((prev) => ({ ...prev, [key]: value }))
    }

  return {
    params,
    setLimit: setParam("limit"),
    setMode: setParam("mode"),
    setKind: setParam("kind"),
  }
}

export function useYearRange(username: string) {
  return useQuery({
    queryKey: ["year-range"],
    queryFn: () => fetchYearRange(username)
  });
}