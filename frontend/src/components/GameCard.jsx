import { Link } from 'react-router-dom';

export default function GameCard({ username, gameId, title, image, price, discount = 0 }) {
  const finalPrice = discount ? price - (price * discount) / 100 : price;

  return (
    <Link to={`/store/${username}/${gameId}`} className="block bg-gray-800 rounded-lg overflow-hidden hover:scale-105 transition-transform">
      <img src={image} alt={title} className="w-full h-40 object-cover" />
      <div className="p-4 text-white">
        <h2 className="text-lg font-bold mb-1">{title}</h2>
        <div className="text-sm">
          {discount ? (
            <div className="flex gap-2">
              <span className="line-through text-red-400">${price}</span>
              <span className="text-green-400">${finalPrice.toFixed(2)}</span>
              <span className="ml-auto text-sm bg-red-500 px-2 py-0.5 rounded-full">{discount}% OFF</span>
            </div>
          ) : (
            <span>${price}</span>
          )}
        </div>
      </div>
    </Link>
  );
}
