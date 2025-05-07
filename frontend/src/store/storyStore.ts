import create from "zustand";
import { fetchStories, fetchAIRelatedStories } from "../api/stories";

export interface StoryFilter {
  keyword?: string;
  domain?: string;
  startDate?: string;
  endDate?: string;
  isAIRelated?: boolean;
}

interface Story {
  id: number;
  title: string;
  url: string;
  domain: string;
  score: number;
  comments_count: number;
  author: string;
  timestamp: string;
  is_ai_related: boolean;
}

interface StoryState {
  stories: Story[];
  filteredStories: Story[];
  filters: StoryFilter;
  isLoading: boolean;
  error: string | null;
  fetchStories: () => Promise<void>;
  fetchAIRelatedStories: () => Promise<void>;
  setFilter: (filter: Partial<StoryFilter>) => void;
  clearFilters: () => void;
}

export const useStoryStore = create<StoryState>((set, get) => ({
  stories: [],
  filteredStories: [],
  filters: {},
  isLoading: false,
  error: null,

  fetchStories: async () => {
    try {
      set({ isLoading: true, error: null });
      const stories = await fetchStories(get().filters);
      set({
        stories,
        filteredStories: stories,
        isLoading: false,
      });
    } catch (error) {
      set({
        error: "Failed to fetch stories",
        isLoading: false,
      });
    }
  },

  fetchAIRelatedStories: async () => {
    try {
      set({ isLoading: true, error: null });
      const stories = await fetchAIRelatedStories();
      set({
        stories,
        filteredStories: stories,
        isLoading: false,
        filters: { ...get().filters, isAIRelated: true },
      });
    } catch (error) {
      set({
        error: "Failed to fetch AI-related stories",
        isLoading: false,
      });
    }
  },

  setFilter: (filter) => {
    const newFilters = { ...get().filters, ...filter };
    set({ filters: newFilters });
    get().fetchStories();
  },

  clearFilters: () => {
    set({ filters: {} });
    get().fetchStories();
  },
}));
