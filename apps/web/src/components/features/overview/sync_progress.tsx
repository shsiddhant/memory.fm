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
                <Box w={"md"}>
                    <Alert.Root status={"error"} title="Sync Error">
                        <Alert.Indicator />
                        <Alert.Content>
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
            align="center"
            alignItems={"center"}
        >
            <Progress.Root
                value={progressPercent}
                width="sm"
            >
                <HStack gap={"5"}>
                    <Progress.Label>Syncing scrobbles...</Progress.Label>
                    <Progress.Track flex="1" height="2">
                        <Progress.Range />
                    </Progress.Track>
                    <Progress.ValueText>
                        {progressPercent.toPrecision(3)}%
                    </Progress.ValueText>
                </HStack>
            </Progress.Root>
        </Flex>
    )
}
