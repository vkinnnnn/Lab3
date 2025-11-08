/**
 * Pros & Cons List Component
 * AI-generated advantages and disadvantages
 * Following KIRO Global Steering Guidelines
 */

'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ThumbsUp, ThumbsDown, Sparkles } from 'lucide-react';
import type { ProsCons } from '@/types';

interface ProsConsListProps {
  prosCons: ProsCons[];
  bestOverall: string;
}

export function ProsConsList({ prosCons, bestOverall }: ProsConsListProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <Sparkles className="mr-2 h-5 w-5 text-teal" />
          AI-Powered Pros & Cons Analysis
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-6 md:grid-cols-3">
          {prosCons.map((pc) => (
            <div
              key={pc.loan_id}
              className={`rounded-lg border-2 p-6 transition-all ${
                pc.bank_name === bestOverall
                  ? 'border-teal bg-teal-50'
                  : 'border-gray-200 bg-white'
              }`}
            >
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-lg font-semibold text-slate">{pc.bank_name}</h3>
                {pc.bank_name === bestOverall && (
                  <Badge variant="success">Recommended</Badge>
                )}
              </div>

              {/* Pros */}
              <div className="mb-4">
                <div className="mb-2 flex items-center text-sm font-medium text-green-700">
                  <ThumbsUp className="mr-2 h-4 w-4" />
                  Pros
                </div>
                <ul className="space-y-1">
                  {pc.pros.map((pro, idx) => (
                    <li key={idx} className="flex items-start text-sm text-slate-light">
                      <span className="mr-2 text-green-600">✓</span>
                      {pro}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Cons */}
              <div className="mb-4">
                <div className="mb-2 flex items-center text-sm font-medium text-red-700">
                  <ThumbsDown className="mr-2 h-4 w-4" />
                  Cons
                </div>
                <ul className="space-y-1">
                  {pc.cons.map((con, idx) => (
                    <li key={idx} className="flex items-start text-sm text-slate-light">
                      <span className="mr-2 text-red-600">✗</span>
                      {con}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Summary */}
              <div className="rounded-lg bg-white p-3">
                <p className="text-sm italic text-slate-light">{pc.summary}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
