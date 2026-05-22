import { Alert, Box, Flex, HStack, Progress, VStack } from "@chakra-ui/react";
import type { SyncStatus } from "@/api/sync";


export default function SyncProgress(
    { syncStatus }: { syncStatus: SyncStatus }
) {


    if (!syncStatus) return null;

    if (syncStatus?.status == "error") {
        return (
            <VStack mb={6}
            >
                <Box w={{ base: "xs", md: "md" }}>
                    <Alert.Root status={"error"} title="Sync Error">
                        <Alert.Indicator />
                        <Alert.Content textAlign={"left"}>
                            <Alert.Description>
                                Sync failed: {syncStatus.error || "Unexpected Error."}
                            </Alert.Description>
                        </Alert.Content>
                    </Alert.Root>
                </Box>
            </VStack>
        )
    }

    if (!syncStatus?.page || !syncStatus?.totalpages) {
        return (
            <div> Syncing scrobbles...</div>
        )
    }

    const progressPercent =
        (
            syncStatus.status === "started" ||
            syncStatus.total_scrobbles == 0
        ) ? 0
            : syncStatus.status == "completed" ? 100
                : (syncStatus.page / syncStatus.totalpages) * 100;


    return (
        <Flex
            direction={"column"}
            padding={5}
            mb={"6"}
            gap={"6"}
            align="center"
            alignItems={"center"}
        >
            <Progress.Root
                value={progressPercent}
                width={{ base: "250px", md: "xl" }}
            >
                <HStack gap={"5"}>
                    <Progress.Label>Syncing...</Progress.Label>
                    <Progress.Track flex="1" height={{ base: 1, md: 2 }}>
                        <Progress.Range />
                    </Progress.Track>
                    <Progress.ValueText>
                        {progressPercent.toPrecision(3)}%
                    </Progress.ValueText>
                </HStack>
                <Progress.Label mt={2}>
                    Fetched {syncStatus.fetched_scrobbles?.toLocaleString()} of {syncStatus.total_scrobbles?.toLocaleString()} scrobbles
                </Progress.Label>
            </Progress.Root>
            <Alert.Root status={"info"} width={{ base: "auto", md: "md" }} justifySelf={"center"}>
                <Alert.Indicator />
                <Alert.Content textAlign={"left"}>
                    <Alert.Title>First sync may take some time for large listening histories.</Alert.Title>
                    <Alert.Description> While your scrobbles
                        sync, you can still view your stats and charts using the sidebar.
                        .</Alert.Description>
                </Alert.Content>
            </Alert.Root>
        </Flex>
    )
}
