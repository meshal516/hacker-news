import React, { useEffect, useRef } from "react";
import { useInsightStore } from "../../store/insightStore";
import { Bar } from "react-chartjs-2";
import { useTheme } from "../../contexts/ThemeContext";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const KeywordFrequencyChart: React.FC = () => {
  const { keywordFrequency, fetchKeywordFrequency, isLoading, error } =
    useInsightStore();
  const { isDark } = useTheme();
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchKeywordFrequency();
  }, [fetchKeywordFrequency]);

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

  if (!keywordFrequency || Object.keys(keywordFrequency).length === 0) {
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

  const sortedData = [...keywordFrequency] // Create a shallow copy before sorting
    .sort((a, b) => b.count - a.count) // Sort by count in descending order
    .slice(0, 10); // Take top 10

  const labels = sortedData.map((item) => item.keyword);
  const data = sortedData.map((item) => item.count);

  const chartData = {
    labels,
    datasets: [
      {
        label: "Frequency",
        data,
        backgroundColor: isDark
          ? "rgba(129, 140, 248, 0.8)"
          : "rgba(79, 70, 229, 0.8)",
        borderColor: isDark ? "rgba(129, 140, 248, 1)" : "rgba(79, 70, 229, 1)",
        borderWidth: 1,
        borderRadius: 4,
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
        const clickedKeyword = chart.data.labels[elementIndex];
        const clickedFrequency = chart.data.datasets[0].data[elementIndex];
        console.log(
          `Clicked Keyword: ${clickedKeyword}, Frequency: ${clickedFrequency}`
        );
        // Potential future enhancement:
        // navigateToKeywordSearch(clickedKeyword);
        // or setFilterByKeyword(clickedKeyword);
      }
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: isDark
          ? "rgba(30, 41, 59, 0.8)"
          : "rgba(255, 255, 255, 0.8)",
        titleColor: isDark ? "#fff" : "#111827",
        bodyColor: isDark ? "#e5e7eb" : "#4b5563",
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: isDark ? "#9ca3af" : "#6b7280",
          maxRotation: 45,
          minRotation: 45,
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          color: isDark ? "rgba(75, 85, 99, 0.2)" : "rgba(229, 231, 235, 0.5)",
        },
        ticks: {
          color: isDark ? "#9ca3af" : "#6b7280",
          precision: 0,
        },
      },
    },
  };

  return (
    <div ref={chartRef} className="h-full">
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default KeywordFrequencyChart;
