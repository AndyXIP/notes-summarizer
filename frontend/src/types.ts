export interface Note {
  id: number;
  title: string;
  content: string;
  summary?: string | null;
  timestamp: string;
}