import { List, Link } from "@chakra-ui/react";
import type { IconType } from "react-icons";
import { NavLink } from "react-router-dom";


export interface SidebarNavItem {
  icon: IconType;
  label: string;
  pathname: string;
}

export interface SidebarNavItemsProps {
  navItems: SidebarNavItem[];
}

function sidebarItem(
    item: SidebarNavItem, index: number
) {
  return (
    <List.Item key={index}>
      <List.Indicator asChild>
        <item.icon />
      </List.Indicator>
      <Link
        display={"block"}
        as={NavLink}
        href={item.pathname}
        _focus={{ bg: "gray.100" }}
        _hover={{
          bg: "gray.200"
        }}
        _active={{ bg: "orange.500", color: "white" }}
        w="full"
        borderRadius="md"
        >
          {item.label}
      </Link>
    </List.Item>
  )
}


export default function SidebarNavItems (
  {navItems} : SidebarNavItemsProps
) {
  return (
    <List.Root
      gap="2"
      variant={"plain"}
      >
        {navItems.map(
          (item, index) => sidebarItem(item, index)
        )}
      </List.Root>
  )
}