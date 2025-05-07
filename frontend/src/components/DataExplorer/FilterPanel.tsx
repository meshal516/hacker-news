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
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import FilterAltIcon from "@mui/icons-material/FilterAlt";

const FilterPanel: React.FC = () => {
  return (
    <Paper sx={{ p: { xs: 2, sm: 3 } }} elevation={0} variant="outlined">
      <Grid container spacing={3} alignItems="center">
        <Grid size={{ xs: 12, md: 6, lg: 5 }}>
          <TextField
            fullWidth
            label="Search Keywords"
            variant="outlined"
            size="small"
            slotProps={{
              inputLabel: { shrink: true },
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon fontSize="small" />
                  </InputAdornment>
                ),
              },
            }}
          />
        </Grid>
        <Grid size={{ xs: 12, md: 6, lg: 4 }}>
          <FormControl fullWidth size="small">
            <InputLabel>Domain</InputLabel>
            <Select label="Domain" defaultValue="all">
              <MenuItem value="all">All Domains</MenuItem>
              <MenuItem value="techcrunch.com">techcrunch.com</MenuItem>
              <MenuItem value="github.com">github.com</MenuItem>
              <MenuItem value="medium.com">medium.com</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid size={{ xs: 12, md: 12, lg: 3 }}>
          <FormControl component="fieldset">
            <FormLabel
              component="legend"
              sx={{ fontSize: "0.8rem", mb: 0.5, fontWeight: "medium" }}
            >
              Story Type
            </FormLabel>
            <RadioGroup row defaultValue="all" name="ai-related-group">
              <FormControlLabel
                value="all"
                control={<Radio size="small" />}
                label={<Typography variant="body2">All</Typography>}
              />
              <FormControlLabel
                value="ai"
                control={<Radio size="small" />}
                label={<Typography variant="body2">AI Related</Typography>}
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid size={{ xs: 12, lg: 9 }}>
          <Typography
            variant="caption"
            display="block"
            gutterBottom
            color="text.secondary"
            sx={{ mb: 1, fontWeight: "medium" }}
          >
            Date Range
          </Typography>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
            <TextField
              type="date"
              label="Start Date"
              variant="outlined"
              size="small"
              slotProps={{ inputLabel: { shrink: true } }}
              fullWidth
            />
            <TextField
              type="date"
              label="End Date"
              variant="outlined"
              size="small"
              slotProps={{ inputLabel: { shrink: true } }}
              fullWidth
            />
          </Stack>
        </Grid>
        <Grid
          size={{ xs: 12, lg: 3 }}
          sx={{ display: "flex", alignItems: "flex-end" }}
        >
          <Button
            fullWidth
            variant="contained"
            startIcon={<FilterAltIcon />}
            sx={{ py: "10px" }}
          >
            Apply Filters
          </Button>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default FilterPanel;
