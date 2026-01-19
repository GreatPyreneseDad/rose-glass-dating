'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Loader2 } from 'lucide-react';
import { UploadZone } from '@/components/upload-zone';
import { AnalysisDisplay } from '@/components/analysis-display';
import { analyzeProfile } from '@/lib/api';

export default function AnalyzePage() {
  const [profileImages, setProfileImages] = useState<File[]>([]);
  const [conversationImages, setConversationImages] = useState<File[]>([]);
  const [userContext, setUserContext] = useState('');
  const [usePremium, setUsePremium] = useState(false);

  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (profileImages.length === 0) {
      setError('Please upload at least one profile screenshot');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // For MVP, use dev token
      const token = 'dev_test_user';

      const result = await analyzeProfile(
        {
          profileImages,
          conversationImages: conversationImages.length > 0 ? conversationImages : undefined,
          userContext: userContext || undefined,
          usePremium
        },
        token
      );

      setAnalysis(result);
    } catch (err: any) {
      console.error('Analysis error:', err);
      setError(err.message || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setAnalysis(null);
    setProfileImages([]);
    setConversationImages([]);
    setUserContext('');
    setError(null);
  };

  return (
    <div className="min-h-screen py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-rose-500 hover:text-rose-600 mb-4"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Home
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Profile Analysis</h1>
          <p className="text-gray-600 mt-2">
            Upload dating profile screenshots for Rose Glass translation
          </p>
        </div>

        {/* Analysis Result */}
        {analysis ? (
          <div className="space-y-6">
            <AnalysisDisplay
              analysis={analysis.analysis}
              usage={analysis.usage}
              remainingCredits={analysis.remaining_credits}
            />
            <button
              onClick={resetAnalysis}
              className="w-full py-3 bg-rose-500 hover:bg-rose-600 text-white rounded-lg font-medium transition-colors"
            >
              Analyze Another Profile
            </button>
          </div>
        ) : (
          /* Upload Interface */
          <div className="space-y-6">
            {/* Profile Images */}
            <div className="bg-white rounded-lg p-6 border shadow-sm">
              <UploadZone
                onImagesSelected={setProfileImages}
                maxImages={10}
                label="Profile Screenshots (Required)"
              />
            </div>

            {/* Conversation Images */}
            <div className="bg-white rounded-lg p-6 border shadow-sm">
              <UploadZone
                onImagesSelected={setConversationImages}
                maxImages={10}
                label="Conversation Screenshots (Optional)"
              />
              <p className="text-sm text-gray-500 mt-2">
                Upload conversation screenshots to analyze investment level and get next-move recommendations
              </p>
            </div>

            {/* User Context */}
            <div className="bg-white rounded-lg p-6 border shadow-sm">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your Context (Optional)
              </label>
              <textarea
                value={userContext}
                onChange={(e) => setUserContext(e.target.value)}
                className="w-full p-3 border rounded-lg resize-none focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                rows={3}
                placeholder="e.g., Looking for long-term relationship, prefer intellectual connection, value humor..."
              />
              <p className="text-sm text-gray-500 mt-2">
                Share context about yourself to get more personalized compatibility insights
              </p>
            </div>

            {/* Premium Toggle */}
            <div className="bg-white rounded-lg p-6 border shadow-sm">
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={usePremium}
                  onChange={(e) => setUsePremium(e.target.checked)}
                  className="w-4 h-4 text-rose-500 rounded focus:ring-rose-500"
                />
                <div>
                  <div className="font-medium">Use Premium Model (Claude Opus)</div>
                  <div className="text-sm text-gray-500">
                    More detailed analysis, better for complex profiles (~$0.10-0.20 vs ~$0.02-0.04)
                  </div>
                </div>
              </label>
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}

            {/* Analyze Button */}
            <button
              onClick={handleAnalyze}
              disabled={loading || profileImages.length === 0}
              className="w-full py-4 bg-rose-500 hover:bg-rose-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                `Analyze Profile (${profileImages.length} ${profileImages.length === 1 ? 'image' : 'images'})`
              )}
            </button>

            {/* Info */}
            <div className="text-center text-sm text-gray-500">
              <p>Analysis typically takes 10-30 seconds</p>
              <p className="mt-1">
                Cost: {usePremium ? '~$0.10-0.20' : '~$0.02-0.04'} per analysis
              </p>
            </div>
          </div>
        )}

        {/* About Rose Glass */}
        <div className="mt-12 bg-rose-50 rounded-lg p-6 border border-rose-200">
          <h3 className="font-semibold text-rose-900 mb-2">About Rose Glass Translation</h3>
          <p className="text-sm text-rose-800 leading-relaxed">
            The Rose Glass framework translates dating profiles through four dimensions:
            <strong> Ψ</strong> (internal consistency),
            <strong> ρ</strong> (wisdom depth),
            <strong> q</strong> (emotional activation), and
            <strong> f</strong> (social belonging).
            This is translation, not judgment - revealing patterns to help you understand
            communication styles and craft authentic connections.
          </p>
        </div>
      </div>
    </div>
  );
}
