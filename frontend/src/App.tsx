import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { ThemeProvider as MuiThemeProvider, CssBaseline } from "@mui/material";
import { getTheme } from "./theme/theme";
import {
  ThemeProvider as CustomThemeProvider,
  useTheme as useCustomTheme,
} from "./contexts/ThemeContext";
import DashboardLayout from "./layouts/DashboardLayout";
import Dashboard from "./pages/Dashboard";
import DataExplorer from "./pages/DataExplorer";

const AppWithMuiTheme: React.FC = () => {
  const { isDark } = useCustomTheme();
  const muiTheme = React.useMemo(
    () => getTheme(isDark ? "dark" : "light"),
    [isDark]
  );

  return (
    <MuiThemeProvider theme={muiTheme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<DashboardLayout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="data-explorer" element={<DataExplorer />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Route>
        </Routes>
      </Router>
    </MuiThemeProvider>
  );
};

const App: React.FC = () => {
  return (
    <CustomThemeProvider>
      <AppWithMuiTheme />
    </CustomThemeProvider>
  );
};

export default App;
