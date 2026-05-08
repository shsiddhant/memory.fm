export const getClientTimezone = () =>
  Intl.DateTimeFormat().resolvedOptions().timeZone || "Etc/UTC";