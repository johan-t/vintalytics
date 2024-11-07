import { useEffect, useState, useCallback } from "react"
import { BarChartComponent } from '@/components/ui/barchart'
import { ChartConfig } from "../ui/chart"

interface TimeSeriesData {
    date: string;
    [key: string]: string | number;
}

interface ChartData {
    month: string;
    [key: string]: string | number;
}

interface ItemOverviewProps {
    brand: string;
}

type DataType = 'listings' | 'pricing';
type ValueKey = 'count' | 'price';

const ItemOverview = ({ brand }: ItemOverviewProps) => {
    const [listingsChartData, setListingsChartData] = useState<ChartData[]>([]);
    const [priceChartData, setPriceChartData] = useState<ChartData[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    const fetchTimeSeriesData = useCallback(async (
        dataType: DataType,
        valueKey: ValueKey,
        setData: (data: ChartData[]) => void
    ) => {
        try {
            const encodedBrand = encodeURIComponent(brand);
            const endpoint = dataType === 'listings' ? 'count' : 'average';
            const response = await fetch(
                `http://localhost:8000/api/${encodedBrand}/monthly/${dataType}/${endpoint}`
            );
            const data = await response.json();

            // Transform API data to chart format
            const transformedData: ChartData[] = data.data.map((item: TimeSeriesData) => ({
                month: new Date(item.date).toLocaleString('default', { month: 'long' }),
                [dataType === 'listings' ? 'listings' : 'price']: item[valueKey] as number
            }));

            setData(transformedData);
        } catch (error) {
            console.error(`Error fetching ${dataType} data:`, error);
        } finally {
            setIsLoading(false);
        }
    }, [brand]);

    useEffect(() => {
        fetchTimeSeriesData('listings', 'count', setListingsChartData);
        fetchTimeSeriesData('pricing', 'price', setPriceChartData);
    }, [brand, fetchTimeSeriesData]);

    const listingsChartConfig = {
        listings: {
            label: "Listings",
            color: "#2563eb",
            dataKey: "listings"
        },
    } satisfies ChartConfig

    const priceChartConfig = {
        listings: {
            label: "Pricing",
            color: "#2563eb",
            dataKey: "price"
        },
    } satisfies ChartConfig

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