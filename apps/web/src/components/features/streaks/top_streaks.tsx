import type { ListeningStreak } from "@/typing";
import { Box, Card, Flex, Text as ChakraText, Badge, Alert, useBreakpointValue, Stack } from "@chakra-ui/react";

function topStreaksByLength(streaks: ListeningStreak[], count: number) {

    const sortedStreaks = streaks.sort((a, b) => b.length - a.length);
    return sortedStreaks.slice(0, count);
}

function StreakCard(streak: ListeningStreak) {

    const { start, end } = streak;

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
    const startDate = new Date(streak.start);
    const endDate = new Date(streak.end);

    const transformedStreak = {
        ...streak,
        startFormatted: formatDate(start),
        endFormatted: formatDate(end),
        duration: endDate.getTime() - startDate.getTime(),
        durationFormatted: formatDuration(endDate.getTime() - startDate.getTime()),
        subnameFormatted: streak.subname ? `${streak.subname}` : "",
    };

    return (
        <>
            <Box w={{ base: "240px", md: "240px" }}>
                <Card.Root
                    variant="outline"
                    _hover={{ bg: "bg.muted" }}
                    transition="0.2s"
                    padding={4}
                >
                    <Flex justify="space-between" align="center">
                        <Stack gap={"1"}>
                            <ChakraText fontWeight="bold">
                                {transformedStreak.name}
                            </ChakraText>
                            {transformedStreak.subnameFormatted && (
                                <ChakraText fontSize="sm" fontStyle="italic" color="fg">
                                    {transformedStreak.subnameFormatted}
                                </ChakraText>
                            )}
                            <ChakraText fontWeight={"bold"} fontSize={"sm"} color={"accent"}>
                                {transformedStreak.length} Scrobbles
                            </ChakraText>
                            <Badge colorPalette={"brand"} mt={2} variant="surface" size={{ base: "sm", md: "md" }}>
                                {transformedStreak.durationFormatted}
                            </Badge>
                            <Badge bg="bg.muted" mt={2} variant="surface" size={{ base: "sm", md: "md" }}>
                                Start: {transformedStreak.startFormatted}
                            </Badge>
                            <Badge bg="bg.muted" mt={1} variant="surface" size={{ base: "sm", md: "md" }}>
                                End: {transformedStreak.endFormatted}
                            </Badge>
                        </Stack>
                    </Flex>
                </Card.Root>
            </Box>
        </>
    )

}

function groupCards(streaks: ListeningStreak[], size: number) {
    const groups = [];

    for (let i = 0; i < streaks.length; i += size) {
        groups.push(streaks.slice(i, i + size));
    }

    return groups;
}

function StreakGroup(group: ListeningStreak[]) {
    return (
        <Flex
            direction={{ base: "column", md: "row" }}
            gap="10"
            w={"full"}
        >
            {group.map((s) => (
                StreakCard(s)
            ))}
        </Flex>
    )
}

export default function TopStreaks(
    { streaks }: { streaks: ListeningStreak[] }
) {

    if (streaks.length === 0) {
        <Flex justify={"center"}>
            <Alert.Root status={"info"} width={{ base: "250px", md: "sm" }} justifySelf={"center"}>
                <Alert.Indicator />
                <Alert.Content textAlign={"left"}>
                    <Alert.Title>No streaks found in the selected period.</Alert.Title>
                </Alert.Content>
            </Alert.Root>
        </Flex>
    }

    const topStreaks = topStreaksByLength(streaks, 8);
    const groupSize = useBreakpointValue({ base: 1, md: 2, lg: 3, xl: 4 });
    const groups = groupCards(topStreaks, groupSize || 1);

    return (
        <Flex
            gap={{ base: 8, md: 12 }}
            mt={6}
            direction="column"
            justify={"center"}
        >
            {groups.map((g) => (
                StreakGroup(g)
            ))}
        </Flex>
    )
}