/**
 * Compare Page - Multi-Loan Comparison Dashboard
 * Beautiful side-by-side comparison with charts
 * Following KIRO Global Steering Guidelines
 */

'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ComparisonTable } from '@/components/features/Comparison/ComparisonTable';
import { ComparisonCharts } from '@/components/features/Comparison/ComparisonCharts';
import { ProsConsList } from '@/components/features/Comparison/ProsConsList';
import { BarChart3, TrendingDown, Trophy, Upload, ArrowRight } from 'lucide-react';
import type { ComparisonResult } from '@/types';

export default function ComparePage() {
  const [comparison, setComparison] = useState<ComparisonResult | null>(null);
  const [loading, setLoading] = useState(false);

  // Mock data for demo (replace with actual API call)
  const loadSampleComparison = () => {
    setLoading(true);
    setTimeout(() => {
      const mockComparison: ComparisonResult = {
        loans: [
          { document_id: 'loan1', document_name: 'Bank A Loan', bank_name: 'Bank A' },
          { document_id: 'loan2', document_name: 'Bank B Loan', bank_name: 'Bank B' },
          { document_id: 'loan3', document_name: 'Bank C Loan', bank_name: 'Bank C' },
        ],
        metrics: [
          {
            loan_id: 'loan1',
            bank_name: 'Bank A',
            principal: 10000,
            interest_rate: 5.5,
            tenure_months: 60,
            monthly_payment: 191.01,
            total_cost: 11460.6,
            total_interest: 1460.6,
            effective_rate: 5.7,
            upfront_costs: 250,
            processing_fee: 200,
            other_fees: 50,
          },
          {
            loan_id: 'loan2',
            bank_name: 'Bank B',
            principal: 10000,
            interest_rate: 6.5,
            tenure_months: 48,
            monthly_payment: 237.9,
            total_cost: 11419.2,
            total_interest: 1419.2,
            effective_rate: 6.8,
            upfront_costs: 100,
            processing_fee: 100,
            other_fees: 0,
          },
          {
            loan_id: 'loan3',
            bank_name: 'Bank C',
            principal: 10000,
            interest_rate: 5.0,
            tenure_months: 72,
            monthly_payment: 161.33,
            total_cost: 11615.76,
            total_interest: 1615.76,
            effective_rate: 5.4,
            upfront_costs: 400,
            processing_fee: 300,
            other_fees: 100,
          },
        ],
        flexibility_scores: [
          {
            loan_id: 'loan1',
            bank_name: 'Bank A',
            score: 8,
            features: ['No prepayment penalty', 'Deferment available'],
            details: { prepayment_allowed: true, deferment: true },
          },
          {
            loan_id: 'loan2',
            bank_name: 'Bank B',
            score: 4,
            features: ['Partial payment accepted'],
            details: { prepayment_allowed: false, deferment: false },
          },
          {
            loan_id: 'loan3',
            bank_name: 'Bank C',
            score: 6,
            features: ['Flexible payment dates', 'Top-up available'],
            details: { prepayment_allowed: true, deferment: false },
          },
        ],
        pros_cons: [
          {
            loan_id: 'loan1',
            bank_name: 'Bank A',
            pros: ['Lowest monthly payment', 'High flexibility', 'Low processing fee'],
            cons: ['Longer tenure', 'Slightly higher total cost'],
            summary: 'Best for affordability with good flexibility',
          },
          {
            loan_id: 'loan2',
            bank_name: 'Bank B',
            pros: ['Shortest tenure', 'Lowest processing fee', 'Finish debt quickly'],
            cons: ['Highest monthly payment', 'Limited flexibility', 'Higher interest rate'],
            summary: 'Best for quick repayment if you can afford higher EMI',
          },
          {
            loan_id: 'loan3',
            bank_name: 'Bank C',
            pros: ['Lowest interest rate', 'Moderate flexibility', 'Good for long-term'],
            cons: ['Highest total cost', 'High processing fee', 'Longest tenure'],
            summary: 'Best for lowest monthly burden but pays most interest',
          },
        ],
        best_overall: 'Bank B',
        best_by_category: {
          lowest_total_cost: 'Bank B',
          lowest_monthly_payment: 'Bank C',
          most_flexible: 'Bank A',
          lowest_interest_rate: 'Bank C',
        },
        recommendation: `**Recommendation: Bank B**\n\nBased on comprehensive analysis, Bank B offers the best overall value. While it has a higher monthly payment ($237.90), you'll finish paying 12 months earlier and save $196 in total interest compared to Bank A.\n\nKey advantages:\n• Lowest total cost ($11,419)\n• Shortest repayment period (48 months)\n• Minimal upfront fees ($100)\n\n**Consider Bank A if:** You need lower monthly payments ($191) and value flexibility.\n\n**Consider Bank C if:** You want the absolute lowest interest rate (5%) but can accept longer tenure.`,
        comparison_date: new Date().toISOString(),
      };
      
      setComparison(mockComparison);
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="container py-12">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center justify-between">
          <div>
            <div className="mb-2 inline-flex items-center rounded-full bg-teal-100 px-3 py-1 text-sm font-medium text-teal">
              <BarChart3 className="mr-2 h-4 w-4" />
              AI-Powered Analysis
            </div>
            <h1 className="mb-2 text-4xl font-bold text-slate">Compare Loan Offers</h1>
            <p className="text-lg text-slate-light">
              Side-by-side comparison with AI-generated insights
            </p>
          </div>
          <Button asChild variant="outline">
            <a href="/upload">
              <Upload className="mr-2 h-4 w-4" />
              Upload More Documents
            </a>
          </Button>
        </div>
      </motion.div>

      {!comparison ? (
        /* Empty State */
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <Card className="border-2 border-dashed">
            <CardContent className="p-12 text-center">
              <div className="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-teal-50">
                <BarChart3 className="h-10 w-10 text-teal" />
              </div>
              <h3 className="mb-2 text-xl font-semibold text-slate">No Comparison Yet</h3>
              <p className="mb-6 text-slate-lighter">
                Upload multiple loan documents to compare them side-by-side
              </p>
              <div className="flex items-center justify-center gap-4">
                <Button onClick={loadSampleComparison} loading={loading}>
                  Load Sample Comparison
                </Button>
                <Button asChild variant="outline">
                  <a href="/upload">Upload Documents</a>
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ) : (
        /* Comparison Results */
        <div className="space-y-8">
          {/* Best Option Banner */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Card className="border-teal bg-teal-50">
              <CardContent className="p-6">
                <div className="flex items-start">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-teal text-white">
                    <Trophy className="h-6 w-6" />
                  </div>
                  <div className="ml-4 flex-1">
                    <div className="flex items-center">
                      <h3 className="text-lg font-semibold text-slate">
                        Best Overall: {comparison.best_overall}
                      </h3>
                      <Badge variant="success" className="ml-2">
                        Recommended
                      </Badge>
                    </div>
                    <p className="mt-1 text-sm text-slate-light">
                      Based on total cost, flexibility, and repayment terms
                    </p>
                  </div>
                  <Button variant="accent" size="sm">
                    View Details
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Quick Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid gap-4 sm:grid-cols-3"
          >
            <Card>
              <CardContent className="p-6">
                <div className="text-sm text-slate-lighter">Lowest Total Cost</div>
                <div className="mt-1 text-2xl font-bold text-teal">
                  {comparison.best_by_category.lowest_total_cost}
                </div>
                <div className="mt-1 text-sm text-slate-light">
                  Save ${(comparison.metrics[0].total_cost - Math.min(...comparison.metrics.map(m => m.total_cost))).toFixed(0)} vs highest
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6">
                <div className="text-sm text-slate-lighter">Most Flexible</div>
                <div className="mt-1 text-2xl font-bold text-teal">
                  {comparison.best_by_category.most_flexible}
                </div>
                <div className="mt-1 text-sm text-slate-light">
                  Score: {Math.max(...comparison.flexibility_scores.map(f => f.score))}/10
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6">
                <div className="text-sm text-slate-lighter">Lowest Rate</div>
                <div className="mt-1 text-2xl font-bold text-teal">
                  {comparison.best_by_category.lowest_interest_rate}
                </div>
                <div className="mt-1 text-sm text-slate-light">
                  {Math.min(...comparison.metrics.map(m => m.interest_rate))}% APR
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Comparison Table */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <ComparisonTable metrics={comparison.metrics} bestOverall={comparison.best_overall} />
          </motion.div>

          {/* Charts */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <ComparisonCharts metrics={comparison.metrics} />
          </motion.div>

          {/* Pros & Cons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <ProsConsList prosCons={comparison.pros_cons} bestOverall={comparison.best_overall} />
          </motion.div>

          {/* AI Recommendation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingDown className="mr-2 h-5 w-5 text-teal" />
                  AI Recommendation
                </CardTitle>
                <CardDescription>Personalized analysis based on your needs</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="prose prose-slate max-w-none">
                  {comparison.recommendation.split('\n').map((line, idx) => {
                    if (line.startsWith('**') && line.endsWith('**')) {
                      return (
                        <h4 key={idx} className="font-semibold text-slate">
                          {line.replace(/\*\*/g, '')}
                        </h4>
                      );
                    }
                    if (line.startsWith('•')) {
                      return (
                        <li key={idx} className="ml-4 text-slate-light">
                          {line.substring(2)}
                        </li>
                      );
                    }
                    return line ? (
                      <p key={idx} className="text-slate-light">
                        {line}
                      </p>
                    ) : null;
                  })}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="flex gap-4"
          >
            <Button asChild className="flex-1">
              <a href="/chat">
                Ask Questions About Comparison
                <ArrowRight className="ml-2 h-4 w-4" />
              </a>
            </Button>
            <Button asChild variant="outline" className="flex-1">
              <a href="/learn">Learn About Loan Terms</a>
            </Button>
          </motion.div>
        </div>
      )}
    </div>
  );
}
