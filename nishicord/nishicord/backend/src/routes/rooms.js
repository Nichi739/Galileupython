import { Router } from 'express';
import { supabase, requireAuth } from '../supabaseClient.js';

export const roomsRouter = Router();

// Lista as salas em que o usuário logado é membro
roomsRouter.get('/', requireAuth, async (req, res) => {
  const { data, error } = await supabase
    .from('room_members')
    .select('role, rooms(id, name, invite_code, owner_id)')
    .eq('user_id', req.user.id);

  if (error) return res.status(500).json({ error: error.message });

  const rooms = data.map((row) => ({ ...row.rooms, role: row.role }));
  res.json(rooms);
});

// Cria uma sala nova e já cria um canal de texto "geral" e um de voz "Geral"
roomsRouter.post('/', requireAuth, async (req, res) => {
  const { name } = req.body;
  if (!name) return res.status(400).json({ error: 'Nome da sala é obrigatório' });

  const { data: room, error: roomError } = await supabase
    .from('rooms')
    .insert({ name, owner_id: req.user.id })
    .select()
    .single();

  if (roomError) return res.status(500).json({ error: roomError.message });

  await supabase.from('room_members').insert({
    room_id: room.id,
    user_id: req.user.id,
    role: 'owner',
  });

  await supabase.from('channels').insert([
    { room_id: room.id, name: 'geral', type: 'text' },
    { room_id: room.id, name: 'Geral', type: 'voice' },
  ]);

  res.status(201).json(room);
});

// Entrar numa sala usando o código de convite
roomsRouter.post('/join', requireAuth, async (req, res) => {
  const { inviteCode } = req.body;

  const { data: room, error: roomError } = await supabase
    .from('rooms')
    .select('*')
    .eq('invite_code', inviteCode)
    .single();

  if (roomError || !room) {
    return res.status(404).json({ error: 'Código de convite inválido' });
  }

  const { error: memberError } = await supabase
    .from('room_members')
    .upsert(
      { room_id: room.id, user_id: req.user.id, role: 'member' },
      { onConflict: 'room_id,user_id', ignoreDuplicates: true }
    );

  if (memberError) return res.status(500).json({ error: memberError.message });

  res.json(room);
});

// Lista canais + membros de uma sala (só se o usuário for membro)
roomsRouter.get('/:roomId/details', requireAuth, async (req, res) => {
  const { roomId } = req.params;

  const { data: membership } = await supabase
    .from('room_members')
    .select('role')
    .eq('room_id', roomId)
    .eq('user_id', req.user.id)
    .maybeSingle();

  if (!membership) return res.status(403).json({ error: 'Você não é membro dessa sala' });

  const { data: channels } = await supabase
    .from('channels')
    .select('*')
    .eq('room_id', roomId)
    .order('created_at');

  const { data: members } = await supabase
    .from('room_members')
    .select('role, profiles(id, username, avatar_url, status)')
    .eq('room_id', roomId);

  res.json({
    myRole: membership.role,
    channels,
    members: members.map((m) => ({ ...m.profiles, role: m.role })),
  });
});

// Expulsar membro (só dono ou moderador)
roomsRouter.delete('/:roomId/members/:userId', requireAuth, async (req, res) => {
  const { roomId, userId } = req.params;

  const { data: membership } = await supabase
    .from('room_members')
    .select('role')
    .eq('room_id', roomId)
    .eq('user_id', req.user.id)
    .maybeSingle();

  if (!membership || !['owner', 'moderator'].includes(membership.role)) {
    return res.status(403).json({ error: 'Sem permissão para remover membros' });
  }

  await supabase
    .from('room_members')
    .delete()
    .eq('room_id', roomId)
    .eq('user_id', userId);

  res.status(204).end();
});
