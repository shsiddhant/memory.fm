import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchStreaksByYear } from "@/api/analytics";
import { useQuery } from "@tanstack/react-query";
import useAnalyticsParams, { useYearRange } from "@/hooks/use_analytics_params";

import type { ListeningStreak, PageHeaderProps } from "@/typing";

import { Box, Flex, Text as ChakraText, VStack, Alert } from "@chakra-ui/react";
import SliderSelector from "@/components/features/analytics/sliderselector";
import KindSelector from "@/components/features/analytics/kindselector";
import StreaksTimeline from "@/components/features/streaks/streaks_timeline";
import Section from "../ui/section";
import { LoadingSpinner } from "../ui/loading";
import { MdBolt } from "react-icons/md";
import PageHeader from "../ui/page-header";


export default function StreaksPage() {

    const { username } = useParams();
    if (!username?.trim()) {
        return null;
    }

    const { data, isLoading, isError } = useYearRange(username);
    const [year, setYear] = useState<number>();
    const { params, setKind } = useAnalyticsParams({
        limit: 10,
        mode: 30,
        kind: "artist",
    });

    useEffect(() => {
        if (data && year == null) {
            setYear(data.end);
        }
    }, [data, year]);

    const streaksQuery = useQuery({
        queryKey: ["streaks", params.kind, year],
        queryFn: () => fetchStreaksByYear(username, params.kind, year!),
        enabled: !!year
    });

    if (isLoading) {
        return <LoadingSpinner />
    }

    if (isError) {
        return (
            <Flex justify={"center"}>
                <Alert.Root status={"info"} width={"sm"} justifySelf={"center"}>
                    <Alert.Indicator />
                    <Alert.Content>
                        <Alert.Title>No scrobbles found.</Alert.Title>
                    </Alert.Content>
                </Alert.Root>
            </Flex>
        )
    }

    const streaks: ListeningStreak[] = streaksQuery.data || []

    const page: PageHeaderProps = {
        title: "Streaks",
        icon: MdBolt,
        info: "A Streak is a series of consecutive listens of the same artist, album, or track."
    };

    return (
        <Flex
            direction="column"
            gap={4}
        >
            {PageHeader(page)}
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
                    >Year</ChakraText>
                    <SliderSelector
                        value={year!}
                        min={data.start}
                        max={data.end}
                        onValueChange={(value) => setYear(value)}
                    />
                </VStack>
            </Flex>
            {(!isLoading) && (
                <Section
                    title={`Streaks timeline - ${params.kind}s`}
                >
                    <StreaksTimeline
                        streaks={streaks}
                    />
                </Section>
            )}
        </Flex>
    )
}
