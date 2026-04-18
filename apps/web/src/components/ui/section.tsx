import { Stack, Box } from '@chakra-ui/react';
import React from 'react';
import { SectionSeparator } from './ticks';

interface SectionProps {
  title: string;
  children: React.ReactNode;
}


const Section = ({title, children}: SectionProps) => {
    return (
        <>
        <SectionSeparator title={title} colorToken="ticks" />
        <Box as="section" mb="12" justifySelf={"center"}>
        <Stack className="content">
            {children}
        </Stack>
    </Box>
    </>
  );
};

export default Section;