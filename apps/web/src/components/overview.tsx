import { useQuery } from "@tanstack/react-query";
import { fetchRecentActivity, fetchTopCharts, fetchUserSummary } from "@/api/user";
import { MdCalendarMonth } from "react-icons/md";
import { Badge, Box, Container, Flex, Icon, VStack} from "@chakra-ui/react"
import { useParams } from "react-router-dom";
import SummaryBadges from "./summarybadges";
import RecentActivity from "./recent_activity";
import TopChartsPreview from "./topcharts_preview";
import HeaderBar from "./headerbar";
import NoScrobbles from "./no_scrobbles";


export default function Overview () {
    const { username } = useParams();
    const [weeks, period, limit] = [12, 30, 5]
    let isValidUsername = false;
    if (!username?.trim()) {
        return;
    }
    else {
        isValidUsername = true;
    }

    const summaryQuery = useQuery({
        queryKey: ["summaryQuery", username],
                queryFn: () => fetchUserSummary(username),
                enabled: isValidUsername
    });

    const hasValidSummary = summaryQuery.data?.summary != null;

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

    if (!isValidUsername) return null;

    if (summaryQuery.isLoading) {
        return <div>Loading summary...</div>;
    }

    if (summaryQuery.isError || !hasValidSummary) {
        return (
            <>
                <HeaderBar username={username} />
                <NoScrobbles />
            </>
        );
    }

    const isLoading =
        recentActivityQuery.isLoading ||
        topArtistsQuery.isLoading ||
        topTracksQuery.isLoading;

    const isError =
        recentActivityQuery.isError ||
        topArtistsQuery.isError ||
        topTracksQuery.isError;

    if (isLoading) return <div>Loading...</div>;

    if (isError) {
        return (
            <>
                <HeaderBar username={username} />
                <NoScrobbles />
            </>
        );
    }

    const { summary } = summaryQuery.data
    const { from_date, to_date, counts } = recentActivityQuery.data
    const topArtistsInput = {kind: "artist", topCharts: topArtistsQuery.data}
    const topTracksInput = {kind: "track", topCharts: topTracksQuery.data}

    return (
        <>
        <HeaderBar username={username} />
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
    )
}

    