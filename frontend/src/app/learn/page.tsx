/**
 * Learn Page - Financial Education Center
 * Interactive glossary, scenarios, and best practices
 * Following KIRO Global Steering Guidelines
 */

'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  BookOpen,
  Calculator,
  Lightbulb,
  Search,
  TrendingDown,
  DollarSign,
  Clock,
  CheckCircle2,
} from 'lucide-react';

// Financial Glossary Data
const glossaryTerms = [
  {
    term: 'APR (Annual Percentage Rate)',
    category: 'Interest & Rates',
    simple: 'The yearly cost of borrowing money, including interest and fees',
    example: 'If you borrow $10,000 at 10% APR, you pay $1,000 in interest per year',
    whyMatters: 'Lower APR = less money paid over the loan life',
  },
  {
    term: 'Principal Amount',
    category: 'Loan Basics',
    simple: 'The original amount of money you borrow',
    example: 'If you take a $10,000 loan, the principal is $10,000',
    whyMatters: 'Interest is calculated on the principal',
  },
  {
    term: 'EMI (Equated Monthly Installment)',
    category: 'Payments',
    simple: 'The fixed amount you pay every month toward your loan',
    example: 'For a $10,000 loan at 10% for 12 months, EMI is ~$879/month',
    whyMatters: 'Knowing your EMI helps budget monthly expenses',
  },
  {
    term: 'Processing Fee',
    category: 'Fees & Charges',
    simple: 'Upfront charge by the lender to process your loan',
    example: 'On a $10,000 loan with 2% processing fee, you pay $200 upfront',
    whyMatters: 'Reduces the actual amount you receive',
  },
  {
    term: 'Prepayment',
    category: 'Repayment',
    simple: 'Paying off your loan early, before the scheduled end date',
    example: 'Paying $100 extra per month can save hundreds in interest',
    whyMatters: 'Can significantly reduce total interest paid',
  },
];

// Best Practices Data
const bestPractices = [
  {
    title: 'Always Pay On Time',
    icon: CheckCircle2,
    importance: 'high',
    description: 'Timely payments build credit score, avoid late fees, and prevent default',
    tips: [
      'Set up automatic payments',
      'Mark payment dates on calendar',
      'Pay a few days before due date',
    ],
  },
  {
    title: 'Compare Multiple Offers',
    icon: Search,
    importance: 'high',
    description: 'Never accept the first offer. Compare at least 3 lenders',
    tips: [
      'Get quotes from 3+ lenders',
      'Compare APR, not just interest rate',
      'Consider total cost and flexibility',
    ],
  },
  {
    title: 'Pay Extra When Possible',
    icon: TrendingDown,
    importance: 'medium',
    description: 'Even small extra payments significantly reduce total interest',
    tips: [
      'Round up payments',
      'Apply bonuses to principal',
      'Make one extra payment per year',
    ],
  },
  {
    title: 'Build an Emergency Fund',
    icon: DollarSign,
    importance: 'high',
    description: 'Save 3-6 months of expenses to avoid missed payments',
    tips: [
      'Start with $1,000 goal',
      'Gradually build to 3 months expenses',
      'Keep in separate savings account',
    ],
  },
];

