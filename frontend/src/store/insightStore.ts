import { create } from "zustand";
import {
  fetchKeywordFrequency,
  fetchTopDomains,
  fetchStatsSummary,
} from "../api/insights";

export interface KeywordFrequency {
  keyword: string;
  count: number;
}

export interface DomainStats {
  domain: string;
  count: number;
  last_updated: string;
}

interface StatsSummary {
  total_stories: number;
  ai_related_count: number;
  ai_percentage: number;
  unique_domains: number;
  avg_score: number;
  avg_comments: number;
}

interface InsightState {
  keywordFrequency: KeywordFrequency[];
  topDomains: DomainStats[];
  statsSummary: StatsSummary | null;
  isLoading: boolean;
  error: string | null;
  fetchKeywordFrequency: () => Promise<void>;
  fetchTopDomains: (limit?: number) => Promise<void>;
  fetchStatsSummary: () => Promise<void>;
  fetchAllInsights: () => Promise<void>;
}

export const useInsightStore = create<InsightState>((set) => ({
  keywordFrequency: [],
  topDomains: [],
  statsSummary: null,
  isLoading: false,
  error: null,

  fetchKeywordFrequency: async () => {
    try {
      set({ isLoading: true, error: null });
      const data = await fetchKeywordFrequency();
      set({ keywordFrequency: data, isLoading: false });
    } catch (error) {
      set({
        error: "Failed to fetch keyword frequency",
        isLoading: false,
      });
    }
  },

  fetchTopDomains: async (limit = 10) => {
    try {
      set({ isLoading: true, error: null });
      const data = await fetchTopDomains(limit);
      set({ topDomains: data, isLoading: false });
    } catch (error) {
      set({
        error: "Failed to fetch top domains",
        isLoading: false,
      });
    }
  },

  fetchStatsSummary: async () => {
    try {
      set({ isLoading: true, error: null });
      const data = await fetchStatsSummary();
      set({ statsSummary: data, isLoading: false });
    } catch (error) {
      set({
        error: "Failed to fetch statistics summary",
        isLoading: false,
      });
    }
  },

  fetchAllInsights: async () => {
    try {
      set({ isLoading: true, error: null });
      await Promise.all([
        fetchKeywordFrequency().then((data) => set({ keywordFrequency: data })),
        fetchTopDomains().then((data) => set({ topDomains: data })),
        fetchStatsSummary().then((data) => set({ statsSummary: data })),
      ]);
      set({ isLoading: false });
    } catch (error) {
      set({
        error: "Failed to fetch insights",
        isLoading: false,
      });
    }
  },
}));
