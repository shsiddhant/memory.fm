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
      <Box w="full" maxW="1200px">
        <SectionSeparator title={title} colorToken="ticks" />
        <Box as="section" mb="12" justifyItems={"center"}>
          <Stack className="content" h="full">
            {children}
          </Stack>
        </Box>
      </Box>
    </Flex>
  );
};

export default Section;