'use client';

import Link from 'next/link';
import { Heart, BarChart3, MessageSquare, Shield } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Rose Glass Dating
          </h1>
          <p className="text-2xl text-gray-600 mb-4">
            Translation, Not Judgment
          </p>
          <p className="text-lg text-gray-500 mb-8 max-w-2xl mx-auto">
            Analyze dating profiles through the Rose Glass framework - a mathematical lens
            that translates patterns into insights without measuring or judging.
          </p>
          <Link
            href="/analyze"
            className="inline-flex items-center gap-2 bg-rose-500 hover:bg-rose-600 text-white px-8 py-3 rounded-lg font-medium transition-colors"
          >
            <Heart className="h-5 w-5" />
            Start Analysis
          </Link>
        </div>

        {/* Features */}
        <div className="max-w-5xl mx-auto mt-20 grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <BarChart3 className="h-10 w-10 text-rose-500 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Four-Dimensional Translation</h3>
            <p className="text-gray-600">
              Ψ (consistency), ρ (wisdom), q (activation), f (belonging) - understand
              patterns through multiple lenses.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <MessageSquare className="h-10 w-10 text-rose-500 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Calibrated Openers</h3>
            <p className="text-gray-600">
              Get suggested messages perfectly calibrated to their communication style
              and energy level.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg border shadow-sm">
            <Shield className="h-10 w-10 text-rose-500 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Conversation Analysis</h3>
            <p className="text-gray-600">
              Upload conversation screenshots to detect investment levels and red/green flags.
            </p>
          </div>
        </div>

        {/* How It Works */}
        <div className="max-w-3xl mx-auto mt-20">
          <h2 className="text-3xl font-bold text-center mb-8">How It Works</h2>
          <div className="space-y-6">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-rose-500 text-white rounded-full flex items-center justify-center font-semibold">
                1
              </div>
              <div>
                <h4 className="font-semibold mb-1">Upload Screenshots</h4>
                <p className="text-gray-600">
                  Upload 1-10 screenshots of the dating profile you want analyzed.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-rose-500 text-white rounded-full flex items-center justify-center font-semibold">
                2
              </div>
              <div>
                <h4 className="font-semibold mb-1">Rose Glass Translation</h4>
                <p className="text-gray-600">
                  Claude analyzes the profile through the Rose Glass framework,
                  translating patterns into insights.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-rose-500 text-white rounded-full flex items-center justify-center font-semibold">
                3
              </div>
              <div>
                <h4 className="font-semibold mb-1">Get Insights</h4>
                <p className="text-gray-600">
                  Receive dimensional analysis, suggested opener, and actionable insights.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Pricing */}
        <div className="max-w-2xl mx-auto mt-20 text-center">
          <h2 className="text-3xl font-bold mb-4">Simple Pricing</h2>
          <p className="text-gray-600 mb-8">
            Pay per analysis. No subscriptions. Only pay for what you use.
          </p>
          <div className="bg-white p-8 rounded-lg border shadow-sm">
            <div className="text-5xl font-bold text-rose-500 mb-2">$0.02 - $0.10</div>
            <div className="text-gray-600 mb-6">per analysis</div>
            <p className="text-sm text-gray-500">
              Cost varies based on number of images and model used.
              Standard analysis ~$0.02-0.04, Premium ~$0.10-0.20
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="max-w-2xl mx-auto mt-20 text-center">
          <Link
            href="/analyze"
            className="inline-flex items-center gap-2 bg-rose-500 hover:bg-rose-600 text-white px-8 py-3 rounded-lg font-medium transition-colors text-lg"
          >
            Try It Now
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t mt-20 py-8">
        <div className="container mx-auto px-4 text-center text-gray-500 text-sm">
          <p>🌹 Rose Glass Dating - Translation, Not Judgment</p>
          <p className="mt-2">Powered by Claude and the Rose Glass Framework</p>
        </div>
      </footer>
    </div>
  );
}
