import AppNavbar from "@/App/Navbar";
import ErrorBoundary from "@/components/ErrorBoundary";
import { Layout } from "@/constants";
import NavbarProvider from "@/contexts/Navbar";
import OnlineProvider from "@/contexts/Online";
import { notification } from "@/modules/notifications";
import CriticalError from "@/pages/CriticalError";
import { Environment } from "@/utilities";
import { AppShell } from "@mantine/core";
import { useWindowEvent } from "@mantine/hooks";
import { showNotification } from "@mantine/notifications";
import { FunctionComponent, useEffect, useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import AppHeader from "./Header";

const App: FunctionComponent = () => {
  const navigate = useNavigate();

  const [criticalError, setCriticalError] = useState<string | null>(null);
  useWindowEvent("app-critical-error", ({ detail }) => {
    setCriticalError(detail.message);
  });

  useWindowEvent("app-login-required", () => {
    navigate("/login");
  });

  useWindowEvent("app-online-status", ({ detail }) => {
    setOnline(detail.online);
  });

  useEffect(() => {
    if (Environment.hasUpdate) {
      showNotification(
        notification.info(
          "Update available",
          "A new version of Bazarr is ready, restart is required"
        )
      );
    }
  }, []);

  const [navbar, setNavbar] = useState(false);
  const [online, setOnline] = useState(true);

  if (criticalError !== null) {
    return <CriticalError message={criticalError}></CriticalError>;
  }

  return (
    <ErrorBoundary>
      <NavbarProvider value={{ showed: navbar, show: setNavbar }}>
        <OnlineProvider value={{ online, setOnline }}>
          <AppShell
            navbarOffsetBreakpoint={Layout.MOBILE_BREAKPOINT}
            header={<AppHeader></AppHeader>}
            navbar={<AppNavbar></AppNavbar>}
            padding={0}
            fixed
          >
            <Outlet></Outlet>
          </AppShell>
        </OnlineProvider>
      </NavbarProvider>
    </ErrorBoundary>
  );
};

export default App;
