import { useParams } from 'react-router-dom';
import { useEffect, useState, useContext } from 'react';
import GameCard from '../components/GameCard';
import apiClient from "@/api/client";
import { useAuth } from "@/context/AuthContext";

export default function UserStore() {
  const { username } = useParams();
  const { user } = useAuth();
  const [games, setGames] = useState([]);
  const [isOwner, setIsOwner] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserStore = async () => {
      try {
        const res = await apiClient.get(`/store/${username}/games`);
        setGames(res.data);

        const userIsOwner =
          user && user.username === username && user.role === "publisher";
        setIsOwner(userIsOwner);
      } catch (err) {
        console.error(err);
        setError("Failed to fetch store");
      }
    };

    fetchUserStore();
  }, [username, user]);

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

      {games.length === 0 ? (
        <p className="text-gray-400 italic">This user has no games yet.</p>
      ) : (
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
      )}
    </div>
  );
}
