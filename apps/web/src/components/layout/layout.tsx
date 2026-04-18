import { Outlet, useParams } from "react-router-dom";

// Hooks
import { useNavItems } from "@/components/layout/nav_sidebar/nav_sidebar.config";

// Components
// Chakra UI
import { Box, Flex } from "@chakra-ui/react";
// Custom components
import SidebarNav from "@/components/layout/nav_sidebar/nav_sidebar";
import { useSidebarNav } from "@/components/layout/nav_sidebar/nav_sidebar_context";
import HeaderBar from "@/components/layout/headerbar"

export default function AppLayout() {
  const { username } = useParams();

  if (!username?.trim()) {
    return null;
    }

  const navItems = useNavItems(username);

  const { open } = useSidebarNav();
  const sidebarWidth = open ? "260px" : "72px";

  return (
      <Flex minH={"100vh"} direction={"column"}>

        {/* Headerbar */}
        <HeaderBar username={username!} />
        
        {/* Sidebar */}
        <Flex flex="1" overflow={"hidden"}>
          <Box
            w={sidebarWidth}
            bg="bg.muted"
            boxShadow={"md"}
          >
            <SidebarNav navItems={navItems}/>
          </Box>
          
        <Box 
            as="main" 
            flex="1" 
            ml={0} 
            p="6" 
            transition="margin-left 0.2s"
          >
            <Outlet />
          </Box>
          </Flex>
        </Flex>
  );
}