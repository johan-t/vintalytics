import { useEffect, useState, useCallback } from "react"
import { BarChartComponent } from '@/components/ui/barchart'
import { ChartConfig } from "../ui/chart"
import { config } from "@/env";
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "@/components/ui/command"

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

interface KeywordAnalysis {
    average_price: number;
    count: number;
    min_price: number;
    max_price: number;
}

type DataType = 'listings' | 'pricing';
type ValueKey = 'count' | 'price';

const ItemOverview = ({ brand }: ItemOverviewProps) => {
    const [listingsChartData, setListingsChartData] = useState<ChartData[]>([]);
    const [priceChartData, setPriceChartData] = useState<ChartData[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [tagAnalysis, setTagAnalysis] = useState<KeywordAnalysis | null>(null);
    const [suggestedTags, setSuggestedTags] = useState<{ word: string; count: number }[]>([]);
    const [isCommandOpen, setIsCommandOpen] = useState(false);

    const fetchTimeSeriesData = useCallback(async (
        dataType: DataType,
        valueKey: ValueKey,
        setData: (data: ChartData[]) => void
    ) => {
        try {
            const encodedBrand = encodeURIComponent(brand);
            const endpoint = dataType === 'listings' ? 'count' : 'average';
            const response = await fetch(
                `${config.apiUrl}/api/${encodedBrand}/monthly/${dataType}/${endpoint}`
            );
            const data = await response.json();

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

    const fetchTopTags = useCallback(async () => {
        try {
            const encodedBrand = encodeURIComponent(brand);
            const response = await fetch(
                `${config.apiUrl}/api/${encodedBrand}/keywords/top/50`
            );
            const data = await response.json();
            setSuggestedTags(data.keywords || []);
        } catch (error) {
            console.error('Error fetching top tags:', error);
        }
    }, [brand]);

    const fetchTagAnalysis = useCallback(async () => {
        if (selectedTags.length === 0) {
            setTagAnalysis(null);
            return;
        }

        try {
            const encodedBrand = encodeURIComponent(brand);
            const encodedTags = selectedTags.join(',');
            const response = await fetch(
                `${config.apiUrl}/api/${encodedBrand}/keywords/${encodedTags}`
            );
            const data = await response.json();
            setTagAnalysis(data.analysis);
        } catch (error) {
            console.error('Error fetching tag analysis:', error);
        }
    }, [brand, selectedTags]);

    useEffect(() => {
        fetchTimeSeriesData('listings', 'count', (data) => setListingsChartData(sortDataByMonth(data)));
        fetchTimeSeriesData('pricing', 'price', (data) => setPriceChartData(sortDataByMonth(data)));
        fetchTopTags();
    }, [brand, fetchTimeSeriesData, fetchTopTags]);


    useEffect(() => {
        fetchTagAnalysis();
    }, [fetchTagAnalysis, selectedTags]);

    const handleSelectTag = (tag: string) => {
        if (selectedTags.includes(tag)) {
            setSelectedTags(selectedTags.filter(t => t !== tag));
        } else {
            setSelectedTags([...selectedTags, tag]);
        }
    };

    const listingsChartConfig = {
        listings: {
            label: "Listings",
            color: "#2563eb",
            dataKey: "listings"
        },
    } satisfies ChartConfig

    const priceChartConfig = {
        price: {
            label: "Average Price",
            color: "#2563eb",
            dataKey: "price"
        },
    } satisfies ChartConfig

    const sortDataByMonth = (data: ChartData[]): ChartData[] => {
        const monthOrder = [
            "Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
        ];
        return data.sort((a, b) => monthOrder.indexOf(a.month) - monthOrder.indexOf(b.month));
    };

    return (
        <div className="space-y-8">
            <h1 className="text-2xl font-bold text-zinc-100">{brand}</h1>

            <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-6">
                <h2 className="text-lg font-semibold text-zinc-100 mb-4">Search by Tags</h2>
                <Command
                    className="rounded-lg border border-zinc-800 bg-zinc-950"
                    shouldFilter={true}
                    onClick={() => setIsCommandOpen(true)}
                >
                    <CommandInput
                        placeholder="Search tags..."
                        className="border-none focus:ring-0 text-zinc-100"
                    />
                    {isCommandOpen && (
                        <CommandList>
                            <CommandEmpty>No tags found.</CommandEmpty>
                            <CommandGroup heading="Suggested Tags">
                                {suggestedTags.map((tag) => (
                                    <CommandItem
                                        key={tag.word}
                                        onSelect={() => handleSelectTag(tag.word)}
                                        className="text-zinc-100 cursor-pointer"
                                    >
                                        {tag.word} ({tag.count})
                                    </CommandItem>
                                ))}
                            </CommandGroup>
                        </CommandList>
                    )}
                </Command>

                {selectedTags.length > 0 && (
                    <div className="mt-4 space-y-2">
                        <div className="flex flex-wrap gap-2">
                            {selectedTags.map((tag) => (
                                <span
                                    key={tag}
                                    className="px-2 py-1 rounded-md bg-blue-500 text-white text-sm cursor-pointer hover:bg-blue-600"
                                    onClick={() => handleSelectTag(tag)}
                                >
                                    {tag}
                                </span>
                            ))}
                        </div>
                        {tagAnalysis && (
                            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="p-4 rounded-lg bg-zinc-900">
                                    <p className="text-sm text-zinc-400">Average Price</p>
                                    <p className="text-xl font-bold text-zinc-100">
                                        €{tagAnalysis.average_price.toFixed(2)}
                                    </p>
                                </div>
                                <div className="p-4 rounded-lg bg-zinc-900">
                                    <p className="text-sm text-zinc-400">Listings</p>
                                    <p className="text-xl font-bold text-zinc-100">
                                        {tagAnalysis.count}
                                    </p>
                                </div>
                                <div className="p-4 rounded-lg bg-zinc-900">
                                    <p className="text-sm text-zinc-400">Min Price</p>
                                    <p className="text-xl font-bold text-zinc-100">
                                        €{tagAnalysis.min_price.toFixed(2)}
                                    </p>
                                </div>
                                <div className="p-4 rounded-lg bg-zinc-900">
                                    <p className="text-sm text-zinc-400">Max Price</p>
                                    <p className="text-xl font-bold text-zinc-100">
                                        €{tagAnalysis.max_price.toFixed(2)}
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>

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