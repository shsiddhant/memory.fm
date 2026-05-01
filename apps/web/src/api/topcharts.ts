import { BACKEND_URL } from "@/api/urls";
import { handleResponse } from "@/api/user";
import type { ChartsInput } from "@/typing";


export const fetchTopCharts = async (
    { username, kind, from_ts, to_ts, limit }: ChartsInput
) => {
    const res = await fetch(
        `${BACKEND_URL}/user/${username}/top?kind=${kind}&from_ts=${from_ts}&to_ts=${to_ts}&limit=${limit}`
    );
    return handleResponse(res);
};