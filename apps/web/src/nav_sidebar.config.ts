import { MdHome, MdListAlt } from "react-icons/md";
import type { SidebarNavItem } from "./components/nav_sidebar/nav_items";

export const useNavItems = (username: string): SidebarNavItem[] => [
    { icon: MdHome, label: "Home", pathname: "/"},
    { icon: MdListAlt, label: "Overview", pathname: `/user/${username}/overview` },
];