import { useEffect, useState } from "react";
import { MdCalendarMonth } from "react-icons/md";
import { Badge, Icon, VStack} from "@chakra-ui/react"
import { useParams } from "react-router-dom";
import SummaryBadges from "./summarybadges";

export default function Overview () {
    const { username } = useParams();
    const [userData, setUserData] = useState<null | {
        user: {
            user_id: number,
            username: string
        },
        summary: {
            total_scrobbles: number,
            days: number,
            scrobbling_since: string,
            scrobbles_per_day: number,
            tracks: number,
            artists: number,
            albums: number,
        },
    }>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!username || !username.trim()) {
            return;
        }
        async function fetchData() {
            try {
                const response = await fetch(`http://127.0.0.1:8000/user/${username}/summary`);
                if (response.ok) {
                    const result = await response.json();
                    setUserData(result)
                } else {
                console.error("User not found.");
                return;
                }
            } catch (error) {
                console.error("Network Error:", error);
            } finally {
            setLoading(false);
            }
        }

        fetchData();
    }, [username]);

    if (loading) {
        return <div>Loading....</div>;
    }
    if (!userData) {
        return <div>No data found.</div>;
    }
    const summary = userData.summary;
    return (
        <>
        <section id="center">
          <VStack gap={5}>
            <h1>{username}</h1>
            <Badge bg={"purple.subtle"} color={"purple.fg"} size={"lg"}>
                <Icon as={MdCalendarMonth} mr={1}></Icon>
                {`Scrobbling since ${summary.scrobbling_since}`}
            </Badge>
          </VStack>
        </section>
        <section className="ticks"></section>
        <section id="main-content" >
            <SummaryBadges {...summary} />
        </section>
        </>
    )
}