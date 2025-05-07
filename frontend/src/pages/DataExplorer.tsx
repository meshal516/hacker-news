import React, { useState } from "react";
import { Box, Button, Typography, Collapse, Paper, Stack } from "@mui/material";
import {
  FilterList as FilterListIcon,
  FilterListOff as FilterListOffIcon,
} from "@mui/icons-material";
import FilterPanel from "../components/DataExplorer/FilterPanel";
import StoryTable from "../components/DataExplorer/StoryTable";

const DataExplorer: React.FC = () => {
  const [isFilterOpen, setIsFilterOpen] = useState(true);

  return (
    <Box sx={{ p: { xs: 2, sm: 3 } }}>
      <Stack
        direction={{ xs: "column", sm: "row" }}
        justifyContent="space-between"
        alignItems={{ xs: "flex-start", sm: "center" }}
        spacing={2}
        sx={{ mb: 3 }}
      >
        <Box>
          <Typography
            variant="h4"
            component="h1"
            gutterBottom
            sx={{ fontWeight: "bold" }}
          >
            Data Explorer
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Search and filter through all Hacker News stories.
          </Typography>
        </Box>
        <Button
          variant="contained"
          onClick={() => setIsFilterOpen(!isFilterOpen)}
          startIcon={isFilterOpen ? <FilterListOffIcon /> : <FilterListIcon />}
          sx={{ minWidth: "160px" }}
        >
          {isFilterOpen ? "Hide Filters" : "Show Filters"}
        </Button>
      </Stack>

      <Collapse in={isFilterOpen} timeout="auto" unmountOnExit>
        <Box sx={{ mb: 3 }}>
          <FilterPanel />
        </Box>
      </Collapse>

      <Paper elevation={2} sx={{ width: "100%", overflow: "hidden" }}>
        <StoryTable />
      </Paper>
    </Box>
  );
};

export default DataExplorer;
