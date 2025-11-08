/**
 * Comparison Charts Component
 * Visual charts for loan comparison
 * Following KIRO Global Steering Guidelines
 */

'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart3, PieChart } from 'lucide-react';
import type { LoanMetrics } from '@/types';

interface ComparisonChartsProps {
  metrics: LoanMetrics[];
}

export function ComparisonCharts({ metrics }: ComparisonChartsProps) {
  // Find max values for scaling
  const maxCost = Math.max(...metrics.map((m) => m.total_cost));
  const maxMonthly = Math.max(...metrics.map((m) => m.monthly_payment));

  return (
    <div className="grid gap-6 md:grid-cols-2">
      {/* Total Cost Comparison */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-lg">
            <BarChart3 className="mr-2 h-5 w-5 text-teal" />
            Total Cost Comparison
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {metrics.map((metric) => {
              const percentage = (metric.total_cost / maxCost) * 100;
              const isLowest = metric.total_cost === Math.min(...metrics.map((m) => m.total_cost));

              return (
                <div key={metric.loan_id}>
                  <div className="mb-2 flex items-center justify-between text-sm">
                    <span className="font-medium text-slate">{metric.bank_name}</span>
                    <span className={isLowest ? 'font-semibold text-teal' : 'text-slate-light'}>
                      ${metric.total_cost.toLocaleString()}
                    </span>
                  </div>
                  <div className="h-8 overflow-hidden rounded-full bg-base-dark">
                    <div
                      className={`h-full transition-all duration-1000 ${
                        isLowest ? 'bg-teal' : 'bg-teal-light'
                      }`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Monthly Payment Comparison */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-lg">
            <PieChart className="mr-2 h-5 w-5 text-accent-orange" />
            Monthly Payment Comparison
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {metrics.map((metric) => {
              const percentage = (metric.monthly_payment / maxMonthly) * 100;
              const isLowest =
                metric.monthly_payment === Math.min(...metrics.map((m) => m.monthly_payment));

              return (
                <div key={metric.loan_id}>
                  <div className="mb-2 flex items-center justify-between text-sm">
                    <span className="font-medium text-slate">{metric.bank_name}</span>
                    <span className={isLowest ? 'font-semibold text-accent-orange' : 'text-slate-light'}>
                      ${metric.monthly_payment.toLocaleString()}
                    </span>
                  </div>
                  <div className="h-8 overflow-hidden rounded-full bg-base-dark">
                    <div
                      className={`h-full transition-all duration-1000 ${
                        isLowest ? 'gradient-accent' : 'bg-orange-300'
                      }`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
