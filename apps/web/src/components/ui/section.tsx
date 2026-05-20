import { Stack, Box, Flex } from '@chakra-ui/react';
import React from 'react';
import { SectionSeparator } from './ticks';

interface SectionProps {
  title: string;
  children: React.ReactNode;
}


const Section = ({ title, children }: SectionProps) => {
  return (
    <Flex direction="column" w="full" align="center">
      <Box width="full" maxW="1200px" mx={"auto"}>
        <SectionSeparator title={title} colorToken="ticks" />
      </Box>
        <Box as="section" mb={{base: 0, md: 8}} justifyItems={"center"}>
          <Stack
            className="content"
            h="full"
            direction={{ base: "column", lg: "row"}}
            gap={10}
            minW="max-content"
            >
            {children}
          </Stack>
        </Box>
    </Flex>
  );
};

export default Section;