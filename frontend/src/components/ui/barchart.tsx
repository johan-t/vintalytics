"use client"

import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts"
import {
  ChartConfig,
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { ChartData } from "@/components/pages/ItemOverview"

interface BarChartProps {
  data: ChartData[]
  isLoading: boolean
  chartConfig: ChartConfig
}

export function BarChartComponent({ data, isLoading, chartConfig }: BarChartProps) {
  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <ChartContainer config={chartConfig} className="min-h-[400px] w-full">
      <BarChart accessibilityLayer data={data}>
        <CartesianGrid vertical={false} />
        <XAxis
          dataKey="month"
          tickLine={false}
          tickMargin={10}
          axisLine={false}
          tickFormatter={(value) => value.slice(0, 3)}
        />
        <YAxis
          tickLine={false}
          tickMargin={10}
          axisLine={false}
        />
        <ChartTooltip content={<ChartTooltipContent />} />
        <ChartLegend content={<ChartLegendContent />} />
        <Bar dataKey="listings" fill="var(--color-listings)" radius={4} />
      </BarChart>
    </ChartContainer>
  )
}
