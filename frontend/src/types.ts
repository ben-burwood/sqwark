export interface Feedback {
  id: string;
  text: string;
  tags: string[];
  created_at: string;
}

export interface TagCount {
  name: string;
  count: number;
}
