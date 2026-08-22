-- Nishicord — schema do banco (rodar no SQL editor do Supabase)

create extension if not exists "uuid-ossp";

-- Perfis de usuário (complementa o auth.users nativo do Supabase)
create table profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  username text unique not null,
  avatar_url text,
  status text default 'online', -- online | away | busy | offline
  created_at timestamptz default now()
);

-- Salas ("servidores")
create table rooms (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  invite_code text unique not null default substr(md5(random()::text), 1, 8),
  owner_id uuid references profiles(id) on delete cascade,
  created_at timestamptz default now()
);

-- Membros de cada sala + papel (permissões)
create table room_members (
  room_id uuid references rooms(id) on delete cascade,
  user_id uuid references profiles(id) on delete cascade,
  role text not null default 'member', -- owner | moderator | member
  joined_at timestamptz default now(),
  primary key (room_id, user_id)
);

-- Canais dentro de uma sala
create table channels (
  id uuid primary key default uuid_generate_v4(),
  room_id uuid references rooms(id) on delete cascade,
  name text not null,
  type text not null default 'text', -- text | voice
  created_at timestamptz default now()
);

-- Mensagens de texto
create table messages (
  id uuid primary key default uuid_generate_v4(),
  channel_id uuid references channels(id) on delete cascade,
  user_id uuid references profiles(id) on delete cascade,
  content text not null,
  created_at timestamptz default now()
);

-- Row Level Security básica
alter table profiles enable row level security;
alter table rooms enable row level security;
alter table room_members enable row level security;
alter table channels enable row level security;
alter table messages enable row level security;

create policy "profiles visíveis para todos autenticados" on profiles
  for select using (auth.role() = 'authenticated');

create policy "usuário edita o próprio perfil" on profiles
  for update using (auth.uid() = id);

create policy "membros veem salas onde participam" on rooms
  for select using (
    id in (select room_id from room_members where user_id = auth.uid())
  );

create policy "qualquer autenticado cria sala" on rooms
  for insert with check (auth.uid() = owner_id);

create policy "membros veem a lista de membros da própria sala" on room_members
  for select using (
    room_id in (select room_id from room_members where user_id = auth.uid())
  );

create policy "membros veem canais da própria sala" on channels
  for select using (
    room_id in (select room_id from room_members where user_id = auth.uid())
  );

create policy "membros veem mensagens dos canais da própria sala" on messages
  for select using (
    channel_id in (
      select c.id from channels c
      join room_members rm on rm.room_id = c.room_id
      where rm.user_id = auth.uid()
    )
  );

create policy "membros enviam mensagens" on messages
  for insert with check (auth.uid() = user_id);
