export interface User {
  id: string;
  username: string;
  displayName: string;
  avatar?: string;
}

export interface Post {
  id: string;
  userId: string;
  content: string;
  createdAt: Date;
  likes: string[]; // User IDs who liked
  comments: Comment[];
}

export interface Comment {
  id: string;
  userId: string;
  content: string;
  createdAt: Date;
}

export interface CreatePostRequest {
  content: string;
  userId: string;
}

export interface AIGenerateRequest {
  prompt: string;
}

export interface AIGenerateResponse {
  content: string;
}
