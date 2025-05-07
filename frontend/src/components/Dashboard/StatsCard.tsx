import { useTheme } from "../../contexts/ThemeContext";

const StatsCard = ({
  title,
  value,
  icon,
  trend,
}: {
  title: string;
  value: string;
  icon: string;
  trend: number;
}) => {
  const { isDark } = useTheme();

  return (
    <div
      className={`p-6 rounded-xl ${
        isDark ? "bg-gray-800" : "bg-white"
      } shadow-sm`}
    >
      <div className="flex justify-between items-start">
        <div>
          <p
            className={`text-sm ${isDark ? "text-gray-400" : "text-gray-600"}`}
          >
            {title}
          </p>
          <p
            className={`text-3xl font-bold mt-2 ${
              isDark ? "text-white" : "text-gray-900"
            }`}
          >
            {value}
          </p>
        </div>
        <div
          className={`p-3 rounded-lg ${isDark ? "bg-gray-700" : "bg-gray-100"}`}
        >
          <span className="text-2xl">{icon}</span>
        </div>
      </div>
      <div className="mt-4 flex items-center">
        <span
          className={`text-sm ${
            trend > 0
              ? "text-green-600 dark:text-green-400"
              : "text-red-600 dark:text-red-400"
          }`}
        >
          {trend > 0 ? "↑" : "↓"} {Math.abs(trend)}%
        </span>
        <span className="ml-2 text-sm text-gray-500 dark:text-gray-400">
          vs last month
        </span>
      </div>
    </div>
  );
};

export default StatsCard;
