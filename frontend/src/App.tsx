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

  useEffect(() => {
    const fetchBrands = async () => {
      try {
        const response = await fetch("http://localhost:8000/brands");
        const data: BrandsResponse = await response.json();
        setBrands(data.brands);
      } catch (error) {
        console.error('Error fetching brands:', error);
      }
    };

    fetchBrands();
  }, []);

  return (
    <div className="min-h-screen w-full bg-zinc-950 p-4">
      <div className={`transition-all duration-300 ${selectedBrand ? 'pt-4' : 'flex items-center justify-center min-h-screen'}`}>
        <Command className="rounded-lg border max-w-lg w-full border-zinc-800 bg-zinc-950 mx-auto">
          <CommandInput
            placeholder="Search for a brand..."
            className="border-none focus:ring-0 text-zinc-100 text-md h-[60px]"
            onFocus={() => {
              setSelectedBrand(null);
            }}
          />
          {!selectedBrand && (
            <CommandList>
              <CommandEmpty>No results found.</CommandEmpty>
              <CommandGroup heading="Brands">
                {brands.map((brand) => (
                  <CommandItem
                    key={brand}
                    onSelect={() => setSelectedBrand(brand)}
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

      {selectedBrand && (
        <div className="mt-8">
          <ItemOverview brand={selectedBrand} />
        </div>
      )}
    </div>
  )
}

export default App