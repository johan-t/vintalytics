import { useEffect, useState } from "react"
import { BarChartComponent } from '@/components/ui/barchart'

interface ItemOverviewProps {
    brand: string
}

interface ListingData {
    date: string
    count: number
}

interface ChartData {
    month: string
    listings: number
}

const ItemOverview = ({ brand }: ItemOverviewProps) => {
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

    return (
        <div className="space-y-8">
            <h1 className="text-2xl font-bold text-zinc-100">{brand}</h1>
            <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-6">
                <h2 className="text-lg font-semibold text-zinc-100 mb-4">Monthly Listings</h2>
                <BarChartComponent data={chartData} isLoading={isLoading} />
            </div>
        </div>
    )
}

export default ItemOverview