import { Alert, CloseButton, Flex } from "@chakra-ui/react"

export default function SyncCompleteAlert(
    { fetched, onClose }: {
        fetched: number | null
        onClose: () => void
    }
) {

    const formatFetched = (fetched: number | null) => {
        if (fetched! <= 1) {
            return 0;
        } else if (fetched! > 1) {
            return fetched!;
        }
    };

    const fetchedFormatted = formatFetched(fetched);
    const formattedTitle = `Fetched ${fetchedFormatted} scrobble${fetchedFormatted != 1 ? "s" : ""}`;

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
                <Alert.Content textAlign={"left"}>
                    <Alert.Title>{formattedTitle}</Alert.Title>
                </Alert.Content>
                <CloseButton
                    position="absolute"
                    right="1"
                    top="1"
                    onClick={() => onClose()} />
            </Alert.Root>
        </Flex>
    )
}