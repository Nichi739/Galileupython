import { useEffect, useRef, useState } from 'react';
import { socket } from '../lib/socket';
import { apiGet } from '../lib/api';

export default function ChatBox({ channel, user }) {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState('');
  const [typingUser, setTypingUser] = useState('');
  const bottomRef = useRef(null);

  useEffect(() => {
    apiGet(`/channels/${channel.id}/messages`).then(setMessages).catch(console.error);

    socket.emit('join-channel', channel.id);

    function onNewMessage(msg) {
      setMessages((prev) => [...prev, msg]);
    }
    function onTyping(username) {
      setTypingUser(username);
      setTimeout(() => setTypingUser(''), 2000);
    }

    socket.on('new-message', onNewMessage);
    socket.on('user-typing', onTyping);

    return () => {
      socket.emit('leave-channel', channel.id);
      socket.off('new-message', onNewMessage);
      socket.off('user-typing', onTyping);
    };
  }, [channel.id]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  function handleSend(e) {
    e.preventDefault();
    if (!text.trim()) return;
    socket.emit('send-message', { channelId: channel.id, userId: user.id, content: text });
    setText('');
  }

  return (
    <div className="chat-box">
      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className="chat-message">
            <strong>{msg.profiles?.username || 'usuário'}</strong>
            <span className="muted"> {new Date(msg.created_at).toLocaleTimeString()}</span>
            <p>{msg.content}</p>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {typingUser && <p className="muted typing-indicator">{typingUser} está digitando...</p>}

      <form className="chat-input" onSubmit={handleSend}>
        <input
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            socket.emit('typing', { channelId: channel.id, username: user.username });
          }}
          placeholder={`Conversar em #${channel.name}`}
        />
        <button type="submit">Enviar</button>
      </form>
    </div>
  );
}
