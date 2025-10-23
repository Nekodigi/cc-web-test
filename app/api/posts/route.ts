import { NextRequest, NextResponse } from 'next/server';
import { posts } from '@/lib/data';
import { Post } from '@/types';

export async function GET() {
  // 日付でソート（新しい順）
  const sortedPosts = [...posts].sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );
  return NextResponse.json(sortedPosts);
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { content, userId } = body;

    if (!content || !userId) {
      return NextResponse.json(
        { error: 'Content and userId are required' },
        { status: 400 }
      );
    }

    const newPost: Post = {
      id: Date.now().toString(),
      userId,
      content,
      createdAt: new Date(),
      likes: [],
      comments: [],
    };

    posts.unshift(newPost);

    return NextResponse.json(newPost, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create post' },
      { status: 500 }
    );
  }
}
