import memoryfm as mfm

log = mfm.ScrobbleLog.from_json("sample_2.json")

filtered = log.filter_by_date(start="2024-05-09 4:00PM", end="2024-05-10 2:00AM")#.head()
tablefmt = "pipe"
file = "filter_2.md"
maxcolwidths = 4*[30]
filtered.to_markdown(file, tablefmt=tablefmt,
                     maxcolwidths=maxcolwidths,
                     newest_first=False)

