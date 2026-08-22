import { useEffect, useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { supabase } from './lib/supabaseClient';
import Login from './pages/Login.jsx';
import Rooms from './pages/Rooms.jsx';
import Room from './pages/Room.jsx';

export default function App() {
  const [session, setSession] = useState(undefined); // undefined = carregando

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setSession(data.session));

    const { data: listener } = supabase.auth.onAuthStateChange((_event, newSession) => {
      setSession(newSession);
    });

    return () => listener.subscription.unsubscribe();
  }, []);

  if (session === undefined) return <div className="center-screen">Carregando...</div>;

  return (
    <Routes>
      <Route path="/login" element={session ? <Navigate to="/" /> : <Login />} />
      <Route path="/" element={session ? <Rooms /> : <Navigate to="/login" />} />
      <Route path="/rooms/:roomId" element={session ? <Room /> : <Navigate to="/login" />} />
    </Routes>
  );
}
