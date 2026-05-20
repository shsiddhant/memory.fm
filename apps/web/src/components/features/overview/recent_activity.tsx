import { ResponsiveTimeRange } from "@nivo/calendar";
import { Box, useBreakpointValue, useToken } from "@chakra-ui/react";

interface ScrobblesCount {
    day: string,
    value: number
}

interface RecentActivityObject {
    from_date: string;
    to_date: string;
    counts: ScrobblesCount[]
}

export default function RecentActivity(
    { from_date, to_date, counts }: RecentActivityObject
) {

    const chartWidth = useBreakpointValue({ base: 300, md: 600 });
    const margin = useBreakpointValue({ base: 0, md: 20 });
    const radius = useBreakpointValue({ base: 3, md: 5 });
    const chartHeight = useBreakpointValue({ base: 200, md: 250});

    const theme = {
        labels: {
            text: {
                fontSize: "var(--chakra-font-sizes-sm)",
                fill: "var(--chakra-colors-fg-muted)",
                fontFamily: "var(--chakra-fonts-body)",
                fontWeight: "500",
            },
        },

        tooltip: {
            container: {
                fontFamily: "var(--chakra-fonts-body)",
                fontSize: "var(--chakra-font-sizes-sm)",
                background: "var(--chakra-colors-bg-panel)",
                color: "var(--chakra-colors-fg-muted)",
            },
        },
    };

    const [emptyColor, c0, c1, c2, c3, c4] = useToken(
        "colors.activityColors", [
        "empty",
        "c0",
        "c1",
        "c2",
        "c3",
        "c4"
    ]
    )
    return (
        <Box height={chartHeight} width={chartWidth}>
            <ResponsiveTimeRange
                data={counts}
                theme={theme}
                from={`${from_date}T00:00:00`}
                to={`${to_date}T23:59:59`}
                emptyColor={emptyColor}
                colors={[c0, c1, c2, c3, c4]}
                maxValue={"auto"}
                minValue={0}
                margin={{ top: 40, right: margin, bottom: 0, left: margin }}
                dayBorderColor=""
                daySpacing={3}
                dayRadius={radius}
                monthLegendOffset={20}
                monthLegend={(_year, _month, date) => `${date.toLocaleDateString("default", { month: "short" })}`}
                weekdayTicks={[1, 3, 5]}
                weekdays={["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]}
                weekdayLegendOffset={40}
            />
        </Box>
    )
}