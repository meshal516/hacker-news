import React, { useEffect } from "react";
import { DataGrid, GridColDef, GridRowParams } from "@mui/x-data-grid";
import {
  Typography,
  Chip,
  Checkbox,
  CircularProgress,
  Box,
  Alert,
} from "@mui/material";
import { format } from "date-fns";
import { useStoryStore } from "../../store/storyStore";

const columns: GridColDef[] = [
  {
    field: "title",
    headerName: "Title",
    flex: 2,
    renderCell: (params) => (
      <Typography variant="body2" noWrap>
        {params.value}
      </Typography>
    ),
  },
  { field: "domain", headerName: "Domain", flex: 1 },
  {
    field: "score",
    headerName: "Score",
    align: "center",
    renderCell: (params) => (
      <Chip
        label={params.value}
        color={params.value > 50 ? "primary" : "default"}
      />
    ),
  },
  { field: "comments_count", headerName: "Comments", align: "center" },
  {
    field: "timestamp",
    headerName: "Date",
    flex: 1,
    valueFormatter: (value: string | Date) =>
      format(new Date(value), "MMM d, yyyy"),
  },
  {
    field: "is_ai_related",
    headerName: "AI Related",
    align: "center",
    renderCell: (params) => <Checkbox checked={params.value} color="primary" />,
  },
];

const StoryTable: React.FC = () => {
  const { stories, isLoading, error, fetchStories, filters } = useStoryStore();

  useEffect(() => {
    fetchStories();
  }, [fetchStories, filters]);

  if (isLoading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: 400,
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: 400,
        }}
      >
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }
  return (
    <div style={{ height: 600, width: "100%" }}>
      <DataGrid
        rows={stories}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: { pageSize: 10, page: 0 },
          },
        }}
        pageSizeOptions={[5, 10, 20]}
        showToolbar
        slotProps={{
          toolbar: {
            showQuickFilter: true,
            quickFilterProps: { debounceMs: 500 },
          },
        }}
        sx={{
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: "background.paper",
          },
        }}
        getRowClassName={(params: GridRowParams<{ id: number }>) =>
          Number(params.id) % 2 === 0 ? "even" : "odd"
        }
      />
    </div>
  );
};

export default StoryTable;
