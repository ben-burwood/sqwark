export interface Feedback {
  id: string;
  text: string;
  tags: string[];
  created_at: string;
  is_archived: boolean;
}

export interface TagCount {
  name: string;
  count: number;
}
