import { useParams } from 'react-router-dom';

export default function GamePage() {
  const { username, gameId } = useParams();

  // Later, fetch game data by username + gameId
  return (
    <div className="text-white p-8">
      <h1 className="text-3xl font-bold">Game: {gameId}</h1>
      <p className="mt-2 text-gray-400">By: {username}</p>

      {/* Placeholder for screenshots, video, and description */}
      <div className="mt-6">
        <div className="w-full h-64 bg-gray-700 rounded-lg mb-4">[ Game Banner Image ]</div>
        <p className="text-lg">Game description goes here...</p>
      </div>
    </div>
  );
}
