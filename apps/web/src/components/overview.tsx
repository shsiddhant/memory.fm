import { useQueries } from "@tanstack/react-query";
import { fetchRecentActivity, fetchUserSummary } from "@/api/user";
import { MdCalendarMonth } from "react-icons/md";
import { Badge, Box, Container, Flex, Icon, VStack} from "@chakra-ui/react"
import { useParams } from "react-router-dom";
import SummaryBadges from "./summarybadges";
import RecentActivity from "./recent_activity";


export default function Overview () {
    const { username } = useParams();
    const weeks = 12;
    
    if (!username || !username.trim()) {
            return;
        }
    const [recentActivityQuery, summaryQuery] = useQueries({
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
        ],
    });

    const isLoading = recentActivityQuery.isLoading || summaryQuery.isLoading;

    if (isLoading) {
        return <div>Loading...</div>
    }

    if (summaryQuery.isError) {
        return <div>Error: {summaryQuery.error.message}</div>
    }
    if (recentActivityQuery.isError) {
        return <div>Error: {recentActivityQuery.error.message}</div>
    }
    if (!summaryQuery.data || !recentActivityQuery.data) {
        return <div>No data.</div>;}
    const { summary } = summaryQuery.data
    const { from_date, to_date, counts } = recentActivityQuery.data
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
                <h2>Recent Activity</h2>
                <Flex justifySelf={"center"} mt={6}>
                    <Box outlineColor={"red"}>
                        <RecentActivity from_date={from_date} to_date={to_date} counts={counts} />
                    </Box>
                </Flex>
            </Container>
        </section>
        </>
    )
}