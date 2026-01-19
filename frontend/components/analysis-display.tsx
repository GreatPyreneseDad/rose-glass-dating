'use client';

import { useState } from 'react';
import { Copy, Check, MessageSquare, BarChart3 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface AnalysisDisplayProps {
  analysis: string;
  usage: {
    input_tokens: number;
    output_tokens: number;
    cost_usd: number;
    charge_usd: number;
  };
  remainingCredits: number;
}

export function AnalysisDisplay({ analysis, usage, remainingCredits }: AnalysisDisplayProps) {
  const [copied, setCopied] = useState(false);

  const openerMatch = analysis.match(/\*\*Suggested Opener[:\*]*\*?\s*\n?>?\s*(.+?)(?:\n\n|\n\*\*|$)/s);
  const suggestedOpener = openerMatch?.[1]?.trim();

  const copyOpener = () => {
    if (suggestedOpener) {
      navigator.clipboard.writeText(suggestedOpener);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-rose-50 to-pink-50 rounded-lg p-4 border border-rose-200">
        <div className="flex justify-between items-center text-sm">
          <div className="flex items-center gap-4">
            <span className="text-gray-600">
              Cost: <span className="font-medium">${usage.charge_usd.toFixed(4)}</span>
            </span>
            <span className="text-gray-400">|</span>
            <span className="text-gray-600">
              Tokens: {usage.input_tokens + usage.output_tokens}
            </span>
          </div>
          <span className="text-gray-600">
            Balance: <span className="font-medium text-green-600">${remainingCredits.toFixed(2)}</span>
          </span>
        </div>
      </div>

      <div className="bg-white rounded-lg p-6 border shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <BarChart3 className="h-5 w-5 text-rose-500" />
          <h2 className="text-lg font-semibold">Rose Glass Analysis</h2>
        </div>
        <div className="prose prose-rose max-w-none">
          <ReactMarkdown
            components={{
              table: ({ children }) => (
                <div className="overflow-x-auto my-4">
                  <table className="min-w-full border-collapse border border-gray-200">
                    {children}
                  </table>
                </div>
              ),
              th: ({ children }) => (
                <th className="border border-gray-200 bg-rose-50 px-4 py-2 text-left font-medium">
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td className="border border-gray-200 px-4 py-2">{children}</td>
              ),
            }}
          >
            {analysis}
          </ReactMarkdown>
        </div>
      </div>

      {suggestedOpener && (
        <div className="border-2 border-rose-200 bg-rose-50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <MessageSquare className="h-4 w-4 text-rose-500" />
            <h3 className="text-sm font-semibold">Suggested Opener</h3>
          </div>
          <div className="flex items-start gap-4">
            <p className="flex-1 text-gray-700 italic">"{suggestedOpener}"</p>
            <button
              onClick={copyOpener}
              className="shrink-0 p-2 rounded-md hover:bg-rose-100 transition-colors"
            >
              {copied ? (
                <Check className="h-4 w-4 text-green-500" />
              ) : (
                <Copy className="h-4 w-4 text-rose-500" />
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
