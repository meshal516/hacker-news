import React, { useEffect } from "react";
import {
  Box,
  Grid,
  Paper,
  Typography,
  Avatar,
  Card,
  CircularProgress,
  Alert,
} from "@mui/material";
import { Article, Assessment, Insights } from "@mui/icons-material";
import KeywordFrequencyChart from "../components/Dashboard/KeywordFrequencyChart";
import TopDomainsChart from "../components/Dashboard/TopDomainsChart";
import { useInsightStore } from "../store/insightStore";

interface SummaryCardProps {
  title: string;
  value: string | number;
  icon: React.ReactElement;
  avatarColor?: string;
}

const SummaryCard: React.FC<SummaryCardProps> = ({
  title,
  value,
  icon,
  avatarColor,
}) => {
  return (
    <Card
      sx={{ display: "flex", alignItems: "center", p: 2, height: "100%" }}
      elevation={2}
    >
      <Avatar
        sx={{
          bgcolor: avatarColor || "primary.main",
          width: 50,
          height: 50,
          mr: 2,
        }}
      >
        {icon}
      </Avatar>
      <Box>
        <Typography variant="body2" color="text.secondary">
          {title}
        </Typography>
        <Typography variant="h5" component="div" fontWeight="bold">
          {value}
        </Typography>
      </Box>
    </Card>
  );
};

const Dashboard: React.FC = () => {
  const {
    statsSummary,
    fetchStatsSummary,
    isLoading: insightsLoading,
    error: insightsError,
  } = useInsightStore();

  useEffect(() => {
    fetchStatsSummary();
  }, [fetchStatsSummary]);

  const summaryData: SummaryCardProps[] = statsSummary
    ? [
        {
          title: "Total Stories Processed",
          value: statsSummary.total_stories.toLocaleString(),
          icon: <Article />,
          avatarColor: "primary.light",
        },
        {
          title: "AI Related Stories",
          value: statsSummary.ai_related_count.toLocaleString(),
          icon: <Insights />,
          avatarColor: "secondary.light",
        },
        {
          title: "Unique Domains Tracked",
          value: statsSummary.unique_domains.toLocaleString(),
          icon: <Assessment />,
          avatarColor: "info.light",
        },
      ]
    : [];

  return (
    <Box sx={{ p: { xs: 2, sm: 3 }, flexGrow: 1 }}>
      {" "}
      {/* Responsive padding */}
      <Typography
        variant="h4"
        component="h1"
        gutterBottom
        sx={{ fontWeight: "bold", mb: 1 }}
      >
        Analytics Dashboard
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 4 }}>
        Overview of Hacker News story analytics and trends.
      </Typography>
      {insightsLoading && !statsSummary && (
        <Box sx={{ display: "flex", justifyContent: "center", my: 4 }}>
          <CircularProgress />
        </Box>
      )}
      {insightsError && (
        <Alert severity="error" sx={{ my: 2 }}>
          Error loading summary statistics: {insightsError}
        </Alert>
      )}
      {!insightsLoading &&
        !insightsError &&
        statsSummary &&
        summaryData.length > 0 && (
          <Grid container spacing={{ xs: 2, md: 3 }} sx={{ mb: 4 }}>
            {summaryData.map((item, index) => (
              <Grid size={{ xs: 12, md: 6, lg: 4 }} key={index}>
                <SummaryCard
                  title={item.title}
                  value={item.value}
                  icon={item.icon}
                  avatarColor={item.avatarColor}
                />
              </Grid>
            ))}
          </Grid>
        )}
      <Grid container spacing={{ xs: 2, md: 3 }}>
        <Grid size={{ xs: 12, md: 6, lg: 4 }}>
          <Paper
            elevation={2}
            sx={{
              p: { xs: 1.5, sm: 2.5 },
              height: "420px",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <Typography variant="h6" gutterBottom sx={{ mb: 1 }}>
              Keyword Frequency
            </Typography>
            <Box sx={{ flexGrow: 1, minHeight: 0 }}>
              {" "}
              {/* Ensure Box can shrink and grow */}
              <KeywordFrequencyChart />
            </Box>
          </Paper>
        </Grid>
        <Grid size={{ xs: 12, lg: 6 }}>
          <Paper
            elevation={2}
            sx={{
              p: { xs: 1.5, sm: 2.5 },
              height: "420px",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <Typography variant="h6" gutterBottom sx={{ mb: 1 }}>
              Top Domains
            </Typography>
            <Box sx={{ flexGrow: 1, minHeight: 0 }}>
              {" "}
              {/* Ensure Box can shrink and grow */}
              <TopDomainsChart />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
