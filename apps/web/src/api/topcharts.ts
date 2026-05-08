import { BACKEND_URL } from "@/api/urls";
import { handleResponse } from "@/api/user";
import { getClientTimezone } from "@/api/tzhelper";
import type { ChartsInput } from "@/typing";


export const fetchTopCharts = async (
    { username, kind, from_ts, to_ts, limit }: ChartsInput
) => {
    const tz = getClientTimezone();

    const params = new URLSearchParams({
        kind,
        tz,
        limit: String(limit)
    })

    if (from_ts) {
        params.append("from_ts", from_ts);
    }

    if (to_ts) {
        params.append("to_ts", to_ts);
    }

    const res = await fetch(
        `${BACKEND_URL}/user/${username}/top?${params.toString()}`
    );
    return handleResponse(res);
};