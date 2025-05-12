import { useParams } from 'react-router-dom';
import GameCard from '../components/GameCard'

export default function UserStore() {
  const { username } = useParams();
  if (!username) return <div className="text-white p-8">No user selected</div>;
  const games = [ // mock for now
    { id: 'fifa25', title: 'EA FC 25', image: '/src/assets/fifa.jpg', price: 69.99, discount: 10 },
    { id: 'zelda', title: 'Zelda X', image: '/src/assets/zelda.jpg', price: 49.99 },
  ]

  return (
    <div className="p-8">
      <h1 className="text-white text-2xl font-bold mb-4">{username}'s Games</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {games.map(game => (
          <GameCard
            key={game.id}
            username={username}
            gameId={game.id}
            title={game.title}
            image={game.image}
            price={game.price}
            discount={game.discount}
          />
        ))}
      </div>
    </div>
  )
}
