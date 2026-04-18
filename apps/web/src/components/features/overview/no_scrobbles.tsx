import { Alert, Box, Button, VStack } from "@chakra-ui/react";
import type { SyncStatus } from "@/api/sync";
import { useStartSync } from "@/hooks/use_start_sync";


export default function NoScrobbles(
    { username, syncStatus, isSyncActive}: {
        username: string,
        syncStatus: SyncStatus,
        isSyncActive: boolean,
    }
) {

    const startSync = useStartSync();

    async function handleClick() {
        await startSync(username);
    }

    const inProgress = syncStatus != null && syncStatus.status == "progress";
    const isCompleted = syncStatus?.status == "completed";

    const isLoadingSyncButton = 
        isSyncActive ||
        syncStatus?.status == "started" ||
        inProgress;
    
    const showWarning =
        !isSyncActive &&
        !inProgress &&
        !isCompleted;


    return (
    <VStack gap={"10"} width={"full"}>
        <Box width="sm">
            {showWarning && (
                <Alert.Root status={"warning"} title="Title">
                    <Alert.Indicator />
                    <Alert.Content>
                        <Alert.Description>
                            No Scrobbles found! Please sync scrobbles using the sync button below.
                        </Alert.Description>
                    </Alert.Content>
                </Alert.Root>
            )}
        </Box>
        <Button
            h="10"
            onClick={handleClick}
            loading={isLoadingSyncButton}
            loadingText="Syncing..."
        >
            Sync
        </Button>
    </VStack>
    )
} 
