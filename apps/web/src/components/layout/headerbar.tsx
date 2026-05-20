import { Avatar, Box, Flex, IconButton, Menu, Portal, Text as ChakraText } from "@chakra-ui/react";
import { useStartSync } from "@/hooks/use_start_sync";
import { LuMenu } from "react-icons/lu";
import { useSidebarNav } from "@/components/layout/nav_sidebar/nav_sidebar_context";

export default function HeaderBar (
    { username}: { username: string }
) {
    const startSync = useStartSync();
    
    async function handleClick() {
        await startSync(username);
    }

    const { toggle } = useSidebarNav();

    return (
        <Flex
          as="header"
          align="center"
          boxShadow="md"
          direction="row"
          justify="space-between"
          h="16"
          width="100%"
          position={"sticky"}
          top={0}
          zIndex="sticky"
          bg={"bg.muted"}
          padding={5}
          py={{base: "4", md: "10"}}
        >
          <Flex align="center" gap="4">
            <IconButton 
              aria-label="Toggle Sidebar" 
              variant="ghost" 
              size="sm"
              onClick={toggle}
            >
              <LuMenu size="20px" />
            </IconButton>
            <Box>
              <ChakraText
                fontSize="4xl"
                fontWeight="bold"
                color="accent"
                lineHeight="1"
                letterSpacing={"tight"}
                >
                  memory.fm
              </ChakraText>
            </Box>
          </Flex>

          <Box>
            <Menu.Root positioning={{ placement: "bottom-end"}}>
              <Menu.Trigger rounded={"full"} focusRing={"outside"} >
                <Avatar.Root size={"lg"}>
                  <Avatar.Fallback name={username} textStyle="xl" /> 
                </Avatar.Root>
              </Menu.Trigger>
              <Portal>
                <Menu.Positioner>
                  <Menu.Content>
                    <Menu.ItemGroup>
                      <Menu.ItemGroupLabel fontSize={"md"} >{username}</Menu.ItemGroupLabel>
                    <Menu.Separator />
                    <Menu.Item
                      value="sync"
                      onClick={() => handleClick()}
                    >
                      Sync Scrobbles
                    </Menu.Item>
                    </Menu.ItemGroup>
                  </Menu.Content>
                </Menu.Positioner>
              </Portal>
            </Menu.Root>
          </Box>
        </Flex>
    )
}