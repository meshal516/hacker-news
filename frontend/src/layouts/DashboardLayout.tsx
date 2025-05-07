import React, { useState } from "react";
import { Outlet, Link as RouterLink, useLocation } from "react-router-dom";
import {
  AppBar,
  Box,
  CssBaseline,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  useTheme as useMuiTheme, // Alias to avoid conflict with custom useTheme
  Tooltip,
} from "@mui/material";
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Assessment as AssessmentIcon, // Data Explorer
  Brightness4 as Brightness4Icon, // Dark mode
  Brightness7 as Brightness7Icon, // Light mode
} from "@mui/icons-material";
import { useTheme as useCustomTheme } from "../contexts/ThemeContext";

const drawerWidth = 240;

const DashboardLayout: React.FC = () => {
  const { isDark, toggleTheme } = useCustomTheme();
  const muiTheme = useMuiTheme(); // MUI's theme object for breakpoints, etc.
  const { pathname } = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const navigationItems = [
    { name: "Dashboard", path: "/dashboard", icon: <DashboardIcon /> },
    { name: "Data Explorer", path: "/data-explorer", icon: <AssessmentIcon /> },
  ];

  const drawerContent = (
    <Box>
      <Toolbar
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          py: 1,
        }}
      >
        <Typography
          variant="h6"
          noWrap
          component={RouterLink}
          to="/dashboard"
          sx={{
            fontWeight: "bold",
            textDecoration: "none",
            color: "inherit",
          }}
        >
          StoryAnalyzer
        </Typography>
      </Toolbar>
      {/* <Divider /> */}
      <List>
        {navigationItems.map((item) => (
          <ListItem key={item.name} disablePadding>
            <ListItemButton
              component={RouterLink}
              to={item.path}
              selected={pathname === item.path}
              sx={{
                "&.Mui-selected": {
                  backgroundColor: "primary.main",
                  color: "primary.contrastText",
                  "& .MuiListItemIcon-root": {
                    color: "primary.contrastText",
                  },
                  "&:hover": {
                    backgroundColor: "primary.dark",
                  },
                },
                mx: 1,
                borderRadius: 1,
                mb: 0.5,
              }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.name} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          zIndex: muiTheme.zIndex.drawer + 1,
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: "none" } }} // Show only on mobile/tablet
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{
              flexGrow: 1,
              display: { xs: "none", sm: "block" },
              overflow: "hidden", // Prevent text overflow
              textOverflow: "ellipsis", // Add ellipsis for long titles
            }}
          >
            {navigationItems.find((item) => item.path === pathname)?.name ||
              "StoryAnalyzer"}
          </Typography>
          <Tooltip
            title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
          >
            <IconButton onClick={toggleTheme} color="inherit">
              {isDark ? <Brightness7Icon /> : <Brightness4Icon />}
            </IconButton>
          </Tooltip>
        </Toolbar>
      </AppBar>

      {/* Mobile Drawer */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: { xs: "block", md: "none" },
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: drawerWidth,
          },
        }}
      >
        {drawerContent}
      </Drawer>

      {/* Desktop Drawer */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: "none", md: "block" },
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: drawerWidth,
          },
        }}
        open // permanent drawer is always open
      >
        {drawerContent}
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${drawerWidth}px)` },
          ml: { md: `${drawerWidth}px` }, // Offset by drawer width on desktop
        }}
      >
        <Toolbar /> {/* Spacer for AppBar */}
        <Outlet />
      </Box>
    </Box>
  );
};

export default DashboardLayout;
