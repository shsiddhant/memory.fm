import { Provider } from "@/components/ui/provider"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { SidebarNavProvider } from "@/components/layout/nav_sidebar/nav_sidebar_context"
import App from './App.tsx'
import "./index.css"
import "@fontsource-variable/atkinson-hyperlegible-mono"
import "@fontsource-variable/atkinson-hyperlegible-next"

const queryClient = new QueryClient();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider>
      <SidebarNavProvider>
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
      </SidebarNavProvider>
    </Provider>
  </StrictMode>,
)
