'use client';

import { useState, useEffect } from 'react';

type Quote = {
  id: string;
  texto: string;
  autor_id: string;
  autor_nombre?: string;
};

export default function Page() {
  const [quote, setQuote] = useState<Quote | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchRandomQuote() {
      try {
        const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const res = await fetch(`${base}/quotes/random`);
        if (res.ok) {
          const data = await res.json();
          setQuote(data);
        }
      } catch (error) {
        console.error('Error fetching quote:', error);
      } finally {
        setLoading(false);
      }
    }
    
    fetchRandomQuote();
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      {/* Content */}
      <div className="text-center max-w-4xl mx-auto">
        <h1 className="text-6xl font-bold text-gray-800 mb-8 drop-shadow-lg">
          🏴‍☠️ Pirate Philosopher
        </h1>
        
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Cargando cita...</p>
          </div>
        ) : quote ? (
          <div className="card max-w-3xl mx-auto">
            <blockquote className="border-l-4 border-amber-500 pl-6">
              <p className="text-2xl text-gray-800 italic mb-6 font-medium">"{quote.texto}"</p>
              <footer className="text-lg text-gray-700 font-semibold">
                — {quote.autor_nombre || 'Autor desconocido'}
              </footer>
            </blockquote>
          </div>
        ) : (
          <div className="card max-w-3xl mx-auto">
            <p className="text-lg text-gray-600">No se pudo cargar la cita. Intenta recargar la página.</p>
          </div>
        )}
      </div>
    </div>
  );
}


