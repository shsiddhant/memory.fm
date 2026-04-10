import { ResponsiveTimeRange} from "@nivo/calendar";
import { useToken } from "@chakra-ui/react";

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
        <div style={{ height: 250, width: 500 }}>
        <ResponsiveTimeRange
        data={counts}
        from={`${from_date}T00:00:00`}
        to={`${to_date}T23:59:59`}
        emptyColor={ emptyColor }
        colors={ [c0, c1, c2, c3, c4] }
        maxValue={"auto"}
        minValue={0}
        margin={{ top: 0, right: 20, bottom: 20, left: 20 }}
        dayBorderColor=""
        daySpacing={3}
        dayRadius={5}
        
        />
        </div>
    )
}