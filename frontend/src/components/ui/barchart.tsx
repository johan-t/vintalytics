"use client"

import { useEffect, useState } from "react"
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts"
import {
  ChartConfig,
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

interface ListingData {
  date: string
  count: number
}

interface ChartData {
  month: string
  listings: number
}

interface BarChartProps {
  brand: string
}

const chartConfig = {
  listings: {
    label: "Listings",
    color: "#2563eb",
  },
} satisfies ChartConfig

export function BarChartComponent({ brand }: BarChartProps) {
  const [chartData, setChartData] = useState<ChartData[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const encodedBrand = encodeURIComponent(brand)
        const response = await fetch(
          `http://localhost:8000/api/${encodedBrand}/monthly/listings/count`
        )
        const data = await response.json()

        // Transform API data to chart format
        const transformedData: ChartData[] = data.data.map((item: ListingData) => ({
          month: new Date(item.date).toLocaleString('default', { month: 'long' }),
          listings: item.count
        }))

        setChartData(transformedData)
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [brand])

  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <ChartContainer config={chartConfig} className="min-h-[400px] w-full">
      <BarChart accessibilityLayer data={chartData}>
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
