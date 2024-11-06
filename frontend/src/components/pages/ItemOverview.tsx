interface ItemOverviewProps {
    brand: string;
}

const ItemOverview = ({ brand }: ItemOverviewProps) => {
    return (
        <div>
            <h1>{brand}</h1>
        </div>
    )
}

export default ItemOverview;