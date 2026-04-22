import { createBrowserRouter } from 'react-router-dom';
import AppLayout from "@/components/layout/layout"
import HomePage from "@/components/pages/homepage"
import Overview from "@/components/pages/overview";
import TopChartsPage from '@/components/pages/topcharts';


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
        ],
    },
]);