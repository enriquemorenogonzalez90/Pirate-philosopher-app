'use client';

export const dynamic = 'force-dynamic';

import { useState, useEffect } from 'react';

type Quote = {
  id: number;
  texto: string;
  autor_id: number;
};

type Author = {
  id: number;
  nombre: string;
  imagen_url?: string | null;
};

async function fetchAuthor(id: string) {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000';
  const res = await fetch(`${base}/authors/${id}`, { cache: 'no-store' });
  if (!res.ok) return null;
  return res.json();
}

async function fetchAuthorQuotes(authorId: string) {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000';
  const res = await fetch(`${base}/authors/${authorId}/quotes`, { cache: 'no-store' });
  if (!res.ok) return [];
  return res.json();
}

export default function AuthorQuotes({ params }: { params: { id: string } }) {
  const [author, setAuthor] = useState<Author | null>(null);
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const authorData = await fetchAuthor(params.id);
      const quotesData = await fetchAuthorQuotes(params.id);
      setAuthor(authorData);
      setQuotes(quotesData);
      setLoading(false);
    }
    loadData();
  }, [params.id]);
  
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Cargando citas del autor...</p>
      </div>
    );
  }
  
  if (!author) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Autor no encontrado</h1>
        <p className="text-gray-600">El autor que buscas no existe.</p>
        <a href="/authors" className="btn btn-primary mt-4 inline-block">
          Volver a Autores
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-6">
        <a href={`/authors/${author.id}`} className="btn btn-secondary">
          ← Volver al Autor
        </a>
        <div className="flex items-center gap-4">
          {author.imagen_url && (
            <img
              src={author.imagen_url}
              alt={author.nombre}
              className="w-12 h-12 rounded-full object-cover"
            />
          )}
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Citas de {author.nombre}</h1>
            <p className="text-gray-600">{quotes.length} cita{quotes.length !== 1 ? 's' : ''} encontrada{quotes.length !== 1 ? 's' : ''}</p>
          </div>
        </div>
      </div>

      {quotes.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600 text-lg">Este autor no tiene citas registradas.</p>
          <a href={`/authors/${author.id}`} className="btn btn-primary mt-4 inline-block">
            Volver al Autor
          </a>
        </div>
      ) : (
        <div className="space-y-6">
          {quotes.map((quote) => (
            <div key={quote.id} className="card hover:shadow-md transition-shadow">
              <blockquote className="border-l-4 border-primary-500 pl-6">
                <p className="text-xl text-gray-800 italic mb-4 leading-relaxed">"{quote.texto}"</p>
                <footer className="flex items-center gap-3 text-gray-600">
                  {author.imagen_url && (
                    <img
                      src={author.imagen_url}
                      alt={author.nombre}
                      className="w-8 h-8 rounded-full object-cover"
                    />
                  )}
                  <span className="font-medium">— {author.nombre}</span>
                </footer>
              </blockquote>
            </div>
          ))}
        </div>
      )}

      <div className="flex justify-center gap-4 pt-8">
        <a href={`/authors/${author.id}`} className="btn btn-secondary">
          Ver Perfil Completo
        </a>
        <a href={`/authors/${author.id}/books`} className="btn btn-primary">
          Ver Libros del Autor
        </a>
      </div>
    </div>
  );
}
