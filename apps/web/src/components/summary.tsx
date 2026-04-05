import { useEffect, useState } from "react";
import { Badge, Stack, VStack} from "@chakra-ui/react"
import { useParams } from "react-router-dom";

export default function Summary () {
    const { username } = useParams();
    const [userData, setUserData] = useState<null | {
        user: {
            user_id: Number,
            username: String
        },
        summary: {
            total_scrobbles: Number,
            days: Number,
            scrobbles_per_day: Number,
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
    const { total_scrobbles, days, scrobbles_per_day } = summary
    return (
        <>
        <section id="center">
          <div>
            <h1>memory.fm</h1>
          </div>
        </section>
        <section id="main-content">
          <VStack>
            <h2>{username}</h2>
            <Stack direction={"row"} gap={"5"}>
              <Badge bg={"yellow.subtle"} color={"yellow.fg"}>{`${total_scrobbles} Scrobbles`}</Badge>
              <Badge bg={"purple.subtle"} color={"purple.fg"}>{`Scrobbling for ${days} days`}</Badge>
              <Badge bg={"green.subtle"} color={"green.fg"}>{`${scrobbles_per_day} Scrobbles a day`}</Badge>
            </Stack>
          </VStack>
        </section>
        </>
    )
}