import { Box, Flex, Text as ChakraText } from "@chakra-ui/react"

interface SectionSeparatorProps {
  title?: string
  colorToken?: string // e.g. "border.muted" or "gray.200"
}

export const SectionSeparator = ({ 
  title, 
  colorToken = "border.muted" 
}: SectionSeparatorProps) => {

    const tickBase = {
    content: '""',
    position: "absolute",
    top: "-4.5px",
    border: "5px solid transparent",
  }

  return (
    <Flex align="center" gap="4" w="90%" my={{base: 4, md: 8}} justifySelf={"center"} mt={12}>
      <Box
        flex="1"
        h="1px"
        bg={colorToken}
        position="relative"
        _before={{
          ...tickBase,
          left: "0",
          borderLeftColor: `{colors.${colorToken}}`,
        }}
      />

        {title && (
        <ChakraText
          fontSize={{base: "sm", md: "md"}}
          fontWeight="bold"
          color="fg.muted"
          textTransform="uppercase"
          letterSpacing="widest"
          lineBreak={"auto"}
        >
          {title}
        </ChakraText>
      )}
      <Box
        flex="1"
        h="1px"
        bg={colorToken}
        position="relative"
        _after={{
          ...tickBase,
          right: "0",
          borderRightColor: `{colors.${colorToken}}`,
        }}
      />
    </Flex>
  )
}
