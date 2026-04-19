import { useState } from "react"
import { type AnalyticsParams } from "@/typing"

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