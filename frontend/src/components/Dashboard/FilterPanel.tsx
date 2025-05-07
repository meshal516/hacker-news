import { useTheme } from "../../contexts/ThemeContext";

const FilterPanel = () => {
  const { isDark } = useTheme();

  return (
    <div
      className={`rounded-xl p-6 shadow-sm ${
        isDark ? "bg-gray-800" : "bg-white"
      }`}
    >
      <h2 className="text-xl font-semibold mb-6 dark:text-white">
        Advanced Filters
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium mb-2 dark:text-gray-300">
            Keyword
          </label>
          <input
            type="text"
            className={`w-full px-4 py-2 rounded-lg border ${
              isDark
                ? "bg-gray-700 border-gray-600 text-white"
                : "bg-white border-gray-300"
            } focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
            placeholder="Search stories..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 dark:text-gray-300">
            Date Range
          </label>
          <div className="flex gap-2">
            <input
              type="date"
              className={`flex-1 px-4 py-2 rounded-lg border ${
                isDark
                  ? "bg-gray-700 border-gray-600 text-white"
                  : "bg-white border-gray-300"
              }`}
            />
            <span className="self-center text-gray-500">to</span>
            <input
              type="date"
              className={`flex-1 px-4 py-2 rounded-lg border ${
                isDark
                  ? "bg-gray-700 border-gray-600 text-white"
                  : "bg-white border-gray-300"
              }`}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 dark:text-gray-300">
            Domain
          </label>
          <select
            className={`w-full px-4 py-2 rounded-lg border ${
              isDark
                ? "bg-gray-700 border-gray-600 text-white"
                : "bg-white border-gray-300"
            }`}
          >
            <option>All Domains</option>
            <option>news.com</option>
            <option>blog.org</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 dark:text-gray-300">
            AI Related
          </label>
          <div className="flex space-x-4">
            <label className="flex items-center">
              <input type="radio" name="ai-related" className="mr-2" />
              <span className="dark:text-gray-300">All</span>
            </label>
            <label className="flex items-center">
              <input type="radio" name="ai-related" className="mr-2" />
              <span className="dark:text-gray-300">AI Only</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FilterPanel;
