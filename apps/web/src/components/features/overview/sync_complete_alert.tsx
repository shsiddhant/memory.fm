import { Alert, CloseButton, Flex } from "@chakra-ui/react"

export default function SyncCompleteAlert(
    { fetched, onClose }: {
        fetched: number | null
        onClose: () => void
    }
) {
    return (
        <Flex
            direction={"column"}
            padding={{base: 2, md: 5 }}
            mb={"6"}
            align="center"
            alignItems={"center"}
        >
            <Alert.Root status={"info"} width={{ base: "250px", md: "xs"}}>
                <Alert.Indicator />
                <Alert.Content>
                    <Alert.Title>Fetched {fetched! - 1} scrobble{fetched! != 1 ? "s" : ""}</Alert.Title>
                </Alert.Content>
                <CloseButton
                    position="absolute"
                    right="-1"
                    top="1"
                    onClick={() => onClose()} />
            </Alert.Root>
        </Flex>
    )
}