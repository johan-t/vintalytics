import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"

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
  return (
    <div className="min-h-screen w-full bg-zinc-950 flex items-center justify-center p-4">
      <Command className="rounded-lg border max-w-lg w-full border-zinc-800 bg-zinc-950">
        <CommandInput
          placeholder="Search for a brand..."
          className="border-none focus:ring-0 text-zinc-100 text-md h-[60px]"
        />
        <CommandList>
          <CommandEmpty >No results found.</CommandEmpty>
          {searchItems.map((section) => (
            <CommandGroup key={section.category} heading={section.category}>
              {section.items.map((item) => (
                <CommandItem
                  key={item.title}
                  onSelect={() => window.location.href = item.url}
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
  )
}

export default App