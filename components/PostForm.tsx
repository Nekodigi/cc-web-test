'use client';

import { useState } from 'react';

interface PostFormProps {
  onSubmit: (content: string) => void;
}

export default function PostForm({ onSubmit }: PostFormProps) {
  const [content, setContent] = useState('');
  const [isAIGenerating, setIsAIGenerating] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (content.trim()) {
      onSubmit(content);
      setContent('');
    }
  };

  const handleAIGenerate = async () => {
    const prompt = window.prompt('AIに生成してほしい内容を入力してください（例: 今日の天気について）');
    if (!prompt) return;

    setIsAIGenerating(true);
    try {
      const response = await fetch('/api/ai/generate-post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      setContent(data.content);
    } catch (error) {
      console.error('AI generation failed:', error);
      alert('AI生成に失敗しました。');
    } finally {
      setIsAIGenerating(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 mb-6">
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="今何を考えていますか？"
        className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        rows={4}
      />
      <div className="flex justify-between items-center mt-4">
        <button
          type="button"
          onClick={handleAIGenerate}
          disabled={isAIGenerating}
          className="px-6 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition disabled:opacity-50 flex items-center gap-2"
        >
          {isAIGenerating ? '⏳ 生成中...' : '🤖 AIで生成'}
        </button>
        <button
          type="submit"
          disabled={!content.trim()}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition disabled:opacity-50"
        >
          投稿する
        </button>
      </div>
    </form>
  );
}
