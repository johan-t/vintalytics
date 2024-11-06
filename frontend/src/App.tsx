import { useEffect, useState } from "react";

import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import ItemOverview from "@/components/pages/ItemOverview";

interface BrandsResponse {
  brands: string[];
}

function App() {
  const [selectedBrand, setSelectedBrand] = useState<string | null>(null);
  const [brands, setBrands] = useState<string[]>([]);
  const [filteredBrands, setFilteredBrands] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [key, setKey] = useState(0);

  useEffect(() => {
    const fetchBrands = async () => {
      try {
        const response = await fetch("http://localhost:8000/brands");
        const data: BrandsResponse = await response.json();
        setBrands(data.brands);
        setFilteredBrands(data.brands.slice(0, 15));
      } catch (error) {
        console.error('Error fetching brands:', error);
      }
    };

    fetchBrands();
  }, []);

  const handleSearch = (value: string) => {
    setSearchQuery(value);
    
    if (value.trim() === "") {
      setFilteredBrands(brands.slice(0, 15));
    } else {
      const filtered = brands.filter(brand => 
        brand.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredBrands(filtered);
    }
  };

  const handleSelectBrand = (brand: string) => {
    setSelectedBrand(brand);
    setSearchQuery("");
    setKey(prev => prev + 1);
  };

  return (
    <div className="min-h-screen w-full bg-zinc-950 p-4">
      <div className={`transition-all duration-300 ${selectedBrand ? 'pt-4' : 'flex items-center justify-center min-h-screen'}`}>
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
      </div>

      {selectedBrand && <ItemOverview brand={selectedBrand} />}
    </div>
  );
}

export default App;