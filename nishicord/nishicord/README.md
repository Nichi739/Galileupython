# Nishicord

MVP de um app de comunicação estilo Discord: salas, canais de texto, chamadas de voz/vídeo e transmissão de tela.

## Stack
- **Frontend:** React + Vite
- **Backend:** Node.js + Express + Socket.io
- **Voz/vídeo/tela:** LiveKit
- **Autenticação e banco:** Supabase (Postgres)

## 1. Configurar o Supabase
1. Crie um projeto em https://supabase.com
2. Vá em **SQL Editor** e rode o conteúdo de `database/schema.sql`
3. Em **Project Settings → API**, copie:
   - `Project URL` → vira `SUPABASE_URL` / `VITE_SUPABASE_URL`
   - `anon public key` → vira `VITE_SUPABASE_ANON_KEY`
   - `service_role key` → vira `SUPABASE_SERVICE_ROLE_KEY` (⚠️ só no backend, nunca no frontend)

## 2. Configurar o LiveKit
1. Crie uma conta gratuita em https://cloud.livekit.io
2. Crie um projeto e copie: `URL do servidor`, `API Key`, `API Secret`

## 3. Rodar localmente

### Backend
```bash
cd backend
cp .env.example .env   # preencha com suas chaves do Supabase e LiveKit
npm install
npm run dev
```

### Frontend
```bash
cd frontend
cp .env.example .env   # preencha com suas chaves do Supabase e a URL do backend
npm install
npm run dev
```

Abra http://localhost:5173 — crie uma conta, crie uma sala e teste o chat, a chamada de voz/vídeo e o compartilhamento de tela.

## 4. Deploy (colocar no ar)

1. Suba o projeto para um repositório no GitHub
2. **Backend → Railway ou Render**: aponte para a pasta `backend`, configure as mesmas variáveis do `.env` nas configurações do serviço
3. **Frontend → Vercel**: aponte para a pasta `frontend`, configure as variáveis `VITE_...` apontando para a URL pública do backend já hospedado
4. No Supabase, em **Authentication → URL Configuration**, adicione a URL da Vercel como origem permitida

## Estrutura do projeto
```
nishicord/
├── backend/     # API + Socket.io + geração de token do LiveKit
├── frontend/    # App React
└── database/    # schema.sql para rodar no Supabase
```

## Próximos passos sugeridos (fora do MVP)
- Emojis, reactions, threads de mensagem
- Upload de avatar
- Gravação de chamadas
- Apps mobile nativos com Capacitor
