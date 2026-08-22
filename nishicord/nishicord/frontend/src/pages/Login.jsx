import { useState } from 'react';
import { supabase } from '../lib/supabaseClient';

export default function Login() {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isSignUp) {
        const { data, error: signUpError } = await supabase.auth.signUp({ email, password });
        if (signUpError) throw signUpError;

        // cria a linha de perfil (username) assim que o usuário existe
        if (data.user) {
          await supabase.from('profiles').insert({ id: data.user.id, username });
        }
      } else {
        const { error: signInError } = await supabase.auth.signInWithPassword({ email, password });
        if (signInError) throw signInError;
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="center-screen">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h1>Nishicord</h1>
        <p>{isSignUp ? 'Criar conta' : 'Entrar'}</p>

        {isSignUp && (
          <input
            placeholder="Nome de usuário"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        )}
        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={6}
        />

        {error && <p className="error-text">{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? 'Aguarde...' : isSignUp ? 'Criar conta' : 'Entrar'}
        </button>

        <button type="button" className="link-button" onClick={() => setIsSignUp(!isSignUp)}>
          {isSignUp ? 'Já tenho conta' : 'Criar uma conta nova'}
        </button>
      </form>
    </div>
  );
}
