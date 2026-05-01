import { BACKEND_URL } from "@/api/urls";


export const handleResponse = async (res: Response) => {
  const data = await res.json();

  if (!res.ok) {
    if (res.status === 422 && data.errors) {
      const errorMessages = data.errors
        .map((err: { msg: string }, i: number) => `${i} - ${err.msg}`)
        .join(", ");

      throw new Error(errorMessages);
    }

    throw new Error(data.message || "Request failed");
  }

  return data;
};


export const ensureUser = async (username: string) => {
  const res = await fetch(
    `${BACKEND_URL}/user/${username}/ensure/`,
    {
      method: "POST",
    }
  );
  return handleResponse(res);
}

export const syncUserScrobbles = async (username: string) => {
  const res = await fetch(
    `${BACKEND_URL}/user/${username}/sync/`,
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
  const res = await fetch(`${BACKEND_URL}/user/${username}/recent_scrobbles?weeks=${weeks}`);
  return handleResponse(res);
};

export const fetchTopChartsByPeriod = async (
  username: string, kind: string, period: number | "all_time", limit: number
) => {
  const res = await fetch(
    `${BACKEND_URL}/user/${username}/top_last?kind=${kind}&period=${period}&limit=${limit}`
  );
  return handleResponse(res);
};

export const fetchYearRange = async (username: string) => {
  const res = await fetch(
    `${BACKEND_URL}/user/${username}/year_range`
  );
  return handleResponse(res);
};