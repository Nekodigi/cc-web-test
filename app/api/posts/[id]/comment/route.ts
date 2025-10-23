import { NextRequest, NextResponse } from 'next/server';
import { posts } from '@/lib/data';
import { Comment } from '@/types';

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const body = await request.json();
  const { userId, content } = body;

  const post = posts.find((p) => p.id === id);

  if (!post) {
    return NextResponse.json({ error: 'Post not found' }, { status: 404 });
  }

  const newComment: Comment = {
    id: Date.now().toString(),
    userId,
    content,
    createdAt: new Date(),
  };

  post.comments.push(newComment);

  return NextResponse.json(post);
}
