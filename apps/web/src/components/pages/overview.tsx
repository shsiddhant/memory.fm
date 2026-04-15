import { useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchRecentActivity, fetchTopCharts, fetchUserSummary } from "@/api/user";
import { MdCalendarMonth } from "react-icons/md";
import { Badge, Box, Container, Flex, Icon, VStack} from "@chakra-ui/react"
import { useParams } from "react-router-dom";
import { useSyncStatus } from "@/api/sync";

import SyncCompleteAlert from "../sync_complete_alert";
import SyncProgress from "../sync_progress";
import SummaryBadges from "../summarybadges";
import RecentActivity from "../recent_activity";
import TopChartsPreview from "../topcharts_preview";
import HeaderBar from "../headerbar";
import NoScrobbles from "../no_scrobbles";
import { useEffect, useState } from "react";


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
    
    const [ hasStartedSync, setHasStartedSync ] = useState<boolean>(false);

    const { syncStatus } = useSyncStatus(username, hasStartedSync); 

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
        queryFn: () => fetchTopCharts(username, "artist", period, limit),
        enabled: isValidUsername && hasValidSummary
    });

    const topTracksQuery = useQuery({
        queryKey: ["topTracks", username, period, limit],
        queryFn: () => fetchTopCharts(username, "track", period, limit),
        enabled: isValidUsername && hasValidSummary
    });

    useEffect(() => {
    if (!syncStatus) return;

    if (syncStatus.status === "completed") {

        setTimeout(() => {
            setHasStartedSync(false);
            setFetched(syncStatus?.fetched_scrobbles);
            setShowAlert(true);
        }, 1000);

        queryClient.invalidateQueries({
            queryKey: ["summaryQuery", username],
            refetchType: "active"
        });
    }
  }, [syncStatus?.status, syncStatus?.fetched_scrobbles, username, queryClient]);

  useEffect(() => {
    queryClient.invalidateQueries({
      queryKey: ["summaryQuery", username]
    });
  }, [username, queryClient]);

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
        <HeaderBar username={username} onSync={setHasStartedSync} />
        {showAlert ? (
            <SyncCompleteAlert
                fetched={fetched}
                onClose={setShowAlert}
            /> 
        ) : hasStartedSync ? (
            <SyncProgress
                syncStatus={syncStatus}
            />
        ) : null}
        {!hasValidSummary ? (
            <NoScrobbles
                    username={username}
                    syncStatus={syncStatus}
                    hasStartedSync={hasStartedSync}
                    onSync={setHasStartedSync}
            />
        ) : (
            <>
                <section id="center">
                    <VStack gap={10} mb={10}>
                        <Badge bg={"purple.subtle"} color={"purple.fg"} size={"lg"}>
                            <Icon as={MdCalendarMonth} mr={1}></Icon>
                            {`Scrobbling since ${summary.scrobbling_since}`}
                        </Badge>
                        <SummaryBadges {...summary} />
                    </VStack>
                </section>
                <section className="ticks"></section>
                <section id="main-content">
                    <Container>
                        <h2>{"Recent Activity".toUpperCase()}</h2>
                        <Flex justifySelf={"center"} mt={12}>
                            <Box outlineColor={"red"}>
                                <RecentActivity from_date={from_date} to_date={to_date} counts={counts} />
                            </Box>
                        </Flex>
                    </Container>
                </section>
                <section className="ticks"></section>
                <section id="main-content">
                    <Container>
                        <h2>{`Top Charts - Last ${period} Days`.toUpperCase()}</h2>
                        <Flex gap={20} justify={"center"} mt={12}>
                            <TopChartsPreview {...topArtistsInput} />
                            <TopChartsPreview {...topTracksInput} />
                        </Flex>
                    </Container>
                </section>
                <section id="spacer"></section>
            </>
        )}
        </>
    );
}

    