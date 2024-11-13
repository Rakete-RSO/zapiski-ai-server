import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
    return new NextResponse(JSON.stringify({
        request: request.url
    }), {
        status: 200
    });
}