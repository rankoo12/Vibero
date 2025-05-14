import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import GameCard from '../components/GameCard';
import { apiRequest } from '@/api';

export default function UserStore() {
  const { username } = useParams();
  const [games, setGames] = useState([]);
  const [isOwner, setIsOwner] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const data = await apiRequest(`/store/${username}`, {
          method: 'GET',
          credentials: 'include',
        });

        setGames(data);

        // Owner check
        // await apiRequest(`/store/${username}/game`, {
        //   method: 'POST',
        //   credentials: 'include',
        //   body: { title: '__check__', description: 'tmp' },
        // });

        setIsOwner(true);

      } catch (err) {
        if (err.message.includes('403')) {
          setIsOwner(false);
        } else {
          console.error(err);
          setError("Failed to fetch store");
        }
      }
    };

    fetchGames();
  }, [username]);

  if (error) return <div className="text-red-400 p-8">{error}</div>;

  return (
    <div className="p-8">
      <h1 className="text-white text-2xl font-bold mb-4">
        {username}'s Games
      </h1>

      {isOwner && (
        <button className="bg-blue-600 text-white px-4 py-2 rounded mb-4">
          + Add Game
        </button>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {games.map((game) => (
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
  );
}
