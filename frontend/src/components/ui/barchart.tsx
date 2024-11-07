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

interface BarChartProps {
  data: unknown[]
  isLoading: boolean
  chartConfig: ChartConfig
}

export function BarChartComponent({ data, isLoading, chartConfig }: BarChartProps) {
  if (isLoading) {
    return <div>Loading...</div>
  }

  // Get the first config entry's dataKey and color
  const firstConfig = Object.values(chartConfig)[0]
  const dataKey = firstConfig?.dataKey || 'listings'
  const color = firstConfig?.color || 'var(--color-listings)'

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
        <Bar dataKey={dataKey} fill={color} radius={4} />
      </BarChart>
    </ChartContainer>
  )
}
