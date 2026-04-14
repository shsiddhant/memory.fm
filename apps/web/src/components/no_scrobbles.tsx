import { Alert, Box, Button, VStack } from "@chakra-ui/react";

export default function NoScrobbles() {
    return (
    <VStack gap={"10"}>
        <Box>
            <Alert.Root status={"warning"} title="Title">
                <Alert.Indicator />
                <Alert.Content>
                    <Alert.Description>
                        No Scrobbles found! Please sync scrobbles using the sync button below.
                    </Alert.Description>
                </Alert.Content>
            </Alert.Root>
        </Box>
        <Button h="10" width={"-moz-fit-content"}>Sync</Button>
    </VStack>
    )
} 
