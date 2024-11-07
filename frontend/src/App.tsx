import { useEffect, useState } from "react";
import { config } from "@/env";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import { PieChartComponent } from "@/components/ui/piechart";
import ItemOverview from "@/components/pages/ItemOverview";

interface BrandsResponse {
  brands: { brand: string; count: number }[];
}

function App() {
  const [selectedBrand, setSelectedBrand] = useState<string | null>(null);
  const [brandsData, setBrandsData] = useState<{ brand: string; count: number }[]>([]);
  const [filteredBrands, setFilteredBrands] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [key, setKey] = useState(0);

  useEffect(() => {
    const fetchBrands = async () => {
      try {
        const response = await fetch(`${config.apiUrl}/api/brands`);
        const data: BrandsResponse = await response.json();
        setBrandsData(data.brands);
        setFilteredBrands(data.brands.slice(0, 15).map(brand => brand.brand));
      } catch (error) {
        console.error('Error fetching brands:', error);
      }
    };

    fetchBrands();
  }, []);

  const handleSearch = (value: string) => {
    setSearchQuery(value);

    if (value.trim() === "") {
      setFilteredBrands(brandsData.slice(0, 15).map(brand => brand.brand));
    } else {
      const filtered = brandsData
        .filter(brand => brand.brand.toLowerCase().includes(value.toLowerCase()))
        .map(brand => brand.brand);
      setFilteredBrands(filtered);
    }
  };

  const handleSelectBrand = (brand: string) => {
    setSelectedBrand(brand);
    setSearchQuery("");
    setKey(prev => prev + 1);
  };

  // Transform data for pie chart
  const pieChartData = brandsData
    .slice(0, 10)
    .map(item => ({
      name: item.brand,
      value: item.count
    }));

  return (
    <div className="min-h-screen w-full bg-zinc-950 p-4">
      <div className={`transition-all duration-300 ${selectedBrand ? 'pt-4' : 'flex flex-col items-center justify-center min-h-screen'}`}>
        <Command
          key={key}
          className="rounded-lg border max-w-lg w-full border-zinc-800 bg-zinc-950 mx-auto"
        >
          <CommandInput
            placeholder="Search for a brand..."
            className="border-none focus:ring-0 text-zinc-100 text-md h-[60px]"
            value={searchQuery}
            onValueChange={handleSearch}
            onFocus={() => {
              setSelectedBrand(null);
            }}
          />
          {!selectedBrand && (
            <CommandList>
              <CommandEmpty>No results found.</CommandEmpty>
              <CommandGroup heading="Brands">
                {filteredBrands.map((brand) => (
                  <CommandItem
                    key={brand}
                    onSelect={() => handleSelectBrand(brand)}
                    className="text-zinc-100 cursor-pointer"
                  >
                    {brand}
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          )}
        </Command>

        {!selectedBrand && brandsData.length > 0 && (
          <div className="mt-8 w-full max-w-lg mx-auto">
            <h3 className="text-lg font-semibold mb-4 text-zinc-100">Top 10 Brands Distribution</h3>
            <PieChartComponent data={pieChartData} onBrandSelect={handleSelectBrand} />
          </div>
        )}
      </div>

      {selectedBrand && (
        <div className="w-full max-w-3xl mx-auto">
          <ItemOverview brand={selectedBrand} />
        </div>
      )}
    </div>
  );
}

export default App;