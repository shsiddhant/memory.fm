import { Alert, Box, Button, VStack } from "@chakra-ui/react";
import { syncUserScrobbles } from "@/api/user";
import type { SyncStatus } from "@/api/sync";


export default function NoScrobbles(
    { username, syncStatus, hasStartedSync, onSync }: {
        username: string,
        syncStatus: SyncStatus,
        hasStartedSync: boolean,
        onSync: (hasStartedSync: boolean) => void
    }
) {

    async function handleClick() {
        await syncUserScrobbles(username);
        onSync(true);
    }

    const inProgress = syncStatus != null && syncStatus.status == "progress" 
    const isCompleted = syncStatus?.status == "completed";

    const isLoadingSyncButton = 
        hasStartedSync ||
        syncStatus?.status == "started" ||
        inProgress;
    
    const showWarning =
        !hasStartedSync &&
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
