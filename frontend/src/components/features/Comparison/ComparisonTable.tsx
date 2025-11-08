/**
 * Comparison Table Component
 * Side-by-side loan comparison
 * Following KIRO Global Steering Guidelines
 */

'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Check, TrendingUp, TrendingDown } from 'lucide-react';
import { formatCurrency, formatPercent } from '@/lib/utils';
import type { LoanMetrics } from '@/types';

interface ComparisonTableProps {
  metrics: LoanMetrics[];
  bestOverall: string;
}

export function ComparisonTable({ metrics, bestOverall }: ComparisonTableProps) {
  const findBest = (key: keyof LoanMetrics, lowest = true) => {
    const values = metrics.map((m) => m[key] as number);
    const bestValue = lowest ? Math.min(...values) : Math.max(...values);
    return metrics.find((m) => m[key] === bestValue)?.bank_name;
  };

  const rows = [
    { label: 'Principal Amount', key: 'principal' as keyof LoanMetrics, format: formatCurrency },
    { label: 'Interest Rate', key: 'interest_rate' as keyof LoanMetrics, format: formatPercent },
    { label: 'Tenure', key: 'tenure_months' as keyof LoanMetrics, format: (v: number) => `${v} months` },
    { label: 'Monthly Payment', key: 'monthly_payment' as keyof LoanMetrics, format: formatCurrency, highlight: true },
    { label: 'Total Cost', key: 'total_cost' as keyof LoanMetrics, format: formatCurrency, highlight: true },
    { label: 'Total Interest', key: 'total_interest' as keyof LoanMetrics, format: formatCurrency },
    { label: 'Processing Fee', key: 'processing_fee' as keyof LoanMetrics, format: formatCurrency },
    { label: 'Effective Rate', key: 'effective_rate' as keyof LoanMetrics, format: formatPercent },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Detailed Comparison</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="p-4 text-left text-sm font-medium text-slate-lighter">Metric</th>
                {metrics.map((metric) => (
                  <th key={metric.loan_id} className="p-4 text-center">
                    <div className="font-semibold text-slate">{metric.bank_name}</div>
                    {metric.bank_name === bestOverall && (
                      <Badge variant="success" className="mt-1">
                        <Check className="mr-1 h-3 w-3" />
                        Best Overall
                      </Badge>
                    )}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, idx) => {
                const bestBank = findBest(row.key, row.key !== 'interest_rate');
                
                return (
                  <tr key={row.label} className={idx % 2 === 0 ? 'bg-base' : ''}>
                    <td className="p-4 text-sm font-medium text-slate">{row.label}</td>
                    {metrics.map((metric) => {
                      const value = metric[row.key] as number;
                      const isBest = metric.bank_name === bestBank;
                      
                      return (
                        <td
                          key={metric.loan_id}
                          className={`p-4 text-center ${
                            row.highlight
                              ? isBest
                                ? 'bg-teal-50 font-semibold text-teal'
                                : 'font-medium text-slate'
                              : 'text-slate-light'
                          }`}
                        >
                          <div className="flex items-center justify-center">
                            {row.format(value)}
                            {isBest && row.highlight && (
                              <TrendingDown className="ml-2 h-4 w-4 text-teal" />
                            )}
                          </div>
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}
