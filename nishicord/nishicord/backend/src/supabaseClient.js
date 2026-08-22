import { createClient } from '@supabase/supabase-js';
import 'dotenv/config';

// No backend usamos a service_role key: ela ignora RLS, então toda
// verificação de permissão (dono/moderador/membro) é feita manualmente
// nas rotas antes de qualquer escrita.
export const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Middleware simples: valida o token do usuário (enviado pelo frontend)
// e anexa o usuário autenticado em req.user
export async function requireAuth(req, res, next) {
  const authHeader = req.headers.authorization || '';
  const token = authHeader.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'Token não enviado' });
  }

  const { data, error } = await supabase.auth.getUser(token);

  if (error || !data.user) {
    return res.status(401).json({ error: 'Token inválido' });
  }

  req.user = data.user;
  next();
}
