import { useState } from "react";

import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import ItemOverview from "@/components/pages/ItemOverview";


const searchItems = [
  {
    category: "Brands",
    items: [
      { title: "Zara", url: "#zara" },
      { title: "H&M", url: "#h&m" },
      { title: "Uniqlo", url: "#uniqlo" },
    ],
  }
]

function App() {

  const [selectedBrand, setSelectedBrand] = useState<string | null>(null);

  return (
    <div className="min-h-screen w-full bg-zinc-950 p-4">
      <div className={`transition-all duration-300 ${selectedBrand ? 'pt-4' : 'flex items-center justify-center min-h-screen'
        }`}>
        <Command className="rounded-lg border max-w-lg w-full border-zinc-800 bg-zinc-950 mx-auto">
          <CommandInput
            placeholder="Search for a brand..."
            className="border-none focus:ring-0 text-zinc-100 text-md h-[60px]"
          />
          <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            {searchItems.map((section) => (
              <CommandGroup key={section.category} heading={section.category}>
                {section.items.map((item) => (
                  <CommandItem
                    key={item.title}
                    onSelect={() => setSelectedBrand(item.title)}
                    className="text-zinc-100 cursor-pointer"
                  >
                    {item.title}
                  </CommandItem>
                ))}
              </CommandGroup>
            ))}
          </CommandList>
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