import { BACKEND_URL } from "@/api/urls";
import { getClientTimezone } from "@/api/tzhelper";

export const handleResponse = async (res: Response) => {
  const data = await res.json();

  if (!res.ok) {
    const error: any = new Error();
    error.status = res.status;
    error.data = data;

    if (res.status === 422 && data.errors) {
      error.message = data.errors
        .map((err: { msg: string }) => `${err.msg}`)
        .join("\n");
    } else {
      throw new Error(data.message || "Request failed");
    }

    throw error;
  }

  return data;
};


export const ensureUser = async (username: string) => {
  const res = await fetch(
    `${BACKEND_URL}/user/${username}/ensure`,
    {
      method: "POST",
    }
  );
  return handleResponse(res);
}

export const syncUserScrobbles = async (username: string) => {
  const res = await fetch(
    `${BACKEND_URL}/user/${username}/sync`,
    {
      method: "POST",
    }
  );
  return handleResponse(res);
}

export const fetchUserSummary = async (username: string) => {
  const res = await fetch(`${BACKEND_URL}/user/${username}/summary`);
  return handleResponse(res);
};

export const fetchRecentActivity = async (username: string, weeks: number) => {
  const tz = getClientTimezone();

  const params = new URLSearchParams({
    weeks: String(weeks),
    tz
  });

  const res = await fetch(`${BACKEND_URL}/user/${username}/recent_scrobbles?${params.toString()}`);
  return handleResponse(res);
};

export const fetchTopChartsByPeriod = async (
  username: string,
  kind: string,
  period: number | "all_time",
  limit: number
) => {

  const tz = getClientTimezone();

  const params = new URLSearchParams({
    kind,
    period: String(period),
    limit: String(limit),
    tz
  });

  const res = await fetch(
    `${BACKEND_URL}/user/${username}/top_last?${params.toString()}`
  );
  return handleResponse(res);
};

export const fetchYearRange = async (username: string) => {
  const tz = getClientTimezone();

  const params = new URLSearchParams({
    tz
  })
  const res = await fetch(
    `${BACKEND_URL}/user/${username}/year_range?${params.toString()}`
  );
  return handleResponse(res);
};