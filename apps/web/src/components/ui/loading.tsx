import { Spinner, Text, VStack } from "@chakra-ui/react"


export const LoadingSpinner = () => {
  return (
    <VStack colorPalette="brand">
      <Spinner size={"md"}/>
      <Text>Loading...</Text>
    </VStack>
  )
}