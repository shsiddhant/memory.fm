import {
    MdAlbum,
    MdBarChart,
    MdMusicNote,
    MdPerson,
    MdSpeed
} from "react-icons/md";
import { Badge, Icon, Stack} from "@chakra-ui/react"

interface SummaryObject {
    total_scrobbles: number;
    scrobbles_per_day: number;
    tracks: number;
    artists: number;
    albums: number;
}

export default function SummaryBadges(
    { total_scrobbles, scrobbles_per_day, tracks, artists, albums }: SummaryObject
) {
    return (
            <Stack direction={"row"} gap={"10"} wrap={"wrap"}>
                <Badge bg={"red.subtle"} color={"red.fg"} size={"lg"}>
                    <Icon as={MdBarChart}></Icon>
                    {`${total_scrobbles} Scrobbles`}
                </Badge>
                <Badge bg={"yellow.subtle"} color={"yellow.fg"} size={"lg"}>
                    <Icon as={MdSpeed}></Icon>
                    {`${scrobbles_per_day} Scrobbles a day`}
                </Badge>
                <Badge bg={"orange.subtle"} color={"orange.fg"} size={"lg"}>
                    <Icon as={MdMusicNote}></Icon>
                    {`${tracks} Tracks`}
                </Badge>
                <Badge bg={"blue.subtle"} color={"blue.fg"} size={"lg"}>
                    <Icon as={MdPerson}></Icon>
                    {`${artists} Artists`}
                </Badge>
                <Badge bg={"green.subtle"} color={"green.fg"} size={"lg"}>
                    <Icon as={MdAlbum}></Icon>
                    {`${albums} Albums`}
                </Badge>
            </Stack>
    );
}