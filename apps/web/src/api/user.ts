const BASE_URL = "http://127.0.0.1:8000";

export const fetchUserSummary = async (username: string) => {
  const res = await fetch(`${BASE_URL}/user/${username}/summary`);
  if (!res.ok) throw new Error("User summary not found");
  return res.json();
};

export const fetchRecentActivity = async (username: string, weeks: number) => {
  const res = await fetch(`${BASE_URL}/user/${username}/recent_scrobbles?weeks=${weeks}`);
  if (!res.ok) throw new Error("Activity not found");
  return res.json();
};

export const fetchTopCharts = async (
  username: string, kind: string, period: number | "all_time", limit: number
) => {
  const res = await fetch(
    `${BASE_URL}/user/${username}/top?kind=${kind}&period=${period}&limit=${limit}`
  );
  if (!res.ok) throw new Error("Top charts not found");
  return res.json();
};