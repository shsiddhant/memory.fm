import type { ListeningStreak } from "@/typing";
import { Alert, Flex, useBreakpointValue } from "@chakra-ui/react";
import type { Layout } from "plotly.js";
import Plotly from "plotly.js-dist";
import _createPlotlyComponent from 'react-plotly.js/factory';
import { useColorMode } from "@/components/ui/color-mode";
import { useMemo } from "react";


const createPlotlyComponent =
    (typeof _createPlotlyComponent === 'function')
        ? _createPlotlyComponent
        : (_createPlotlyComponent as any).default;

const Plot = createPlotlyComponent(Plotly);

export default function StreaksTimeline(
    { streaks }: { streaks: ListeningStreak[] }
) {

    const getChakraTokenValue = (tokenPath: string) => {
        const variableName = `--chakra-${tokenPath.replace(/\./g, '-')}`;
        const value = getComputedStyle(document.documentElement)
            .getPropertyValue(variableName)
            .trim();

        return value;
    };

    const { colorMode } = useColorMode();

    const colors = useMemo(() => ({
        colorScale: [
            [0.0, getChakraTokenValue("colors.brand.empty")],
            [0.3, getChakraTokenValue("colors.brand.c0")],
            [0.5, getChakraTokenValue("colors.brand.c1")],
            [0.7, getChakraTokenValue("colors.brand.c2")],
            [0.9, getChakraTokenValue("colors.brand.c3")],
            [1.0, getChakraTokenValue("colors.brand.c4")]
        ],
        fgColor: getChakraTokenValue("colors.fg.muted"),
    }), [colorMode]);

    const maxLogLength = Math.max(...streaks.map((d) => d.log_length));
    const maxPower = Math.floor(maxLogLength);
    //Tick vals
    const arr: number[] = Array.from({ length: maxPower + 1 }, (_, i) => i);

    // Format duration

    const fmtNumber = (value: number, name: string) => {
        return value > 1 ? `${value} ${name}s` : value > 0 ? `${value} ${name}` : "";
    }
    const formatDuration = (ms: number) => {
        const totalminutes = Math.trunc(ms / (60 * 1000));
        const minutes = totalminutes % 60;
        const totalhours = Math.trunc(totalminutes / 60);
        const hours = totalhours % 24;
        const days = Math.trunc(totalhours / 24);

        return `${fmtNumber(days, "day")} ${fmtNumber(hours, "hour")} ${fmtNumber(minutes, "minute")}`;
    };

    // Format Date
    const formatDate = (value: string | number | Date) => {
        return new Intl.DateTimeFormat(undefined, {
            year: "numeric",
            month: "short",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            hour12: true,
        }).format(new Date(value));
    };

    // Compute streak duration
    const transformed = streaks.map((d) => {
        const start = new Date(d.start);
        const end = new Date(d.end);
        return {
            ...d,
            startFormatted: formatDate(start),
            endFormatted: formatDate(end),
            duration: end.getTime() - start.getTime(),
            durationFormatted: formatDuration(end.getTime() - start.getTime()).trim(),
            subnameFormatted: d.subname ? `<i>${d.subname}</i><br>` : "",
        };
    });


    const data = [{
        type: "bar",
        orientation: "h",
        x: transformed.map((d) => d.duration),
        y: transformed.map(() => "streaks"),
        base: transformed.map((d) => new Date(d.start)),

        marker: {
            color: transformed.map((d) => d.log_length),
            colorscale: colors.colorScale,
            cmin: 0,
            cmax: maxLogLength,
            colorbar: {
                title: { text: "Streak Length" },
                orientation: "h",
                tickvals: arr,
                ticktext: arr.map((value) => 2 ** value)
            },
        },

        customdata: transformed as any,

        hovertemplate:
            "<b>%{customdata.name}</b><br>" +
            "%{customdata.subnameFormatted}" +
            "<br>Start: %{customdata.startFormatted}<br>" +
            "End: %{customdata.endFormatted}<br>" +
            "Duration: %{customdata.durationFormatted}<br>" +
            "Length: %{customdata.length}<extra></extra>",
    }];

    const chartWidth = useBreakpointValue({ md: 600, lg: 700, xl: 1000 });

    const layout: Partial<Layout> = {
        width: chartWidth,
        height: 300,
        margin: { l: 20, r: 20, t: 0, b: 40 },
        font: {
            family: "var(--chakra-fonts-body)",
            color: colors.fgColor,
        },
        xaxis: {
            type: "date",
            tickformat: "%d %b %Y",
            tickfont: { size: 14 },
            showgrid: false
        },
        yaxis: { visible: false },
        plot_bgcolor: "transparent",
        paper_bgcolor: "transparent",
    }

    const isWide = useBreakpointValue({ base: false, md: true, lg: true });

    return (
        <Flex justify={"center"}>
            {isWide ? (
                <Plot
                    data={data as any}
                    layout={layout}
                    config={{
                        responsive: true,
                        displayModeBar: false,
                    }}
                />) : (
                <Alert.Root status={"info"} width={{ base: "250px", md: "sm" }} justifySelf={"center"}>
                    <Alert.Indicator />
                    <Alert.Content textAlign={"left"}>
                        <Alert.Title>
                            To view the streaks timeline on smaller devices such as smartphones,
                            please rotate the screen to view in landscape mode.
                        </Alert.Title>
                    </Alert.Content>
                </Alert.Root>
            )
            }
        </Flex>
    );
}