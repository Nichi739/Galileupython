import { AccessToken } from 'livekit-server-sdk';
import 'dotenv/config';

// Gera um token de acesso para o usuário entrar numa "sala" do LiveKit,
// que aqui equivale a um canal de voz/vídeo do Nishicord.
// O nome da sala do LiveKit = id do canal (channelId), assim cada canal
// de voz vira uma sala de chamada isolada.
export async function createLiveKitToken({ channelId, userId, username }) {
  const at = new AccessToken(
    process.env.LIVEKIT_API_KEY,
    process.env.LIVEKIT_API_SECRET,
    {
      identity: userId,
      name: username,
    }
  );

  at.addGrant({
    room: channelId,
    roomJoin: true,
    canPublish: true,       // permite mandar áudio/vídeo/tela
    canSubscribe: true,     // permite ouvir/ver os outros
    canPublishData: false,
  });

  return await at.toJwt();
}
