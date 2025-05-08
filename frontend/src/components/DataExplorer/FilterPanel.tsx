import React, { useState, useEffect } from "react";
import {
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Grid,
  Paper,
  Typography,
  FormLabel,
  Stack,
  InputAdornment,
  SelectChangeEvent,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import FilterAltIcon from "@mui/icons-material/FilterAlt";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import { useStoryStore, StoryFilter } from "../../store/storyStore";
import { useInsightStore } from "../../store/insightStore";

const FilterPanel: React.FC = () => {
  const {
    filters: storeFilters,
    setFilter,
    clearFilters: storeClearFilters,
  } = useStoryStore();

  const { topDomains, fetchTopDomains } = useInsightStore();

  const [keyword, setKeyword] = useState(storeFilters.keyword || "");
  const [selectedDomain, setSelectedDomain] = useState(
    storeFilters.domain || "all"
  );
  const [storyType, setStoryType] = useState(() => {
    if (storeFilters.isAIRelated === true) return "ai";
    if (storeFilters.isAIRelated === false) return "non-ai";
    return "all";
  });
  const [startDate, setStartDate] = useState(storeFilters.startDate || "");
  const [endDate, setEndDate] = useState(storeFilters.endDate || "");

  useEffect(() => {
    fetchTopDomains(20);
  }, [fetchTopDomains]);

  useEffect(() => {
    setKeyword(storeFilters.keyword || "");
    setSelectedDomain(storeFilters.domain || "all");
    setStoryType(() => {
      if (storeFilters.isAIRelated === true) return "ai";
      if (storeFilters.isAIRelated === false) return "non-ai";
      return "all";
    });
    setStartDate(storeFilters.startDate || "");
    setEndDate(storeFilters.endDate || "");
  }, [storeFilters]);

  const handleApplyFilters = () => {
    const filtersToApply: Partial<StoryFilter> = {};

    if (keyword) {
      filtersToApply.keyword = keyword;
    } else {
      if (storeFilters.keyword !== undefined) {
        filtersToApply.keyword = undefined;
      }
    }

    if (selectedDomain && selectedDomain !== "all") {
      filtersToApply.domain = selectedDomain;
    } else {
      if (storeFilters.domain !== undefined) {
        filtersToApply.domain = undefined;
      }
    }

    if (storyType === "ai") {
      filtersToApply.isAIRelated = true;
    } else if (storyType === "non-ai") {
      filtersToApply.isAIRelated = false;
    } else {
      if (storeFilters.isAIRelated !== undefined) {
        filtersToApply.isAIRelated = undefined;
      }
    }

    if (startDate) {
      filtersToApply.startDate = startDate;
    } else {
      if (storeFilters.startDate !== undefined) {
        filtersToApply.startDate = undefined;
      }
    }

    if (endDate) {
      filtersToApply.endDate = endDate;
    } else {
      if (storeFilters.endDate !== undefined) {
        filtersToApply.endDate = undefined;
      }
    }

    if (
      Object.keys(filtersToApply).length > 0 ||
      (storeFilters.keyword && !keyword) ||
      (storeFilters.domain && selectedDomain === "all") ||
      (storeFilters.isAIRelated !== undefined && storyType === "all") ||
      (storeFilters.startDate && !startDate) ||
      (storeFilters.endDate && !endDate)
    ) {
      setFilter(filtersToApply);
    }
  };

  const handleClearFilters = () => {
    storeClearFilters();
  };

  return (
    <Paper sx={{ p: { xs: 2, sm: 3 }, mb: 3 }} elevation={0} variant="outlined">
      <Grid container spacing={2} alignItems="flex-start">
        <Grid size={{ xs: 12, md: 6, lg: 3 }}>
          <TextField
            fullWidth
            label="Search Keywords"
            variant="outlined"
            size="small"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            }}
          />
        </Grid>
        <Grid size={{ xs: 12, md: 6, lg: 2 }}>
          <FormControl fullWidth size="small">
            <InputLabel>Domain</InputLabel>
            <Select
              label="Domain"
              value={selectedDomain}
              onChange={(e: SelectChangeEvent<string>) =>
                setSelectedDomain(e.target.value)
              }
            >
              <MenuItem value="all">All Domains</MenuItem>
              {topDomains.map((domainStat) => (
                <MenuItem key={domainStat.domain} value={domainStat.domain}>
                  {domainStat.domain}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid size={{ xs: 12, md: 6, lg: 3 }}>
          <FormControl component="fieldset">
            <FormLabel
              component="legend"
              sx={{ fontSize: "0.8rem", mb: 0.5, fontWeight: "medium" }}
            >
              Story Type
            </FormLabel>
            <RadioGroup
              row
              value={storyType}
              onChange={(e) => setStoryType(e.target.value)}
              name="story-type-group"
            >
              <FormControlLabel
                value="all"
                control={<Radio size="small" />}
                label={<Typography variant="body2">All</Typography>}
              />
              <FormControlLabel
                value="ai"
                control={<Radio size="small" />}
                label={<Typography variant="body2">AI</Typography>}
              />
              <FormControlLabel
                value="non-ai"
                control={<Radio size="small" />}
                label={<Typography variant="body2">Non-AI</Typography>}
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid size={{ xs: 12, md: 6, lg: 4 }}>
          <FormLabel
            component="legend"
            sx={{ fontSize: "0.8rem", mb: 0.5, fontWeight: "medium" }}
          >
            Date Range
          </FormLabel>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
            <TextField
              type="date"
              label="Start Date"
              variant="outlined"
              size="small"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
            <TextField
              type="date"
              label="End Date"
              variant="outlined"
              size="small"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Stack>
        </Grid>
        <Grid
          size={{ xs: 12, md: 12, lg: 2 }}
          sx={{
            display: "flex",
            flexDirection: { xs: "column", sm: "row" },
            gap: 1,
            pt: { md: 3.5, lg: 3.5 },
          }}
        >
          <Button
            fullWidth
            variant="contained"
            startIcon={<FilterAltIcon />}
            onClick={handleApplyFilters}
            sx={{ py: "10px" }}
          >
            Apply
          </Button>
          <Button
            fullWidth
            variant="outlined"
            startIcon={<RestartAltIcon />}
            onClick={handleClearFilters}
            sx={{ py: "10px" }}
          >
            Clear
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default FilterPanel;
