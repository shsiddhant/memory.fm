import { useEffect, useState } from "react";

// Data API
import { fetchTopCharts } from "@/api/topcharts";

import { Box, Flex, parseDate, Text as ChakraText, type DateValue, VStack, Alert } from "@chakra-ui/react";
//import Section from "@/components/ui/section";
import { fetchTopChartsByPeriod } from "@/api/user";
import PeriodSelector from "@/components/features/analytics/periodselector";
import type { Dates, TopChart } from "@/typing";
import { useParams } from "react-router-dom";
import KindSelector from "../features/analytics/kindselector";
import useAnalyticsParams from "@/hooks/use_analytics_params";
import LimitSelector from "../features/analytics/limitselector";
import TopChartsTable from "../features/topcharts/topcharts_table";
import Section from "../ui/section";

// Top Charts Page


export default function TopChartsPage() {

    const { username } = useParams();
    const [loading, setLoading] = useState(false);
    const { params, setLimit, setMode, setKind } = useAnalyticsParams({
        limit: 10,
        mode: 30,
        kind: "track",
    });

    const [customDates, setCustomDates] = useState<Dates>({
        from_ts: parseDate(new Date()),
        to_ts: parseDate(new Date())
    });
    const [data, setData] = useState<TopChart[]>();
    if (!username?.trim()) {
        return null;
    }

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            try {
                let result: TopChart[];
                if (params.mode == "custom") {
                    result = await fetchTopCharts({
                        username: username,
                        kind: params.kind,
                        from_ts: customDates.from_ts.toString(),
                        to_ts: customDates.to_ts.toString(),
                        limit: params.limit,
                    });
                }
                else {
                    result = await fetchTopChartsByPeriod(
                        username, params.kind, params.mode, params.limit,
                    )
                }

                setData(result);
            } catch (error) {
                console.error("Failed to load charts", error);
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [params, customDates]);


    const handleDateChange = (key: keyof Dates, newValues: DateValue[]) => {
        const selectedDate = newValues[0];
        if (selectedDate) {
            setCustomDates((prev) => ({
                ...prev,
                [key]: selectedDate
            }));
        }
    }

    if (!data) {
        return <ChakraText>No Data Found</ChakraText>
    }


    console.log("Data:", data[0])
    return (
        <Flex
            direction="column"
            gap={4}
        >
            <Box mt={"4"}>
                <KindSelector value={params.kind} onKindChange={setKind} />
            </Box>
            <Flex
                justify="space-around"
                wrap="wrap"
                gap={4}
                padding={"4"}
                mx={"12"}
                mt={"4"}
            >
                <VStack align="center" gap={"4"} px="6" py="3">
                    <ChakraText
                        fontSize={"lg"}
                        fontWeight={"bold"}
                    >Period</ChakraText>
                    <PeriodSelector
                        mode={params.mode}
                        onModeChange={setMode}
                        customDates={customDates}
                        onDatesChange={handleDateChange}
                    />
                </VStack>
                <VStack align={"center"} gap={"4"} padding={"6"}>
                    <ChakraText
                        fontSize={"lg"}
                        fontWeight={"bold"}
                    >Limit</ChakraText>
                    <LimitSelector
                        min={5}
                        value={params.limit}
                        onLimitChange={setLimit}
                    />
                </VStack>
            </Flex>
            {(!loading && data.length > 0) ? (
                <>
                <Section
                title={`Top ${params.kind}s`}
                children={<TopChartsTable kind={params.kind} topCharts={data} pageSize={8}/>}
                />
                </>
            ) : (loading) ? (
                <div>Loading...</div>
            ): (
                <Flex justify={"center"}>
                <Alert.Root status={"info"} width={"sm"} justifySelf={"center"}>
                    <Alert.Indicator />
                    <Alert.Content>
                        <Alert.Title>No scrobbles found in the selected period.</Alert.Title>
                    </Alert.Content>
                </Alert.Root>
                </Flex>
            )}
        </Flex>
    )
}