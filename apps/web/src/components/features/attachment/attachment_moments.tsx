import type { AttachmentMoment } from "@/typing";
import {
    Flex,
    Box,
    Card,
    Badge,
    Text as ChakraText,
    Collapsible
} from "@chakra-ui/react";
import { useState } from "react";


function formatName(
    name: string, maxChars: number
) {
    if (name?.length <= maxChars) {
        return name;
    }
    else {
        return name?.slice(0, maxChars - 3) + "..."
    }
}

function MomentCard(
    { item, key }: { item: AttachmentMoment, key: number }
) {
    const { day, z_score } = item;
    const date = new Date(day);
    const date_string = date.toLocaleDateString();
    const [open, setOpen] = useState(false);

    const getColor  = (z_score: number) => {
        if (z_score > 3) {
            return "brand.cardbg"
        }
        else {
            return "bg"
        }
    } 

    return (
        <Flex
            overflow={"auto"}
            key={key}
        >
            <Box w={"240px"}>
                <Collapsible.Root
                    unmountOnExit
                    open={open}
                    onOpenChange={(details) => {
                        setOpen(details.open);
                    }}
                >
                    <Collapsible.Trigger asChild>
                        <Card.Root
                            variant="outline"
                            _hover={{ bg: "brand.muted" }}
                            transition="0.2s"
                            padding={4}
                            bg={getColor(z_score)}
                        >
                            <Flex justify="space-between" align="center">
                                <Box>
                                    <ChakraText fontWeight="bold">
                                        {open ? item.name : formatName(item.name, 24)}
                                    </ChakraText>
                                    <Badge colorPalette={"brand"} mt={1} variant="surface" size={"md"}>
                                        {date_string}
                                    </Badge>
                                </Box>
                            </Flex>
                            <Collapsible.Content>
                                <Box mt={4} fontWeight={"bold"}>
                                    <ChakraText fontSize="sm" color="accent">
                                        Attachment Index: {item.value.toFixed(2)}
                                    </ChakraText>

                                    <ChakraText fontSize="sm">
                                        Scrobbles: {item.scrobbles} / {item.total_scrobbles}
                                    </ChakraText>

                                    <ChakraText fontSize="sm">
                                        Dominance: {(item.dominance * 100).toFixed(1)}%
                                    </ChakraText>

                                    <ChakraText fontSize="sm">
                                        z-score: {item.z_score.toFixed(2)}
                                    </ChakraText>
                                </Box>
                            </Collapsible.Content>
                        </Card.Root>
                    </Collapsible.Trigger>
                </Collapsible.Root>
            </Box>
        </Flex >
    );
};

function groupMoments(moments: AttachmentMoment[], size: number) {
    const groups = [];

    for (let i = 0; i < moments.length; i += size) {
        groups.push(moments.slice(i, i + size));
    }

    return groups;
}

function SnakeGroup(
    { group, index, totalGroups }: {
        group: AttachmentMoment[],
        index: number,
        totalGroups: number,
    }
) {
    const isEvenRow = index % 2 === 0;
    return (
        <Flex
            key={index}
            direction={isEvenRow ? "row" : "row-reverse"}
            gap="10"
            position={"relative"}
            _after={index < totalGroups - 1 ? {
                content: '""',
                position: "absolute",
                top: "95%",
                right: isEvenRow ? "-20px" : "auto",
                left: !isEvenRow ? "-20px" : "auto",
                width: "10",
                height: `${80}px`,
                borderRight: isEvenRow ? "3px solid var(--chakra-colors-brand-solid)" : "none",
                borderLeft: !isEvenRow ? "3px solid var(--chakra-colors-brand-solid)" : "none",
                borderRadius: isEvenRow ? "0 20px 20px 0" : "20px 0 0 20px",
            } : {}}
        >
            {group.map((item, idx) => (
                <Box key={idx} position="relative">
                    <MomentCard item={item} key={idx} />
                    {((isEvenRow && idx < group.length - 1) || (!isEvenRow && idx > 0)) && (
                        <Box
                            position="absolute"
                            top="50px"
                            right="-10"
                            w="10"
                            h="1px"
                            borderTop="3px solid var(--chakra-colors-brand-solid)"
                            zIndex={1}
                        />
                    )}
                </Box>
            ))}
        </Flex>
    )
}

export default function AttachmentTimeline(
    { moments }: { moments: AttachmentMoment[] }
) {

    const groups = groupMoments(moments, 4);
    return (
        <Flex direction="column" gap={12} mt={6} position="relative">
            {groups.map((group, index) => (
                <SnakeGroup
                    group={group}
                    index={index}
                    totalGroups={groups.length}
                />
            ))}
        </Flex>
    )
}
