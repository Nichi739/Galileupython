import { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiGet, apiPost } from '../lib/api';
import { supabase } from '../lib/supabaseClient';
import ChatBox from '../components/ChatBox.jsx';
import VoiceChannel from '../components/VoiceChannel.jsx';
import MemberList from '../components/MemberList.jsx';

export default function Room() {
  const { roomId } = useParams();
  const navigate = useNavigate();

  const [me, setMe] = useState(null);
  const [details, setDetails] = useState(null);
  const [activeChannel, setActiveChannel] = useState(null);
  const [newChannelName, setNewChannelName] = useState('');
  const [error, setError] = useState('');

  const loadDetails = useCallback(async () => {
    try {
      const data = await apiGet(`/rooms/${roomId}/details`);
      setDetails(data);
      if (!activeChannel && data.channels.length > 0) {
        setActiveChannel(data.channels[0]);
      }
    } catch (err) {
      setError(err.message);
    }
  }, [roomId]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      const { data: profile } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', data.user.id)
        .single();
      setMe(profile);
    });
    loadDetails();
  }, [loadDetails]);

  async function handleCreateChannel(type) {
    if (!newChannelName.trim()) return;
    try {
      await apiPost('/channels', { roomId, name: newChannelName, type });
      setNewChannelName('');
      loadDetails();
    } catch (err) {
      setError(err.message);
    }
  }

  if (!details || !me) return <div className="center-screen">Carregando sala...</div>;

  const textChannels = details.channels.filter((c) => c.type === 'text');
  const voiceChannels = details.channels.filter((c) => c.type === 'voice');
  const canManage = details.myRole === 'owner' || details.myRole === 'moderator';

  return (
    <div className="room-layout">
      <aside className="sidebar">
        <button className="link-button" onClick={() => navigate('/')}>← Salas</button>

        <h4>Canais de texto</h4>
        <ul className="channel-list">
          {textChannels.map((c) => (
            <li
              key={c.id}
              className={activeChannel?.id === c.id ? 'active' : ''}
              onClick={() => setActiveChannel(c)}
            >
              # {c.name}
            </li>
          ))}
        </ul>

        <h4>Canais de voz</h4>
        <ul className="channel-list">
          {voiceChannels.map((c) => (
            <li
              key={c.id}
              className={activeChannel?.id === c.id ? 'active' : ''}
              onClick={() => setActiveChannel(c)}
            >
              🔊 {c.name}
            </li>
          ))}
        </ul>

        {canManage && (
          <div className="new-channel-form">
            <input
              placeholder="Novo canal"
              value={newChannelName}
              onChange={(e) => setNewChannelName(e.target.value)}
            />
            <div>
              <button onClick={() => handleCreateChannel('text')}>+ texto</button>
              <button onClick={() => handleCreateChannel('voice')}>+ voz</button>
            </div>
          </div>
        )}
      </aside>

      <main className="main-content">
        {error && <p className="error-text">{error}</p>}
        {activeChannel?.type === 'text' && <ChatBox channel={activeChannel} user={me} />}
        {activeChannel?.type === 'voice' && <VoiceChannel channel={activeChannel} user={me} />}
      </main>

      <MemberList
        roomId={roomId}
        members={details.members}
        myRole={details.myRole}
        onChanged={loadDetails}
      />
    </div>
  );
}
