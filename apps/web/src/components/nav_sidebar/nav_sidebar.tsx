import { Drawer } from "@chakra-ui/react";
import SidebarNavItems from "./nav_items";
import type { SidebarNavItemsProps } from "./nav_items";
import { useSidebarNav } from "./nav_sidebar_context";


export default function SidebarNav(
    { navItems }: SidebarNavItemsProps
) {
    const { open, onToggle } = useSidebarNav();
    return (
        <>
            <Drawer.Root
                open={open}
                onOpenChange={onToggle}
            >
                <Drawer.Backdrop />
                <Drawer.Positioner>
                    <Drawer.Content>
                        <Drawer.Header>
                            <Drawer.Title color={"accent"}></Drawer.Title>
                        </Drawer.Header>
                        <Drawer.Body>
                            <SidebarNavItems navItems={navItems} />
                        </Drawer.Body>
                    </Drawer.Content>
                </Drawer.Positioner>
            </Drawer.Root> 
        </>
    )
}