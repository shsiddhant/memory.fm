import { useState, type ChangeEvent } from 'react';
import { Box, Button, VStack, Input } from '@chakra-ui/react'
import { useNavigate } from 'react-router-dom';
import "../../App.css"
import { ensureUser } from '@/api/user';

function HomePage() {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => setUsername(event.target.value);
  async function handleClick () {
    if (!username.trim()) {
      return;
    }
    await ensureUser(username);
    navigate(`/user/${username}/overview`);
  
  };

  return (
    <>
      <section id="center">
        <div>
          <h1>memory.fm</h1>
          <div className="quote">music meets memory</div>
        </div>
      </section>
      <VStack gap="10">
        <Box w="50%">
          <Input
            value={username}
            placeholder="username"
            variant="flushed"
            textAlign="center"
            onChange={handleChange}
          />
        </Box>
        <Button
          h="10"
          onClick={handleClick}
        >
          Enter
        </Button>
      </VStack>
    </>
  )
}

export default HomePage
