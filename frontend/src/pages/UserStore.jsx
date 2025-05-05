import { useParams } from 'react-router-dom';

export default function UserStore() {
  const { username } = useParams();

  return (
    <div className="text-white p-8 min-h-screen">
      <h1 className="text-3xl font-bold">User Store: {username}</h1>
      <p className="mt-4">Here you'll find your uploaded games and drafts.</p>
    </div>
  );
}
