import React, { useEffect, useRef } from "react";
import { useInsightStore } from "../../store/insightStore";
import { Pie } from "react-chartjs-2";
import { useTheme } from "../../contexts/ThemeContext";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import type { DomainStats } from "../../store/insightStore";

ChartJS.register(ArcElement, Tooltip, Legend);

const TopDomainsChart: React.FC = () => {
  const { topDomains, fetchTopDomains, isLoading, error } = useInsightStore();
  const { isDark } = useTheme();
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // fetchTopDomains(10); // We'll comment this out for now to use mock data
    // Simulate fetching mock data
    const mockData: DomainStats[] = [
      { domain: "github.com", count: 120, last_updated: "2023-10-26" },
      { domain: "stackoverflow.com", count: 100, last_updated: "2023-10-26" },
      { domain: "medium.com", count: 80, last_updated: "2023-10-26" },
      { domain: "dev.to", count: 70, last_updated: "2023-10-26" },
      { domain: "freecodecamp.org", count: 60, last_updated: "2023-10-26" },
      { domain: "reddit.com", count: 50, last_updated: "2023-10-26" },
      { domain: "news.ycombinator.com", count: 40, last_updated: "2023-10-26" },
      { domain: "producthunt.com", count: 30, last_updated: "2023-10-26" },
      { domain: "indiehackers.com", count: 20, last_updated: "2023-10-26" },
      { domain: "hashnode.com", count: 10, last_updated: "2023-10-26" },
    ];

    useInsightStore.setState({ topDomains: mockData, isLoading: false });
  }, [fetchTopDomains]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-full">
        <div
          className={`animate-spin rounded-full h-8 w-8 border-b-2 ${
            isDark ? "border-white" : "border-indigo-500"
          }`}
        ></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-full">
        <div className="text-red-500">Error loading data</div>
      </div>
    );
  }

  if (!topDomains || topDomains.length === 0) {
    return (
      <div className="flex justify-center items-center h-full">
        <div
          className={`text-center ${
            isDark ? "text-gray-400" : "text-gray-500"
          }`}
        >
          No data available
        </div>
      </div>
    );
  }

  // Prepare chart data
  const labels = topDomains.map((item) => item.domain);
  const counts = topDomains.map((item) => item.count);

  // Generate pleasant colors
  const backgroundColors = [
    "rgba(79, 70, 229, 0.8)", // Indigo
    "rgba(59, 130, 246, 0.8)", // Blue
    "rgba(16, 185, 129, 0.8)", // Green
    "rgba(245, 158, 11, 0.8)", // Amber
    "rgba(239, 68, 68, 0.8)", // Red
    "rgba(217, 70, 239, 0.8)", // Purple
    "rgba(236, 72, 153, 0.8)", // Pink
    "rgba(6, 182, 212, 0.8)", // Cyan
    "rgba(52, 211, 153, 0.8)", // Emerald
    "rgba(124, 58, 237, 0.8)", // Violet
  ];

  const borderColors = backgroundColors.map((color) =>
    color.replace("0.8", "1")
  );

  const chartData = {
    labels: labels,
    datasets: [
      {
        data: counts,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    onHover: (event: any, chartElements: any) => {
      if (event.native) {
        const target = event.native.target as HTMLElement;
        if (chartElements.length > 0) {
          target.style.cursor = "pointer";
        } else {
          target.style.cursor = "default";
        }
      }
    },
    onClick: (event: any, elements: any) => {
      if (elements.length > 0) {
        const chart = event.chart;
        const elementIndex = elements[0].index;
        const clickedDomain = chart.data.labels[elementIndex];
        const clickedCount = chart.data.datasets[0].data[elementIndex];
        console.log(`Clicked Domain: ${clickedDomain}, Count: ${clickedCount}`);
        // Potential future enhancement:
        // navigateToKeywordSearch(clickedKeyword);
        // or setFilterByKeyword(clickedKeyword);
      }
    },
    plugins: {
      legend: {
        position: "right" as const,
        labels: {
          color: isDark ? "#e5e7eb" : "#4b5563",
          boxWidth: 15,
          padding: 15,
        },
      },
      tooltip: {
        callbacks: {
          label: function (context: any) {
            const value = context.raw;
            const total = context.dataset.data.reduce(
              (acc: number, data: number) => acc + data,
              0
            );
            const percentage = ((value / total) * 100).toFixed(1);
            return `${context.label}: ${value} (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <div ref={chartRef} className="h-full">
      <Pie data={chartData} options={options} />
    </div>
  );
};

export default TopDomainsChart;
