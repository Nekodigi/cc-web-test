'use client';

import { useState, useEffect } from 'react';
import PostCard from '@/components/PostCard';
import PostForm from '@/components/PostForm';
import { Post, User } from '@/types';

export default function Home() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [currentUserId, setCurrentUserId] = useState('1'); // デモ用：デフォルトでAliceとしてログイン
  const [isLoading, setIsLoading] = useState(true);

  // 初期データの読み込み
  useEffect(() => {
    loadPosts();
    loadUsers();
  }, []);

  const loadPosts = async () => {
    try {
      const response = await fetch('/api/posts');
      const data = await response.json();
      setPosts(data);
    } catch (error) {
      console.error('Failed to load posts:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadUsers = async () => {
    // 実際のアプリではAPIから取得
    setUsers([
      { id: '1', username: 'alice', displayName: 'Alice', avatar: '👩' },
      { id: '2', username: 'bob', displayName: 'Bob', avatar: '👨' },
      { id: '3', username: 'ai_assistant', displayName: 'AI Assistant', avatar: '🤖' },
    ]);
  };

  const handleCreatePost = async (content: string) => {
    try {
      const response = await fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, userId: currentUserId }),
      });

      if (response.ok) {
        await loadPosts();
      }
    } catch (error) {
      console.error('Failed to create post:', error);
    }
  };

  const handleLike = async (postId: string) => {
    try {
      const response = await fetch(`/api/posts/${postId}/like`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: currentUserId }),
      });

      if (response.ok) {
        await loadPosts();
      }
    } catch (error) {
      console.error('Failed to like post:', error);
    }
  };

  const handleComment = async (postId: string, content: string) => {
    try {
      const response = await fetch(`/api/posts/${postId}/comment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: currentUserId, content }),
      });

      if (response.ok) {
        await loadPosts();
      }
    } catch (error) {
      console.error('Failed to comment:', error);
    }
  };

  const handleDelete = async (postId: string) => {
    if (!confirm('この投稿を削除しますか？')) return;

    try {
      const response = await fetch(`/api/posts/${postId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        await loadPosts();
      }
    } catch (error) {
      console.error('Failed to delete post:', error);
    }
  };

  const currentUser = users.find((u) => u.id === currentUserId);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* ヘッダー */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text">
              🤖 AI SNS
            </h1>
            <div className="flex items-center gap-3">
              <span className="text-2xl">{currentUser?.avatar}</span>
              <div className="hidden sm:block">
                <div className="font-semibold text-gray-900">
                  {currentUser?.displayName}
                </div>
                <div className="text-sm text-gray-500">
                  @{currentUser?.username}
                </div>
              </div>
              <select
                value={currentUserId}
                onChange={(e) => setCurrentUserId(e.target.value)}
                className="ml-2 px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.displayName}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </header>

      {/* メインコンテンツ */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* 投稿フォーム */}
        <PostForm onSubmit={handleCreatePost} />

        {/* 投稿リスト */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">読み込み中...</p>
          </div>
        ) : posts.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-6xl mb-4">📝</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              まだ投稿がありません
            </h3>
            <p className="text-gray-600">
              最初の投稿を作成して、SNSを始めましょう！
            </p>
          </div>
        ) : (
          <div>
            {posts.map((post) => {
              const user = users.find((u) => u.id === post.userId);
              if (!user) return null;

              return (
                <PostCard
                  key={post.id}
                  post={post}
                  user={user}
                  currentUserId={currentUserId}
                  onLike={handleLike}
                  onComment={handleComment}
                  onDelete={handleDelete}
                  users={users}
                />
              );
            })}
          </div>
        )}
      </main>

      {/* フッター */}
      <footer className="bg-white mt-12 border-t">
        <div className="max-w-4xl mx-auto px-4 py-6 text-center text-gray-600 text-sm">
          <p>AI機能付きSNSアプリ - Claude Powered</p>
          <p className="mt-2">
            🤖 AI機能: 投稿の自動生成、コメントの提案
          </p>
        </div>
      </footer>
    </div>
  );
}
