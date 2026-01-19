/**
 * API Client for Rose Glass Dating Backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface AnalysisRequest {
  profileImages: File[];
  conversationImages?: File[];
  userContext?: string;
  usePremium?: boolean;
}

export interface AnalysisResponse {
  success: boolean;
  analysis: string;
  usage: {
    input_tokens: number;
    output_tokens: number;
    cost_usd: number;
    charge_usd: number;
    model_used: string;
  };
  remaining_credits: number;
  analysis_id?: string;
}

export async function analyzeProfile(
  request: AnalysisRequest,
  token: string
): Promise<AnalysisResponse> {
  const formData = new FormData();

  // Add profile images
  request.profileImages.forEach(image => {
    formData.append('profile_images', image);
  });

  // Add conversation images if provided
  if (request.conversationImages && request.conversationImages.length > 0) {
    request.conversationImages.forEach(image => {
      formData.append('conversation_images', image);
    });
  }

  // Add context if provided
  if (request.userContext) {
    formData.append('user_context', request.userContext);
  }

  // Add premium flag
  formData.append('use_premium', String(request.usePremium || false));

  const response = await fetch(`${API_URL}/api/analyze`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Analysis failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export async function getCredits(token: string): Promise<{ credits: number }> {
  const response = await fetch(`${API_URL}/api/analyze/credits`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error('Failed to get credits');
  }

  const data = await response.json();
  return { credits: data.credits };
}
