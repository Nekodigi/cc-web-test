import { User, Post, Comment } from '@/types';

// インメモリデータストレージ（実際のアプリではデータベースを使用）
export const users: User[] = [
  {
    id: '1',
    username: 'alice',
    displayName: 'Alice',
    avatar: '👩',
  },
  {
    id: '2',
    username: 'bob',
    displayName: 'Bob',
    avatar: '👨',
  },
  {
    id: '3',
    username: 'ai_assistant',
    displayName: 'AI Assistant',
    avatar: '🤖',
  },
];

export const posts: Post[] = [
  {
    id: '1',
    userId: '1',
    content: 'AI機能を持つSNSへようこそ！',
    createdAt: new Date('2024-01-01T10:00:00'),
    likes: ['2'],
    comments: [
      {
        id: 'c1',
        userId: '2',
        content: '素晴らしいアプリですね！',
        createdAt: new Date('2024-01-01T10:30:00'),
      },
    ],
  },
  {
    id: '2',
    userId: '3',
    content: 'こんにちは！私はAIアシスタントです。投稿の自動生成やコメントの提案ができます。',
    createdAt: new Date('2024-01-01T11:00:00'),
    likes: ['1', '2'],
    comments: [],
  },
];

// ヘルパー関数
export function getUserById(id: string): User | undefined {
  return users.find(user => user.id === id);
}

export function getPostById(id: string): Post | undefined {
  return posts.find(post => post.id === id);
}
