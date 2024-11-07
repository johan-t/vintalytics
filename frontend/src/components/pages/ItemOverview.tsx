import { useEffect, useState } from "react"
import { BarChartComponent } from '@/components/ui/barchart'
import { ChartConfig } from "../ui/chart"

interface ItemOverviewProps {
    brand: string
}

interface ListingData {
    date: string
    count: number
}

interface PriceData {
    date: string
    price: number
}

interface ListingsChartData {
    month: string
    listings: number
}

interface PriceChartData {
    month: string
    price: number
}

const ItemOverview = ({ brand }: ItemOverviewProps) => {
    const [listingsChartData, setListingsChartData] = useState<ListingsChartData[]>([])
    const [priceChartData, setPriceChartData] = useState<PriceChartData[]>([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        const fetchListings = async () => {
            try {
                const encodedBrand = encodeURIComponent(brand)
                const response = await fetch(
                    `http://localhost:8000/api/${encodedBrand}/monthly/listings/count`
                )
                const data = await response.json()

                // Transform API data to chart format
                const transformedData: ListingsChartData[] = data.data.map((item: ListingData) => ({
                    month: new Date(item.date).toLocaleString('default', { month: 'long' }),
                    listings: item.count
                }))

                setListingsChartData(transformedData)
            } catch (error) {
                console.error('Error fetching data:', error)
            } finally {
                setIsLoading(false)
            }
        }

        fetchListings()
    }, [brand])

    const listingsChartConfig = {
        listings: {
            label: "Listings",
            color: "#2563eb",
            dataKey: "listings"
        },
    } satisfies ChartConfig

    const priceChartConfig = {
        listings: {
            label: "Price",
            color: "#2563eb",
            dataKey: "price"
        },
    } satisfies ChartConfig

    useEffect(() => {
        const fetchPricing = async () => {
            try {
                const encodedBrand = encodeURIComponent(brand)
                const response = await fetch(
                    `http://localhost:8000/api/${encodedBrand}/monthly/pricing/average`
                )
                const data = await response.json()

                // Transform API data to chart format
                const transformedData: PriceChartData[] = data.data.map((item: PriceData) => ({
                    month: new Date(item.date).toLocaleString('default', { month: 'long' }),
                    price: item.price
                }))

                setPriceChartData(transformedData)
                console.log(transformedData)
            } catch (error) {
                console.error('Error fetching data:', error)
            } finally {
                setIsLoading(false)
            }
        }
        fetchPricing()
    }, [brand])

    return (
        <div className="space-y-8">
            <h1 className="text-2xl font-bold text-zinc-100">{brand}</h1>
            <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-6">
                <h2 className="text-lg font-semibold text-zinc-100 mb-4">Monthly Listings</h2>
                <BarChartComponent data={listingsChartData} isLoading={isLoading} chartConfig={listingsChartConfig} />
            </div>
            <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-6">
                <h2 className="text-lg font-semibold text-zinc-100 mb-4">Monthly Pricing</h2>
                <BarChartComponent data={priceChartData} isLoading={isLoading} chartConfig={priceChartConfig} />
            </div>
        </div>
    )
}

export default ItemOverview