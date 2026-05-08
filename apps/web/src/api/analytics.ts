import { handleResponse } from "@/api/user";
import { getClientTimezone } from "@/api/tzhelper";
import type { KindType } from "@/typing";
import { BACKEND_URL } from "@/api/urls";

const alpha = 2;
const threshold = 1.5;
const min_length = 5;
const freq = "day";

export const fetchAttachmentMoments = async (
    { username, kind, from_ts, to_ts }: {
        username: string;
        kind: KindType;
        from_ts: string | null, // ISO 8601
        to_ts: string | null,// ISO 8601

    }
) => {
    const tz = getClientTimezone();

    const params = new URLSearchParams({
        kind,
        freq,
        alpha: String(alpha),
        threshold: String(threshold),
        tz
    });

    if (from_ts) {
        params.append("from_ts", from_ts);
    }

    if (to_ts) {
        params.append("to_ts", to_ts);
    }
    const res = await fetch(
        `${BACKEND_URL}/user/${username}/attachment_moments?${params.toString()}`
    );
    return handleResponse(res);
};

export const fetchAttachmentMomentsByPeriod = async (
    username: string, kind: string, period: number | "all_time"
) => {
    const tz = getClientTimezone();

    const params = new URLSearchParams({
        kind,
        period: String(period),
        freq,
        alpha: String(alpha),
        threshold: String(threshold),
        tz
    });


    const res = await fetch(
        `${BACKEND_URL}/user/${username}/attachment_moments_last?${params.toString()}`
    );
    return handleResponse(res);
}

export const fetchAttachmentIndex = async (
    { username, kind, from_ts, to_ts }: {
        username: string;
        kind: KindType;
        from_ts: string | null, // ISO 8601
        to_ts: string | null,// ISO 8601

    }
) => {
    const tz = getClientTimezone();

    const params = new URLSearchParams({
        kind,
        freq,
        alpha: String(alpha),
        tz
    });

    if (from_ts) {
        params.append("from_ts", from_ts);
    }

    if (to_ts) {
        params.append("to_ts", to_ts);
    }

    const res = await fetch(
        `${BACKEND_URL}/user/${username}/attachment?${params.toString()}`
    );
    return handleResponse(res);
}

export const fetchAttachmentIndexByPeriod = async (
    username: string, kind: string, period: number | "all_time"
) => {
    const tz = getClientTimezone();

    const params = new URLSearchParams({
        kind,
        period: String(period),
        freq,
        alpha: String(alpha),
        tz
    });

    const res = await fetch(
        `${BACKEND_URL}/user/${username}/attachment_last?${params.toString()}`
    );
    return handleResponse(res);
}

export const fetchStreaksByYear = async (
    username: string, kind: KindType, year: number
) => {
    const tz = getClientTimezone();

    const params = new URLSearchParams({
        kind,
        year: String(year),
        min_length: String(min_length),
        tz
    });

    const res = await fetch(
        `${BACKEND_URL}/user/${username}/streaks_yearly?${params.toString()}`
    );
    return handleResponse(res);
}