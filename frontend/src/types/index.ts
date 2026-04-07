export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface SpecificationContent {
  goal: string;
  description: string;
  functional_requirements: string[];
  db_requirements: string[];
  tech_stack: string[];
  features: string[];
}

export interface Specification {
  id: string;
  user_id: string | null;
  title: string;
  content: SpecificationContent;
  type: string;
  complexity: number;
  created_at: string;
}

export interface SharedLink {
  token: string;
  url: string;
}

export interface TrelloExport {
  board_name: string;
  lists: Array<{
    name: string;
    cards: Array<{ name: string }>;
  }>;
}

export type ProjectType = 'Web' | 'Mobile' | 'Game' | 'Corp IS' | 'Other';
export type ComplexityLevel = 1 | 2 | 3 | 4;