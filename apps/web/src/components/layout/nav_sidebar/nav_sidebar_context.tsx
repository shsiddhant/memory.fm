import { createContext, useContext, useState } from "react";

type SidebarNavContextType = {
  open: boolean;
  setOpen: (v: boolean) => void;
  toggle: () => void;
};

const SidebarNavContext = createContext<SidebarNavContextType | null>(null);

export function useSidebarNav() {
  const ctx = useContext(SidebarNavContext);
  if (!ctx) {
    throw new Error("Cannot use `sidebar context` outside SidebarProvider");
  }
  return ctx;
}

export function SidebarNavProvider(
    { children }: { children: React.ReactNode;}
) {
  const [open, setOpen] = useState<boolean>(false);
  
  const toggle = () => setOpen(v => !v);

  return (
    <SidebarNavContext.Provider value={{ open, setOpen, toggle}}>
      {children}
    </SidebarNavContext.Provider>
  );
}