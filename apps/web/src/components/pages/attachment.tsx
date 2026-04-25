import { useEffect, useState } from "react";

// Data API
import { fetchAttachmentMoments, fetchAttachmentMomentsByPeriod } from "@/api/analytics";

import { Box, Flex, parseDate, Text as ChakraText, type DateValue, VStack, Alert } from "@chakra-ui/react";
import Section from "@/components/ui/section";
import PeriodSelector from "@/components/features/analytics/periodselector";
import type { AttachmentMoment, Dates } from "@/typing";
import { useParams } from "react-router-dom";
import KindSelector from "../features/analytics/kindselector";
import useAnalyticsParams from "@/hooks/use_analytics_params";
import AttachmentTimeline from "@/components/features/attachment/attachment_moments";


// Attachment Page


export default function AttachmentPage() {

    const { username } = useParams();

    const [loading, setLoading] = useState(false);
    const { params, setMode, setKind } = useAnalyticsParams({
        limit: 10,
        mode: 30,
        kind: "artist",
    });

    const [customDates, setCustomDates] = useState<Dates>({
        from_ts: parseDate(new Date()),
        to_ts: parseDate(new Date())
    });
    const [data, setData] = useState<AttachmentMoment[]>();
    if (!username?.trim()) {
        return null;
    }

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            try {
                let result: AttachmentMoment[];
                if (params.mode == "custom") {
                    result = await fetchAttachmentMoments({
                        username: username,
                        kind: params.kind,
                        from_ts: customDates.from_ts.toString(),
                        to_ts: customDates.to_ts.toString(),
                    });
                }
                else {
                    result = await fetchAttachmentMomentsByPeriod(
                        username, params.kind, params.mode,
                    )
                }

                setData(result);
            } catch (error) {
                console.error("Failed to load moments", error);
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
            </Flex>
            {(!loading && data.length > 0) ? (
                <>
                    <Section
                        title={`Top Attachment Moments - ${params.kind}s`}
                        children={<AttachmentTimeline moments={data} />}
                    />
                </>
            ) : (loading) ? (
                <div>Loading...</div>
            ) : (
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

