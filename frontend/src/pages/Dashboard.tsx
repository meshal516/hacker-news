import React from "react";
import { Box, Grid, Paper, Typography, Avatar, Card } from "@mui/material";
import { Article, Assessment, Insights } from "@mui/icons-material";
import KeywordFrequencyChart from "../components/Dashboard/KeywordFrequencyChart";
import TopDomainsChart from "../components/Dashboard/TopDomainsChart";

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
  // Mock data for summary cards
  const summaryStats = {
    totalStories: 1234,
    aiRelatedCount: 568,
    uniqueDomains: 240,
    avgScore: 34.8,
  };

  const summaryData: SummaryCardProps[] = [
    {
      title: "Total Stories",
      value: summaryStats.totalStories.toLocaleString(),
      icon: <Article />,
      avatarColor: "primary.light",
    },
    {
      title: "AI Related Stories",
      value: summaryStats.aiRelatedCount.toLocaleString(),
      icon: <Insights />,
      avatarColor: "secondary.light",
    },
    {
      title: "Unique Domains",
      value: summaryStats.uniqueDomains.toLocaleString(),
      icon: <Assessment />,
      avatarColor: "info.light",
    },
  ];

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
      <Grid container spacing={{ xs: 2, md: 3 }} sx={{ mb: 4 }}>
        {summaryData.map((item, index) => (
          <Grid size={{ xs: 12, lg: 6 }} key={index}>
            {" "}
            {/* Adjusted lg for 4 cards */}
            <SummaryCard
              title={item.title}
              value={item.value}
              icon={item.icon}
              avatarColor={item.avatarColor}
            />
          </Grid>
        ))}
      </Grid>
      <Grid container spacing={{ xs: 2, md: 3 }}>
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
