import { Avatar, Box, Flex, Menu, Portal, Text } from "@chakra-ui/react";
import "../App.css"

export default function HeaderBar (
    { username }: { username: string }
) {

    return (
        <Flex
            direction={"row"}
            boxShadow="md"
            justify={"space-between"}
            top={0}
            position={"sticky"}
            zIndex={"sticky"}
            bg={"bg.muted"}
            padding={5}
            mb={"10"}
            align="center"
        >
            <Box ml={5}>
                <Text fontSize={48} fontWeight="600" color="accent">
                    memory.fm
                </Text>
            </Box>
            <Box mr={5}>
                <Menu.Root positioning={{ placement: "bottom-end"}}>
                    <Menu.Trigger rounded={"full"} focusRing={"outside"} >
                        <Avatar.Root size={"lg"}>
                            <Avatar.Fallback name={username} textStyle="xl" /> 
                        </Avatar.Root>
                    </Menu.Trigger>
                    <Portal>
                        <Menu.Positioner>
                            <Menu.Content>
                                <Menu.Item value="sync">Sync Scrobbles</Menu.Item>
                            </Menu.Content>
                        </Menu.Positioner>
                    </Portal>
                </Menu.Root>
            </Box>
        </Flex>
    )
}