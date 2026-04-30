import { MdBarChart,  MdBolt,  MdFavorite,  MdHome, MdListAlt } from "react-icons/md";
import type { SidebarNavItem } from "./nav_items";

export const useNavItems = (username: string): SidebarNavItem[] => [
    { icon: MdHome, label: "Home", pathname: "/"},
    { icon: MdListAlt, label: "Overview", pathname: `/user/${username}/overview` },
    { icon: MdBarChart, label: "Top Charts", pathname: `/user/${username}/topcharts`},
    { icon: MdFavorite, label: "Attachment", pathname: `/user/${username}/attachment`},
    { icon: MdBolt, label: "Streaks", pathname: `/user/${username}/streaks`},
];