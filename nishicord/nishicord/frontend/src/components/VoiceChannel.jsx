import { useEffect, useRef, useState } from 'react';
import {
  Room,
  RoomEvent,
  Track,
  createLocalScreenTracks,
} from 'livekit-client';
import { apiPost } from '../lib/api';

// Anexa um track de vídeo/áudio a um elemento <video>/<audio> na tela
function attachTrack(track, container) {
  const el = track.attach();
  container.appendChild(el);
  return el;
}

export default function VoiceChannel({ channel, user }) {
  const [room, setRoom] = useState(null);
  const [connected, setConnected] = useState(false);
  const [participants, setParticipants] = useState([]);
  const [micOn, setMicOn] = useState(false);
  const [camOn, setCamOn] = useState(false);
  const [sharingScreen, setSharingScreen] = useState(false);
  const videoGridRef = useRef(null);

  useEffect(() => {
    // ao trocar de canal, desconecta da chamada anterior
    return () => {
      room?.disconnect();
      setConnected(false);
    };
  }, [channel.id]);

  async function handleJoinCall() {
    const { token, livekitUrl } = await apiPost(`/channels/${channel.id}/voice-token`, {});

    const newRoom = new Room();
    await newRoom.connect(livekitUrl, token);

    newRoom.on(RoomEvent.TrackSubscribed, (track, _pub, participant) => {
      if (track.kind === Track.Kind.Video || track.kind === Track.Kind.Audio) {
        attachTrack(track, videoGridRef.current);
      }
    });

    newRoom.on(RoomEvent.TrackUnsubscribed, (track) => {
      track.detach().forEach((el) => el.remove());
    });

    newRoom.on(RoomEvent.ActiveSpeakersChanged, (speakers) => {
      setParticipants(
        Array.from(newRoom.remoteParticipants.values()).map((p) => ({
          identity: p.identity,
          name: p.name,
          speaking: speakers.some((s) => s.identity === p.identity),
        }))
      );
    });

    setRoom(newRoom);
    setConnected(true);
  }

  async function handleLeaveCall() {
    await room?.disconnect();
    setRoom(null);
    setConnected(false);
    setMicOn(false);
    setCamOn(false);
    setSharingScreen(false);
    if (videoGridRef.current) videoGridRef.current.innerHTML = '';
  }

  async function toggleMic() {
    if (!room) return;
    await room.localParticipant.setMicrophoneEnabled(!micOn);
    setMicOn(!micOn);
  }

  async function toggleCam() {
    if (!room) return;
    await room.localParticipant.setCameraEnabled(!camOn);
    setCamOn(!camOn);
  }

  async function toggleScreenShare() {
    if (!room) return;

    if (!sharingScreen) {
      // getDisplayMedia é acionado aqui dentro do createLocalScreenTracks
      const tracks = await createLocalScreenTracks({ audio: true });
      for (const track of tracks) {
        await room.localParticipant.publishTrack(track);
      }
      setSharingScreen(true);
    } else {
      room.localParticipant.videoTrackPublications.forEach((pub) => {
        if (pub.source === Track.Source.ScreenShare) {
          room.localParticipant.unpublishTrack(pub.track);
        }
      });
      setSharingScreen(false);
    }
  }

  return (
    <div className="voice-channel">
      {!connected ? (
        <button onClick={handleJoinCall}>🔊 Entrar no canal de voz #{channel.name}</button>
      ) : (
        <>
          <div className="call-controls">
            <button onClick={toggleMic}>{micOn ? '🎤 Mutar' : '🔇 Ativar microfone'}</button>
            <button onClick={toggleCam}>{camOn ? '📷 Desligar câmera' : '📷 Ligar câmera'}</button>
            <button onClick={toggleScreenShare}>
              {sharingScreen ? '🛑 Parar de compartilhar tela' : '🖥️ Compartilhar tela'}
            </button>
            <button onClick={handleLeaveCall} className="danger">Sair da chamada</button>
          </div>

          <ul className="participant-list">
            {participants.map((p) => (
              <li key={p.identity} className={p.speaking ? 'speaking' : ''}>
                {p.name} {p.speaking ? '🔊' : ''}
              </li>
            ))}
          </ul>

          <div ref={videoGridRef} className="video-grid" />
        </>
      )}
    </div>
  );
}
