import { NextRequest, NextResponse } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { prompt } = body;

    if (!prompt) {
      return NextResponse.json(
        { error: 'Prompt is required' },
        { status: 400 }
      );
    }

    // API Keyがない場合はモックレスポンスを返す
    const apiKey = process.env.ANTHROPIC_API_KEY;

    if (!apiKey) {
      // モックレスポンス
      const mockResponses = [
        `${prompt}について考えてみました。\n\n素晴らしいトピックですね！AIの力を活用することで、私たちはより効率的に情報を処理し、新しいアイデアを生み出すことができます。`,
        `${prompt}に関する投稿です。\n\n技術の進化は目覚ましく、日々新しい発見や学びがあります。みなさんはどう思いますか？`,
        `今日は${prompt}について投稿します。\n\nこのテーマは非常に興味深く、多くの可能性を秘めています。皆さんのご意見もぜひお聞かせください！`,
      ];

      const randomResponse = mockResponses[Math.floor(Math.random() * mockResponses.length)];

      return NextResponse.json({ content: randomResponse });
    }

    // 実際のAI生成
    const anthropic = new Anthropic({
      apiKey: apiKey,
    });

    const message = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1024,
      messages: [
        {
          role: 'user',
          content: `SNSの投稿を生成してください。トピック: ${prompt}\n\n以下の条件を満たしてください：\n- 200文字以内\n- フレンドリーなトーン\n- 日本語で\n- 投稿本文のみを返してください（余計な説明は不要）`,
        },
      ],
    });

    const content = message.content[0].type === 'text' ? message.content[0].text : '';

    return NextResponse.json({ content });
  } catch (error) {
    console.error('AI generation error:', error);
    return NextResponse.json(
      { error: 'Failed to generate post' },
      { status: 500 }
    );
  }
}
