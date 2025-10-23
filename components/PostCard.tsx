'use client';

import { Post, User } from '@/types';
import { useState } from 'react';

interface PostCardProps {
  post: Post;
  user: User;
  currentUserId: string;
  onLike: (postId: string) => void;
  onComment: (postId: string, content: string) => void;
  onDelete?: (postId: string) => void;
  users: User[];
}

export default function PostCard({
  post,
  user,
  currentUserId,
  onLike,
  onComment,
  onDelete,
  users,
}: PostCardProps) {
  const [commentText, setCommentText] = useState('');
  const [showComments, setShowComments] = useState(false);
  const [isAIGenerating, setIsAIGenerating] = useState(false);

  const isLiked = post.likes.includes(currentUserId);
  const canDelete = post.userId === currentUserId;

  const handleComment = () => {
    if (commentText.trim()) {
      onComment(post.id, commentText);
      setCommentText('');
    }
  };

  const handleAIComment = async () => {
    setIsAIGenerating(true);
    try {
      const response = await fetch('/api/ai/suggest-comment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ postContent: post.content }),
      });
      const data = await response.json();
      setCommentText(data.content);
    } catch (error) {
      console.error('AI comment generation failed:', error);
    } finally {
      setIsAIGenerating(false);
    }
  };

  const formatDate = (date: Date) => {
    return new Date(date).toLocaleString('ja-JP', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3 mb-4">
          <div className="text-3xl">{user.avatar}</div>
          <div>
            <h3 className="font-bold text-gray-900">{user.displayName}</h3>
            <p className="text-sm text-gray-500">@{user.username}</p>
          </div>
        </div>
        {canDelete && onDelete && (
          <button
            onClick={() => onDelete(post.id)}
            className="text-red-500 hover:text-red-700 text-sm"
          >
            削除
          </button>
        )}
      </div>

      <p className="text-gray-800 mb-4 whitespace-pre-wrap">{post.content}</p>

      <div className="flex items-center gap-4 mb-4 text-sm text-gray-500">
        <span>{formatDate(post.createdAt)}</span>
      </div>

      <div className="flex gap-4 mb-4">
        <button
          onClick={() => onLike(post.id)}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg transition ${
            isLiked
              ? 'bg-red-100 text-red-600'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          {isLiked ? '❤️' : '🤍'} {post.likes.length}
        </button>
        <button
          onClick={() => setShowComments(!showComments)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 transition"
        >
          💬 {post.comments.length}
        </button>
      </div>

      {showComments && (
        <div className="border-t pt-4">
          <div className="space-y-3 mb-4">
            {post.comments.map((comment) => {
              const commentUser = users.find((u) => u.id === comment.userId);
              return (
                <div key={comment.id} className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xl">{commentUser?.avatar}</span>
                    <span className="font-semibold text-sm">
                      {commentUser?.displayName}
                    </span>
                    <span className="text-xs text-gray-500">
                      {formatDate(comment.createdAt)}
                    </span>
                  </div>
                  <p className="text-gray-700 text-sm">{comment.content}</p>
                </div>
              );
            })}
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleComment()}
              placeholder="コメントを入力..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleAIComment}
              disabled={isAIGenerating}
              className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition disabled:opacity-50"
              title="AIがコメントを提案"
            >
              {isAIGenerating ? '⏳' : '🤖'}
            </button>
            <button
              onClick={handleComment}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
            >
              送信
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
