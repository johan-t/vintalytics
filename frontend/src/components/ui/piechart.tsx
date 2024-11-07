"use client"

import { Cell, Pie, PieChart as RechartsPieChart } from "recharts"
import {
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart"

interface PieChartProps {
    data: { name: string; value: number }[]
    isLoading?: boolean
    onBrandSelect?: (brand: string) => void
}

export function PieChartComponent({ data, isLoading, onBrandSelect }: PieChartProps) {
    if (isLoading) {
        return <div>Loading...</div>
    }

    const COLORS = [
        'hsl(var(--chart-1))',
        'hsl(var(--chart-2))',
        'hsl(var(--chart-3))',
        'hsl(var(--chart-4))',
        'hsl(var(--chart-5))',
    ]

    const chartConfig = data.reduce((acc, item) => {
        acc[item.name] = {
            label: item.name,
            color: COLORS[Object.keys(acc).length % COLORS.length],
            dataKey: item.name,
        }
        return acc
    }, {} as Record<string, { label: string; color: string; dataKey: string }>)

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleClick = (data: any) => {
        if (onBrandSelect && data.name) {
            onBrandSelect(data.name);
        }
    };

    return (
        <ChartContainer config={chartConfig} className="min-h-[400px] w-full">
            <RechartsPieChart>
                <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={2}
                    dataKey="value"
                    onClick={handleClick}
                >
                    {data.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <ChartTooltip content={<ChartTooltipContent />} />
                <ChartLegend content={<ChartLegendContent />} />
            </RechartsPieChart>
        </ChartContainer>
    )
}