interface ItemOverviewProps {
	brand: string;
}

import { BarChartComponent } from '@/components/ui/barchart';

const ItemOverview = ({ brand }: ItemOverviewProps) => {
	return (
		<div className="space-y-8">
			<h1 className="text-2xl font-bold text-zinc-100">{brand}</h1>
			<div className="rounded-lg border border-zinc-800 bg-zinc-950 p-6">
				<h2 className="text-lg font-semibold text-zinc-100 mb-4">Monthly Listings</h2>
				<BarChartComponent brand={brand} />
			</div>
		</div>
	);
};

export default ItemOverview;
