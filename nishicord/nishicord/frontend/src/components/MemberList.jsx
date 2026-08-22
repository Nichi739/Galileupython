import { apiDelete } from '../lib/api';

export default function MemberList({ roomId, members, myRole, onChanged }) {
  const canManage = myRole === 'owner' || myRole === 'moderator';

  async function handleKick(userId) {
    if (!confirm('Remover esse membro da sala?')) return;
    await apiDelete(`/rooms/${roomId}/members/${userId}`);
    onChanged();
  }

  return (
    <div className="member-list">
      <h3>Membros</h3>
      <ul>
        {members.map((m) => (
          <li key={m.id}>
            <span className={`status-dot status-${m.status}`} />
            {m.username} <span className="muted">({m.role})</span>
            {canManage && m.role !== 'owner' && (
              <button className="link-button danger" onClick={() => handleKick(m.id)}>
                remover
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
