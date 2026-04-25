const BACKEND_URL = "http://127.0.0.1:8000";
import { handleResponse } from "@/api/user";
import type { KindType } from "@/typing";

const alpha = 2;
const threshold = 1.5;

export const fetchAttachmentMoments = async(
    { username, kind, from_ts, to_ts }: {
        username: string;
        kind: KindType;
        from_ts: string | null, // ISO 8601
        to_ts: string | null,// ISO 8601

    }
) => {
    const res = await fetch(
        `${BACKEND_URL}/user/${username}/attachment_moments?kind=${kind}&from_ts=${from_ts}&to_ts=${to_ts}&freq=day&alpha=${alpha}&threshold=${threshold}`
    );
    return handleResponse(res);
};

export const fetchAttachmentMomentsByPeriod = async (
    username: string, kind: string, period: number | "all_time"
) => {
    const res = await fetch(
        `${BACKEND_URL}/user/${username}/attachment_moments_last?kind=${kind}&period=${period}&freq=day&alpha=${alpha}&threshold=${threshold}`
    );
    return handleResponse(res);
}

export const fetchAttachmentIndex = async(
    { username, kind, from_ts, to_ts }: {
        username: string;
        kind: KindType;
        from_ts: string | null, // ISO 8601
        to_ts: string | null,// ISO 8601

    }
) => {
    const res = await fetch(
        `${BACKEND_URL}/user/${username}/attachment?kind=${kind}&from_ts=${from_ts}&to_ts=${to_ts}&freq=day&alpha=${alpha}`
    );
    return handleResponse(res);
}

export const fetchAttachmentIndexByPeriod = async (
    username: string, kind: string, period: number | "all_time"
) => {
    const res = await fetch(
        `${BACKEND_URL}/user/${username}/attachment_last?kind=${kind}&period=${period}&freq=day&alpha=${alpha}`
    );
    return handleResponse(res);
}