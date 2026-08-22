import { Router } from 'express';
import { supabase, requireAuth } from '../supabaseClient.js';
import { createLiveKitToken } from '../livekit.js';

export const channelsRouter = Router();

// Cria um canal novo dentro de uma sala (só dono/moderador)
channelsRouter.post('/', requireAuth, async (req, res) => {
  const { roomId, name, type } = req.body;

  const { data: membership } = await supabase
    .from('room_members')
    .select('role')
    .eq('room_id', roomId)
    .eq('user_id', req.user.id)
    .maybeSingle();

  if (!membership || !['owner', 'moderator'].includes(membership.role)) {
    return res.status(403).json({ error: 'Sem permissão para criar canais' });
  }

  const { data, error } = await supabase
    .from('channels')
    .insert({ room_id: roomId, name, type })
    .select()
    .single();

  if (error) return res.status(500).json({ error: error.message });
  res.status(201).json(data);
});

// Histórico de mensagens de um canal de texto
channelsRouter.get('/:channelId/messages', requireAuth, async (req, res) => {
  const { data, error } = await supabase
    .from('messages')
    .select('id, content, created_at, profiles(id, username, avatar_url)')
    .eq('channel_id', req.params.channelId)
    .order('created_at', { ascending: true })
    .limit(100);

  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});

// Gera o token do LiveKit para o usuário entrar num canal de voz/vídeo
channelsRouter.post('/:channelId/voice-token', requireAuth, async (req, res) => {
  const { data: profile } = await supabase
    .from('profiles')
    .select('username')
    .eq('id', req.user.id)
    .single();

  const token = await createLiveKitToken({
    channelId: req.params.channelId,
    userId: req.user.id,
    username: profile?.username || 'usuário',
  });

  res.json({ token, livekitUrl: process.env.LIVEKIT_URL });
});
