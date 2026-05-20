import { MdBarChart, MdBolt, MdFavorite, MdHome, MdListAlt, MdOutlineFeedback, MdOutlineVolunteerActivism } from "react-icons/md";
import type { ExternalLinkItem, SidebarNavItem } from "./nav_items";
import { FaGithub } from "react-icons/fa";

export const useNavItems = (username: string): SidebarNavItem[] => [
    { icon: MdHome, label: "Home", pathname: "/" },
    { icon: MdListAlt, label: "Overview", pathname: `/user/${username}/overview` },
    { icon: MdBarChart, label: "Top Charts", pathname: `/user/${username}/topcharts` },
    { icon: MdFavorite, label: "Attachment", pathname: `/user/${username}/attachment` },
    { icon: MdBolt, label: "Streaks", pathname: `/user/${username}/streaks` },
];

export const useExternalLinks = (): ExternalLinkItem[] => [
    { icon: MdOutlineFeedback, label: "Feedback", href: "https://tally.so/r/Y5JVpz" },
    { icon: FaGithub, label: "GitHub", href: "https://github.com/shsiddhant/memory.fm/" },
    { icon: MdOutlineVolunteerActivism, label: "Support Us", href: "https://ko-fi.com/shsiddhant" },
];