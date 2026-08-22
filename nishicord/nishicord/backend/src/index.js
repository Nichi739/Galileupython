import express from 'express';
import cors from 'cors';
import { createServer } from 'http';
import { Server } from 'socket.io';
import 'dotenv/config';

import { roomsRouter } from './routes/rooms.js';
import { channelsRouter } from './routes/channels.js';
import { registerChatHandlers } from './sockets/chat.js';

const app = express();
const httpServer = createServer(app);

const io = new Server(httpServer, {
  cors: { origin: process.env.FRONTEND_URL, credentials: true },
});

app.use(cors({ origin: process.env.FRONTEND_URL }));
app.use(express.json());

app.get('/health', (req, res) => res.json({ ok: true }));

app.use('/rooms', roomsRouter);
app.use('/channels', channelsRouter);

registerChatHandlers(io);

const PORT = process.env.PORT || 4000;
httpServer.listen(PORT, () => {
  console.log(`Nishicord backend rodando na porta ${PORT}`);
});
