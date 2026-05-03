import { HStack, Text as ChakraText, IconButton, Flex, Box } from "@chakra-ui/react"
import { MdInfo } from "react-icons/md"
import { Tooltip } from "./tooltip"
import type { PageHeaderProps } from "@/typing"

export default function PageHeader(
    page: PageHeaderProps
) {
    return (
        <HStack gap={0} align={"top"} justify={"center"} mb={"6"}>
            <Flex align="center" gap="2">
                <Box fontSize="2xl"><page.icon /></Box>
                <ChakraText
                    fontWeight="bold"
                    fontSize={"2xl"}
                    textTransform={"uppercase"}
                    letterSpacing={"widest"}
                >
                    {page.title}
                </ChakraText>
            </Flex>
            {page.info.length>0 && (<Tooltip
                content={page.info}
                interactive
            >
                <IconButton
                    variant="plain"
                    color="fg.subtle"
                    size="xs"
                    aria-label="Attachment Index Info"
                >
                    <MdInfo />
                </IconButton>
            </Tooltip>
            )}
        </HStack>
    )
}