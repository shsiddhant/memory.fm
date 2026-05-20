import type { TimeSeries } from "@/typing"
import { Chart, useChart } from "@chakra-ui/charts"
import { useBreakpointValue } from "@chakra-ui/react";
import { Line, LineChart, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts"

export default function AttachmentGraph(
    { data }: { data: TimeSeries }
) {
    const chart = useChart({ data });

    const chartWidth = useBreakpointValue({ base: 300, md: 500, lg: 700, xl: 1000 });
    const fontSize = useBreakpointValue({ base: "12px", md: "13px" });
    const lableFontSize = useBreakpointValue({ base: "13px", md: "15px" });
    const labelStyleProps = { fontSize: lableFontSize, fontWeight: "bold" };

    return (
        <Chart.Root chart={chart} mt={"6"}>
            <LineChart data={data} width={chartWidth} height={500}>
                <CartesianGrid vertical={false} />
                <XAxis
                    dataKey={"day"}
                    label={{ value: "DATE", position: "bottom", style: labelStyleProps }}
                    interval="preserveStartEnd"
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(day) => new Date(day).toLocaleDateString(
                        "en-US", { month: "short", day: "2-digit", year: "numeric" }
                    )}
                    tick={{ style: { fontSize: fontSize } }}
                    tickMargin={5}
                    minTickGap={30}
                />
                <YAxis
                    label={{
                        value: "ATTACHMENT INDEX",
                        position: "left",
                        angle: -90,
                        style: labelStyleProps
                    }}
                    axisLine={false}
                />
                <Tooltip
                    animationDuration={100}
                    cursor={false}
                    content={<Chart.Tooltip />}
                    labelFormatter={(label) => chart.formatDate({ dateStyle: "medium" })(String(label))}
                    formatter={(value: any) => {
                        const numericValue = typeof value === 'number' ? value.toFixed(2) : 0;
                        return [numericValue, "Attachment Index:"];
                    }}
                />

                <Line
                    dataKey="value"
                    stroke={chart.color("accent")}
                    dot={false}
                    strokeWidth={2}
                />
            </LineChart>
        </Chart.Root>

    )
}
