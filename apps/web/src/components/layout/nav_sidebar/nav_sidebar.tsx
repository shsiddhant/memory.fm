import { Box, Stack} from "@chakra-ui/react";
import SidebarNavItems from "./nav_items";
import type { SidebarNavItemsProps } from "./nav_items";


export default function SidebarNav(
    { navItems }: SidebarNavItemsProps
) {
    return (
        <Box
          as="nav"
          w="full"
          h="full"
          bg="bg.muted"
          borderRightWidth="1px"
          borderColor="border.subtle"
          transition="all 0.2s ease"
          overflowX="hidden"
        >
          <Stack p={"4"} gap={"4"}>
            <SidebarNavItems navItems={navItems} />
          </Stack>
        </Box>
    )
}