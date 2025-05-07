import { createTheme, PaletteMode } from "@mui/material/styles";

export const getTheme = (mode: PaletteMode) =>
  createTheme({
    palette: {
      mode,
      ...(mode === "light"
        ? {
            // Palette values for light mode
            primary: {
              main: "#4f46e5", // Indigo
              contrastText: "#ffffff",
            },
            secondary: {
              main: "#06b6d4", // Cyan
              contrastText: "#ffffff",
            },
            background: {
              default: "#f8fafc", // Slate 50
              paper: "#ffffff", // White
            },
            text: {
              primary: "#0f172a", // Slate 900
              secondary: "#64748b", // Slate 500
            },
          }
        : {
            // Palette values for dark mode
            primary: {
              main: "#818cf8", // Indigo 400 (lighter for dark mode)
              contrastText: "#1e1b4b", // Indigo 950
            },
            secondary: {
              main: "#67e8f9", // Cyan 300 (lighter for dark mode)
              contrastText: "#164e63", // Cyan 900
            },
            background: {
              default: "#0f172a", // Slate 900
              paper: "#1e293b", // Slate 800
            },
            text: {
              primary: "#f8fafc", // Slate 50
              secondary: "#94a3b8", // Slate 400
            },
          }),
    },
    typography: {
      fontFamily: "Inter, sans-serif",
      h1: {
        fontSize: "2rem",
        fontWeight: 700,
      },
      button: {
        textTransform: "none",
        fontWeight: 600,
      },
    },
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: "8px",
            padding: "8px 16px",
          },
        },
      },
      MuiPaper: {
        styleOverrides: {
          root: {
            boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
          },
        },
      },
    },
  });
