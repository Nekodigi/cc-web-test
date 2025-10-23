import { NextRequest, NextResponse } from 'next/server';
import { posts } from '@/lib/data';

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const index = posts.findIndex((p) => p.id === id);

  if (index === -1) {
    return NextResponse.json({ error: 'Post not found' }, { status: 404 });
  }

  posts.splice(index, 1);
  return NextResponse.json({ success: true });
}
