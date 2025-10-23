import { NextRequest, NextResponse } from 'next/server';
import { posts } from '@/lib/data';

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const body = await request.json();
  const { userId } = body;

  const post = posts.find((p) => p.id === id);

  if (!post) {
    return NextResponse.json({ error: 'Post not found' }, { status: 404 });
  }

  const likeIndex = post.likes.indexOf(userId);

  if (likeIndex > -1) {
    // Unlike
    post.likes.splice(likeIndex, 1);
  } else {
    // Like
    post.likes.push(userId);
  }

  return NextResponse.json(post);
}
