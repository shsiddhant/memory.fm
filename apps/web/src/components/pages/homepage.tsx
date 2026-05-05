import { useState, type ChangeEvent, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { ensureUser } from '@/api/user';

import { Box, Button, VStack, Input, Center, Container, Text as ChakraText, Heading, Field } from '@chakra-ui/react'

function HomePage() {
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const normalizedUsername = username.trim();

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    setError(null);
    setUsername(event.target.value);
  }

  async function handleSubmit(event: FormEvent) {
    event?.preventDefault();

    if (!normalizedUsername || loading) return;

    try {
      setLoading(true);
      setError(null);

      await ensureUser(normalizedUsername);

      navigate(`/user/${normalizedUsername}/overview`);
    } catch (err: any) {
      console.error("Failed to ensure user exists.", err);

      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Center minH="100vh" bg="bg.canvas">
      <Container maxW="md">
        <VStack gap="12" textAlign="center">
          {/* Logo/Hero Section */}
          <VStack gap="2">
            <Heading size="6xl" fontWeight="bold" color="accent" letterSpacing="tight">
              memory.fm
            </Heading>
            <ChakraText fontSize="xl" color="fg.muted" fontStyle="italic">
              music meets memory
            </ChakraText>
          </VStack>

          {/* Form Section */}
          <Box as="form" onSubmit={handleSubmit} w="full">
            <VStack gap="6">
              <Field.Root invalid={!!error}>
              <Input
                autoFocus
                value={username}
                placeholder="Enter your Last.fm username"
                variant="subtle"
                display={"flex"}
                textAlign="center"
                lineHeight="1"
                onChange={handleChange}
                disabled={loading}
                _focus={{ borderColor: "accent" }}
              />
              </Field.Root>

              {error && (
                <ChakraText color="red.400" fontSize="sm">
                  {error}
                </ChakraText>
              )}

              <Button
                size="xl"
                w="full"
                type="submit"
                loading={loading}
                disabled={!normalizedUsername}
                bg="accent"
                color="white"
                _hover={{ bg: "accent" }}
              >
                Get Started
              </Button>
            </VStack>
          </Box>
        </VStack>
      </Container>
    </Center>
  );
}

export default HomePage;