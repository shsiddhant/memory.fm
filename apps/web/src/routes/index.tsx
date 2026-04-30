import { createBrowserRouter } from 'react-router-dom';
import AppLayout from "@/components/layout/layout"
import HomePage from "@/components/pages/homepage"
import Overview from "@/components/pages/overview";
import TopChartsPage from '@/components/pages/topcharts';
import AttachmentPage from '@/components/pages/attachment';
import StreaksPage from '@/components/pages/streaks';


export const router = createBrowserRouter([
    {
        path: "/",
        element: <HomePage />
    },
    
    {
        path: "/user/:username",
        element: <AppLayout />,
        children: [
            {
                path: "overview",
                element: <Overview />,
            },
            {
                path: "topcharts",
                element: <TopChartsPage />
            },
            {
                path: "attachment",
                element: <AttachmentPage />
            },
            {
                path: "streaks",
                element: <StreaksPage />
            },
        ],
    },
]);