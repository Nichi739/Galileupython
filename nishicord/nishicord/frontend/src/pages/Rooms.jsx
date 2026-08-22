import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiGet, apiPost } from '../lib/api';
import { supabase } from '../lib/supabaseClient';

export default function Rooms() {
  const [rooms, setRooms] = useState([]);
  const [newRoomName, setNewRoomName] = useState('');
  const [inviteCode, setInviteCode] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  async function loadRooms() {
    try {
      setRooms(await apiGet('/rooms'));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadRooms();
  }, []);

  async function handleCreateRoom(e) {
    e.preventDefault();
    if (!newRoomName.trim()) return;
    try {
      const room = await apiPost('/rooms', { name: newRoomName });
      setNewRoomName('');
      navigate(`/rooms/${room.id}`);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleJoinRoom(e) {
    e.preventDefault();
    if (!inviteCode.trim()) return;
    try {
      const room = await apiPost('/rooms/join', { inviteCode });
      setInviteCode('');
      navigate(`/rooms/${room.id}`);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="page">
      <header className="page-header">
        <h1>Suas salas</h1>
        <button className="link-button" onClick={() => supabase.auth.signOut()}>
          Sair
        </button>
      </header>

      {error && <p className="error-text">{error}</p>}

      <ul className="room-list">
        {rooms.map((room) => (
          <li key={room.id} onClick={() => navigate(`/rooms/${room.id}`)}>
            <strong>{room.name}</strong>
            <span className="muted"> — convite: {room.invite_code}</span>
          </li>
        ))}
        {rooms.length === 0 && <p className="muted">Você ainda não está em nenhuma sala.</p>}
      </ul>

      <div className="two-columns">
        <form onSubmit={handleCreateRoom}>
          <h3>Criar sala nova</h3>
          <input
            placeholder="Nome da sala"
            value={newRoomName}
            onChange={(e) => setNewRoomName(e.target.value)}
          />
          <button type="submit">Criar</button>
        </form>

        <form onSubmit={handleJoinRoom}>
          <h3>Entrar com convite</h3>
          <input
            placeholder="Código de convite"
            value={inviteCode}
            onChange={(e) => setInviteCode(e.target.value)}
          />
          <button type="submit">Entrar</button>
        </form>
      </div>
    </div>
  );
}
