import { NextRequest, NextResponse } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { postContent } = body;

    if (!postContent) {
      return NextResponse.json(
        { error: 'Post content is required' },
        { status: 400 }
      );
    }

    // API Keyがない場合はモックレスポンスを返す
    const apiKey = process.env.ANTHROPIC_API_KEY;

    if (!apiKey) {
      // モックレスポンス
      const mockComments = [
        '素晴らしい投稿ですね！とても参考になりました。',
        'なるほど、面白い視点ですね。もっと詳しく聞きたいです！',
        '共感します！私も同じように感じていました。',
        'とても興味深い内容ですね。ありがとうございます！',
        'いいですね！このトピックについてもっと話しましょう。',
      ];

      const randomComment = mockComments[Math.floor(Math.random() * mockComments.length)];

      return NextResponse.json({ content: randomComment });
    }

    // 実際のAI生成
    const anthropic = new Anthropic({
      apiKey: apiKey,
    });

    const message = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 512,
      messages: [
        {
          role: 'user',
          content: `以下の投稿に対する適切なコメントを生成してください。\n\n投稿: ${postContent}\n\n以下の条件を満たしてください：\n- 100文字以内\n- フレンドリーで建設的なトーン\n- 日本語で\n- コメント本文のみを返してください（余計な説明は不要）`,
        },
      ],
    });

    const content = message.content[0].type === 'text' ? message.content[0].text : '';

    return NextResponse.json({ content });
  } catch (error) {
    console.error('AI comment suggestion error:', error);
    return NextResponse.json(
      { error: 'Failed to suggest comment' },
      { status: 500 }
    );
  }
}
