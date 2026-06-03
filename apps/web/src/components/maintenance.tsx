import { Text as ChakraText, VStack } from '@chakra-ui/react';

export default function Maintenance() {
    return (
        <VStack w="" mx={{base: 4, md: 12}} mt="4">
            <ChakraText fontSize="xl" fontWeight={"bold"}>memory.fm is temporarily under maintenance</ChakraText>
            <ChakraText textAlign="left">Thank you to everyone who tried memory.fm over the past few hours.</ChakraText>
                
            <ChakraText textAlign="left">The response has been much larger than I anticipated,
                and the current infrastructure is struggling to keep up with the volume of large first-time imports.
                To avoid a poor experience for new users, I am temporarily pausing access while I improve the import pipeline and infrastructure.
                Existing imports will continue processing.</ChakraText>

            <ChakraText textAlign="left" mt={"2"}>I'll reopen the site as soon as things are stable again.</ChakraText>

            <ChakraText textAlign="left">Thank you for your patience.</ChakraText>
        </VStack>
    );
}