export default function LearnPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const filteredTerms = glossaryTerms.filter((term) => {
    const matchesSearch =
      term.term.toLowerCase().includes(searchTerm.toLowerCase()) ||
      term.simple.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || term.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = ['all', ...new Set(glossaryTerms.map((t) => t.category))];

  return (
    <div className="container max-w-6xl py-12">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8 text-center"
      >
        <div className="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-full gradient-teal">
          <BookOpen className="h-8 w-8 text-white" />
        </div>
        <h1 className="mb-4 text-4xl font-bold text-slate">Financial Education Center</h1>
        <p className="text-lg text-slate-light">
          Learn financial concepts, explore scenarios, and make informed decisions
        </p>
      </motion.div>

      {/* Tabs */}
      <Tabs defaultValue="glossary" className="space-y-8">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="glossary">
            <BookOpen className="mr-2 h-4 w-4" />
            Glossary
          </TabsTrigger>
          <TabsTrigger value="scenarios">
            <Calculator className="mr-2 h-4 w-4" />
            Scenarios
          </TabsTrigger>
          <TabsTrigger value="practices">
            <Lightbulb className="mr-2 h-4 w-4" />
            Best Practices
          </TabsTrigger>
        </TabsList>

        {/* Glossary Tab */}
        <TabsContent value="glossary" className="space-y-6">
          {/* Search */}
          <Card>
            <CardContent className="p-6">
              <div className="flex gap-4">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-slate-lighter" />
                  <Input
                    placeholder="Search financial terms..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <div className="flex gap-2">
                  {categories.map((cat) => (
                    <Button
                      key={cat}
                      variant={selectedCategory === cat ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => setSelectedCategory(cat)}
                    >
                      {cat === 'all' ? 'All' : cat}
                    </Button>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Terms */}
          <div className="grid gap-4 md:grid-cols-2">
            {filteredTerms.map((term, idx) => (
              <motion.div
                key={term.term}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.05 }}
              >
                <Card className="h-full hover:card-shadow-hover transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-lg">{term.term}</CardTitle>
                        <Badge variant="secondary" className="mt-1">
                          {term.category}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div>
                      <div className="text-sm font-medium text-slate-lighter">Simple Explanation</div>
                      <div className="text-sm text-slate-light">{term.simple}</div>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-slate-lighter">Example</div>
                      <div className="text-sm italic text-slate-light">{term.example}</div>
                    </div>
                    <div className="rounded-lg bg-teal-50 p-3">
                      <div className="text-xs font-medium text-teal">Why It Matters</div>
                      <div className="text-sm text-slate-light">{term.whyMatters}</div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>

        {/* Scenarios Tab */}
        <TabsContent value="scenarios" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Calculator className="mr-2 h-5 w-5 text-teal" />
                Interactive Scenario Calculator
              </CardTitle>
              <CardDescription>
                See how different choices affect your loan costs
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Scenario 1 */}
              <div className="rounded-lg border-2 border-teal-100 bg-teal-50 p-6">
                <div className="mb-4 flex items-center">
                  <TrendingDown className="mr-2 h-6 w-6 text-teal" />
                  <h3 className="text-lg font-semibold text-slate">Extra Payment Impact</h3>
                </div>
                <div className="space-y-3">
                  <div className="grid gap-4 sm:grid-cols-3">
                    <div>
                      <label className="text-sm text-slate-lighter">Principal</label>
                      <Input defaultValue="10000" type="number" />
                    </div>
                    <div>
                      <label className="text-sm text-slate-lighter">Interest Rate (%)</label>
                      <Input defaultValue="5.5" type="number" step="0.1" />
                    </div>
                    <div>
                      <label className="text-sm text-slate-lighter">Tenure (months)</label>
                      <Input defaultValue="60" type="number" />
                    </div>
                  </div>
                  <div>
                    <label className="text-sm text-slate-lighter">Extra Payment/Month</label>
                    <Input defaultValue="100" type="number" placeholder="$100" />
                  </div>
                  <Button className="w-full">Calculate Savings</Button>
                  
                  {/* Result Preview */}
                  <div className="mt-4 grid gap-3 sm:grid-cols-3">
                    <div className="rounded-lg bg-white p-3">
                      <div className="text-xs text-slate-lighter">You Save</div>
                      <div className="text-xl font-bold text-teal">$612</div>
                    </div>
                    <div className="rounded-lg bg-white p-3">
                      <div className="text-xs text-slate-lighter">Finish Early</div>
                      <div className="text-xl font-bold text-teal">22 months</div>
                    </div>
                    <div className="rounded-lg bg-white p-3">
                      <div className="text-xs text-slate-lighter">New Term</div>
                      <div className="text-xl font-bold text-teal">38 months</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Scenario 2 */}
              <div className="rounded-lg border-2 border-orange-100 bg-orange-50 p-6">
                <div className="mb-4 flex items-center">
                  <Clock className="mr-2 h-6 w-6 text-accent-orange" />
                  <h3 className="text-lg font-semibold text-slate">Tenure Comparison</h3>
                </div>
                <div className="space-y-3">
                  <p className="text-sm text-slate-light">
                    Compare how different loan terms affect your monthly payment and total cost
                  </p>
                  <div className="grid gap-3 sm:grid-cols-3">
                    <div className="rounded-lg bg-white p-4">
                      <div className="text-sm font-medium text-slate">36 Months</div>
                      <div className="mt-2 text-xs text-slate-lighter">Monthly: $300</div>
                      <div className="text-xs text-slate-lighter">Total: $10,800</div>
                      <Badge variant="success" className="mt-2">Lowest Cost</Badge>
                    </div>
                    <div className="rounded-lg bg-white p-4">
                      <div className="text-sm font-medium text-slate">48 Months</div>
                      <div className="mt-2 text-xs text-slate-lighter">Monthly: $238</div>
                      <div className="text-xs text-slate-lighter">Total: $11,424</div>
                      <Badge variant="info" className="mt-2">Balanced</Badge>
                    </div>
                    <div className="rounded-lg bg-white p-4">
                      <div className="text-sm font-medium text-slate">60 Months</div>
                      <div className="mt-2 text-xs text-slate-lighter">Monthly: $191</div>
                      <div className="text-xs text-slate-lighter">Total: $11,460</div>
                      <Badge variant="warning" className="mt-2">Lowest Monthly</Badge>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Best Practices Tab */}
        <TabsContent value="practices" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            {bestPractices.map((practice, idx) => (
              <motion.div
                key={practice.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
              >
                <Card
                  className={`h-full ${
                    practice.importance === 'high'
                      ? 'border-2 border-teal-200 bg-teal-50'
                      : ''
                  }`}
                >
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center">
                          <div className="mr-3 flex h-10 w-10 items-center justify-center rounded-lg bg-teal text-white">
                            <practice.icon className="h-5 w-5" />
                          </div>
                          <div>
                            <CardTitle className="text-lg">{practice.title}</CardTitle>
                            <Badge
                              variant={practice.importance === 'high' ? 'destructive' : 'secondary'}
                              className="mt-1"
                            >
                              {practice.importance === 'high' ? 'Must Do' : 'Recommended'}
                            </Badge>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-sm text-slate-light">{practice.description}</p>
                    <div>
                      <div className="mb-2 text-sm font-medium text-slate">Action Items:</div>
                      <ul className="space-y-1">
                        {practice.tips.map((tip, tipIdx) => (
                          <li
                            key={tipIdx}
                            className="flex items-start text-sm text-slate-light"
                          >
                            <CheckCircle2 className="mr-2 mt-0.5 h-4 w-4 flex-shrink-0 text-teal" />
                            {tip}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* CTA */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mt-12"
      >
        <Card className="bg-gradient-to-r from-teal-50 to-blue-50">
          <CardContent className="p-8 text-center">
            <h3 className="mb-4 text-2xl font-bold text-slate">Ready to Apply Your Knowledge?</h3>
            <p className="mb-6 text-slate-light">
              Upload your loan document and get personalized analysis
            </p>
            <div className="flex items-center justify-center gap-4">
              <Button asChild size="lg">
                <a href="/upload">Upload Document</a>
              </Button>
              <Button asChild variant="outline" size="lg">
                <a href="/chat">Ask AI Questions</a>
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
