import { Box, Flex, List, Text as ChakraText, Link, VStack, Separator, } from "@chakra-ui/react";
import type { IconType } from "react-icons";
import { NavLink } from "react-router-dom";
import { useSidebarNav } from "./nav_sidebar_context";


export interface SidebarNavItem {
  icon: IconType;
  label: string;
  pathname: string;
}

export interface ExternalLinkItem {
  icon: IconType;
  label: string;
  href: string;
}

export interface SidebarNavItemsProps {
  navItems: SidebarNavItem[];
}

function sidebarItem(
  item: SidebarNavItem, index: number
) {

  const { open } = useSidebarNav();

  return (
    <List.Item key={index} listStyle={"none"}>
      <NavLink
        to={item.pathname}
        style={{ textDecoration: 'none', width: '100%' }}
      >
        {({ isActive }) => (
          <Box
            display="block"
            w="full"
            borderRadius="md"
            transition="all 0.2s"
            bg={isActive ? "accent" : "transparent"}
            color={isActive ? "white" : "inherit"}
            _hover={!isActive ? { bg: "bg.subtle" } : {}}
          >
            <Flex align="center" gap="4" px="3" py="2">
              <Box fontSize="20px"><item.icon /></Box>
              {open && (
                <ChakraText fontWeight="medium">{item.label}</ChakraText>
              )}
            </Flex>
          </Box>
        )}
      </NavLink>
    </List.Item>
  )
}


function ExternalItem(item: ExternalLinkItem, index: number) {

  const { open } = useSidebarNav();

  return (
    <List.Item key={index} listStyle={"none"}>
      <Link
        href={item.href}
        target="_blank"
        rel="noopener noreferrer"
        style={{ textDecoration: 'none', width: '100%' }}
      >
        <Box
          display="block"
          w="full"
          borderRadius="md"
          transition="all 0.2s"
          _hover={{ bg: "bg.subtle" }}
        >
          <Flex align="center" gap="4" px="3" py="2">
            <Box fontSize="20px"><item.icon /></Box>
            {open && (
              <ChakraText fontWeight="medium">{item.label}</ChakraText>
            )}
          </Flex>
        </Box>
      </Link>
    </List.Item>
  )
}

export default function SidebarNavItems(
  { navItems, externalLinks }: {
    navItems: SidebarNavItem[],
    externalLinks: ExternalLinkItem[]
  }
) {

  return (
    <VStack gap="6" h={"full"}>
      <List.Root gap="2" variant="plain" width="full">
        {navItems.map((item, index) =>
          sidebarItem(item, index)
        )}
      </List.Root>
      <Separator/>
      <List.Root gap="2" variant="plain" width="full">
        {externalLinks.map((item, index) =>
          ExternalItem(item, index)
        )}
      </List.Root>
    </VStack>
  );
}