import { Outlet, useParams } from "react-router-dom";

// Hooks
import { useNavItems, useExternalLinks } from "@/components/layout/nav_sidebar/nav_sidebar.config";

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
  const externalLinks = useExternalLinks();

  const { open } = useSidebarNav();
  const mobileWidth = open ? "260px" : "52px";
  const mdWidth = open ? "260px" : "72px";
  const sidebarWidth = { base: mobileWidth, md: mdWidth };
  const topPosition = { base: "64px", md: "80px" }

  const dynamicHeight = {
    base: `calc(100vh - ${topPosition.base})`,
    md: `calc(100vh - ${topPosition.md})`
  };

  return (
    <Flex minH={"100vh"} direction={"column"}>

      {/* Headerbar */}
      <HeaderBar username={username!} />

      {/* Sidebar */}
      <Flex flex="1">
        <Box
          w={sidebarWidth}
          bg="bg.muted"
          boxShadow={"md"}
          position="sticky"
          zIndex="docked"
          top={topPosition}
          h={dynamicHeight}

        >
          <SidebarNav navItems={navItems} externalLinks={externalLinks} />
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
    </Flex >
  );
}