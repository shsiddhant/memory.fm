import { useQueries } from "@tanstack/react-query";
import { fetchRecentActivity, fetchTopCharts, fetchUserSummary } from "@/api/user";
import { MdCalendarMonth } from "react-icons/md";
import { Badge, Box, Container, Flex, Icon, VStack} from "@chakra-ui/react"
import { useParams } from "react-router-dom";
import SummaryBadges from "./summarybadges";
import RecentActivity from "./recent_activity";
import TopChartsPreview from "./topcharts_preview";


export default function Overview () {
    const { username } = useParams();
    const [weeks, period, limit] = [12, 30, 5] 
    
    if (!username || !username.trim()) {
            return;
        }
    const [recentActivityQuery, summaryQuery, topArtistsQuery, topTracksQuery] = useQueries({
        queries: [
            {
                queryKey: ["recentActivity", username, weeks],
                queryFn: () => fetchRecentActivity(username, weeks),
                enabled: !!username,
            },
            {
                queryKey: ["summaryQuery", username],
                queryFn: () => fetchUserSummary(username),
                enabled: !!username,
            },
            {
                queryKey: ["topArtists", username, period, limit],
                queryFn: () => fetchTopCharts(username, "artist", period, limit),
                enabled: !!username,
            },
            {
                queryKey: ["topTracks", username, period, limit],
                queryFn: () => fetchTopCharts(username, "track", period, limit),
                enabled: !!username,
            },
        ],
    });

    const isLoading = (
        recentActivityQuery.isLoading || summaryQuery.isLoading ||
        topArtistsQuery.isLoading || topTracksQuery.isLoading
    );

    if (isLoading) {
        return <div>Loading...</div>
    }

    for (const query of [recentActivityQuery, summaryQuery, topArtistsQuery, topTracksQuery]) {
        if (query.isError) {
            return <div>Error: { query.error.message }</div>
        }
    }
    if (!summaryQuery.data || !recentActivityQuery.data || !topArtistsQuery.data || !topTracksQuery.data) {
        return <div>No data.</div>;}

    const { summary } = summaryQuery.data
    const { from_date, to_date, counts } = recentActivityQuery.data
    const topArtistsInput = {kind: "artist", topCharts: topArtistsQuery.data}
    const topTracksInput = {kind: "track", topCharts: topTracksQuery.data}

    return (
        <>
        <section id="center">
          <VStack gap={10} mb={10}>
            <h1>{username}</h1>
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
    )
}