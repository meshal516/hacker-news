import { DataGrid, GridColDef, GridRowParams } from "@mui/x-data-grid";
import { Typography, Chip, Checkbox } from "@mui/material";
import { format } from "date-fns";

// Mock data for stories
const stories = [
  {
    id: 1,
    title: "AI Takes Over The World",
    domain: "techcrunch.com",
    score: 150,
    comments_count: 42,
    timestamp: new Date().toISOString(),
    is_ai_related: true,
  },
  {
    id: 2,
    title: "New JavaScript Framework Released",
    domain: "dev.to",
    score: 90,
    comments_count: 23,
    timestamp: new Date().toISOString(),
    is_ai_related: false,
  },
  {
    id: 3,
    title: "Understanding Quantum Computing",
    domain: "medium.com",
    score: 120,
    comments_count: 30,
    timestamp: new Date().toISOString(),
    is_ai_related: true,
  },
  {
    id: 4,
    title: "The Future of Remote Work",
    domain: "forbes.com",
    score: 75,
    comments_count: 15,
    timestamp: new Date().toISOString(),
    is_ai_related: false,
  },
  {
    id: 5,
    title: "Advanced AI in Medical Diagnosis",
    domain: "nature.com",
    score: 200,
    comments_count: 55,
    timestamp: new Date().toISOString(),
    is_ai_related: true,
  },
];

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
