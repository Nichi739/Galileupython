import { supabase } from '../supabaseClient.js';

// Cada canal de texto vira uma "room" do Socket.io (conceito diferente da
// room do LiveKit) — assim as mensagens só vão para quem está no canal certo.
export function registerChatHandlers(io) {
  io.on('connection', (socket) => {
    socket.on('join-channel', (channelId) => {
      socket.join(channelId);
    });

    socket.on('leave-channel', (channelId) => {
      socket.leave(channelId);
    });

    socket.on('send-message', async ({ channelId, userId, content }) => {
      if (!content?.trim()) return;

      const { data, error } = await supabase
        .from('messages')
        .insert({ channel_id: channelId, user_id: userId, content })
        .select('id, content, created_at, profiles(id, username, avatar_url)')
        .single();

      if (error) {
        socket.emit('error-message', 'Não foi possível enviar a mensagem');
        return;
      }

      io.to(channelId).emit('new-message', data);
    });

    socket.on('typing', ({ channelId, username }) => {
      socket.to(channelId).emit('user-typing', username);
    });
  });
}
