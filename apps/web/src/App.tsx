import { RouterProvider } from 'react-router-dom';
import { router } from './routes';
import { Box } from '@chakra-ui/react';

export default function App() {
  return (
    <Box minH="100vh" bg="bg.panel">
    <RouterProvider router={router} />
    </Box>
  );
}
