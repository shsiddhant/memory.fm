import { useParams } from "react-router-dom";
import { useQuery, useQueryClient } from "@tanstack/react-query";

// Data API
import { fetchRecentActivity, fetchTopChartsByPeriod, fetchUserSummary } from "@/api/user";

// Hooks
import { useSyncStatus } from "@/hooks/use_sync_status";

// Components

// Chakra UI components
import { MdCalendarMonth } from "react-icons/md";
import { Badge, Box, Flex, Icon, Separator, VStack} from "@chakra-ui/react"

// Custom Components
import Section from "@/components/ui/section";
import SyncCompleteAlert from "../features/overview/sync_complete_alert";
import SyncProgress from "../features/overview/sync_progress";
import SummaryBadges from "../features/overview/summarybadges";
import RecentActivity from "../features/overview/recent_activity";
import TopChartsPreview from "../features/overview/topcharts_preview";
import NoScrobbles from "../features/overview/no_scrobbles";
import { useEffect, useState } from "react";

// Overview Page

export default function Overview () {
    const { username } = useParams();
    const queryClient = useQueryClient();
    
    const [weeks, period, limit] = [12, 30, 5];
    let isValidUsername = false;
    if (!username?.trim()) {
        return null;
    }
    else {
        isValidUsername = true;
    }
    
    const { syncStatus, isSyncActive } = useSyncStatus(username);
    const [ showAlert, setShowAlert ] = useState<boolean>(false);
    const [ fetched, setFetched ] = useState<number | null>(null);

    const summaryQuery = useQuery({
        queryKey: ["summaryQuery", username],
        queryFn: () => fetchUserSummary(username),
        enabled: isValidUsername
    });

    const hasValidSummary = !!summaryQuery.data?.summary;

    const recentActivityQuery = useQuery({
        queryKey: ["recentActivity", username, weeks],
        queryFn: () => fetchRecentActivity(username, weeks),
        enabled: isValidUsername && hasValidSummary
    });

    const topArtistsQuery = useQuery({
        queryKey: ["topArtists", username, period, limit],
        queryFn: () => fetchTopChartsByPeriod(username, "artist", period, limit),
        enabled: isValidUsername && hasValidSummary
    });

    const topTracksQuery = useQuery({
        queryKey: ["topTracks", username, period, limit],
        queryFn: () => fetchTopChartsByPeriod(username, "track", period, limit),
        enabled: isValidUsername && hasValidSummary
    });

    const handleCloseAlert = () => {
        if (!syncStatus) return;
        
        const key = `syncAlertDismissed:${username}:${syncStatus.fetched_scrobbles}`;
        localStorage.setItem(key, "true");
        setShowAlert(false);
    };

    useEffect(() => {
        if (!syncStatus) return;
        
        if (syncStatus.status !== "completed") return;

        const key = `syncAlertDismissed:${username}:${syncStatus.fetched_scrobbles}`;

        setTimeout(() => {
            const dismissed = localStorage.getItem(key) === "true";
            if (dismissed) return;
            
            setFetched(syncStatus.fetched_scrobbles);
            setShowAlert(true);
        }, 1000);
    
    }, [syncStatus?.status, syncStatus?.fetched_scrobbles, username]);

  useEffect(() => {
    queryClient.invalidateQueries({
      queryKey: ["summaryQuery", username]
    });
  }, [username, queryClient]);

    if (summaryQuery.isLoading) {
        return <div>Loading summary...</div>;
    }

    if (summaryQuery.isLoading) {
        return <div>Loading summary...</div>;
    }

    const isLoading =
        recentActivityQuery.isLoading ||
        topArtistsQuery.isLoading ||
        topTracksQuery.isLoading;

    const isError =
        summaryQuery.isError ||
        recentActivityQuery.isError ||
        topArtistsQuery.isError ||
        topTracksQuery.isError;

    if (isLoading) return <div>Loading...</div>;

    if (isError) {
        return (
            <VStack gap={"5"}>
                <div>
                    { summaryQuery.error?.message}
                </div>
                <div>
                    { recentActivityQuery.error?.message }
                </div>
                <div>
                    { topArtistsQuery.error?.message }
                </div>
                <div>
                    { topTracksQuery.error?.message }
                </div>
            </VStack>
        );
    }


    const { summary } = summaryQuery.data || {}
    const { from_date, to_date, counts } = recentActivityQuery.data || {}
    const topArtistsInput = {kind: "artist", topCharts: topArtistsQuery.data}
    const topTracksInput = {kind: "track", topCharts: topTracksQuery.data}

    return (
        <>
        {showAlert ? (
            <SyncCompleteAlert
                fetched={fetched}
                onClose={handleCloseAlert}
            /> 
        ) : isSyncActive ? (
            <SyncProgress
                syncStatus={syncStatus!}
            />
        ) : null}
        {!hasValidSummary ? (
            <NoScrobbles
                    username={username}
                    syncStatus={syncStatus!}
                    isSyncActive={isSyncActive}
            />
        ) : (
            <>
                <Box px={{ base: 4, md: 8 }}>
                    <VStack gap={{base: 4, md: 10 }}>
                        <Badge
                            bg={"purple.subtle"}
                            color={"purple.fg"}
                            size={"lg"}
                            display="flex"
                        >
                            <Icon as={MdCalendarMonth} mr={1}></Icon>
                            {`Scrobbling since ${summary.scrobbling_since}`}
                        </Badge>
                        <SummaryBadges {...summary} />
                    </VStack>
                </Box>
                <Section
                    title={"Recent Activity"}
                    children={<RecentActivity from_date={from_date} to_date={to_date} counts={counts} />}
                />
                <Section
                    title={`Top Charts - Last ${period} Days`}
                >
                    <Flex direction={"row"} gap="10" justify={"space-between"}>
                        <TopChartsPreview {...topArtistsInput} />
                        <Separator />
                        <TopChartsPreview {...topTracksInput} />
                    </Flex>
                </Section>
            </>
        )}
        </>
    );
}

    