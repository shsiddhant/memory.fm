import { RouterProvider } from 'react-router-dom';
import { router } from './routes';
import { Box } from '@chakra-ui/react';
import Maintenance from '@/components/maintenance';

export default function App() {

  const isMaintenanceMode = import.meta.env.VITE_APP_MAINTENANCE === 'true';

  if (isMaintenanceMode) {
    return <Maintenance />;
  }
  
  return (
    <Box minH="100vh" bg="bg.panel">
      <RouterProvider router={router} />
    </Box>
  );
}
