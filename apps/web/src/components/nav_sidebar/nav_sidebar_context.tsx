import { useDisclosure } from "@chakra-ui/react";
import { createContext, useContext } from "react";

const SidebarNavContext = createContext<ReturnType<typeof useDisclosure> | null>(
  null
);

export function useSidebarNav() {
  const sidebar = useContext(SidebarNavContext);
  if (!sidebar) {
    throw new Error("Cannot use `sidebar context` outside SidebarProvider");
  }
  return { ...(sidebar as ReturnType<typeof useDisclosure>) };
}

export function SidenbarNavProvider(
    { children, ...props }: { children: React.ReactNode;}
) {
  const disclosure = useDisclosure();
  return (
    <SidebarNavContext.Provider value={{ ...disclosure }} {...props}>
      {children}
    </SidebarNavContext.Provider>
  );
}