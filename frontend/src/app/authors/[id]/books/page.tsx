'use client';

export const dynamic = 'force-dynamic';

import { useState, useEffect } from 'react';

type Book = {
  id: number;
  titulo: string;
  descripcion?: string | null;
  imagen_url?: string | null;
  autor_id: number;
};

type Author = {
  id: number;
  nombre: string;
  imagen_url?: string | null;
};

async function fetchAuthor(id: string) {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const res = await fetch(`${base}/authors/${id}`, { cache: 'no-store' });
  if (!res.ok) return null;
  return res.json();
}

async function fetchAuthorBooks(authorId: string) {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const res = await fetch(`${base}/authors/${authorId}/books`, { cache: 'no-store' });
  if (!res.ok) return [];
  return res.json();
}

export default function AuthorBooks({ params }: { params: { id: string } }) {
  const [author, setAuthor] = useState<Author | null>(null);
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const authorData = await fetchAuthor(params.id);
      const booksData = await fetchAuthorBooks(params.id);
      setAuthor(authorData);
      setBooks(booksData);
      setLoading(false);
    }
    loadData();
  }, [params.id]);
  
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Cargando libros del autor...</p>
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
            <h1 className="text-3xl font-bold text-gray-900">Libros de {author.nombre}</h1>
            <p className="text-gray-600">{books.length} libro{books.length !== 1 ? 's' : ''} encontrado{books.length !== 1 ? 's' : ''}</p>
          </div>
        </div>
      </div>

      {books.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-600 text-lg">Este autor no tiene libros registrados.</p>
          <a href={`/authors/${author.id}`} className="btn btn-primary mt-4 inline-block">
            Volver al Autor
          </a>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {books.map((book) => (
            <div key={book.id} className="card hover:shadow-md transition-shadow">
              <div className="text-center">
                {book.imagen_url && (
                  <img
                    src={book.imagen_url}
                    alt={book.titulo}
                    className="w-24 h-32 rounded-lg mx-auto mb-4 object-cover shadow-sm"
                    onError={(e) => {
                      // Fallback si la imagen no carga
                      (e.target as HTMLImageElement).src = `https://ui-avatars.com/api/?name=${encodeURIComponent(book.titulo.slice(0, 30))}&background=2563eb&color=fff&size=200&bold=true&format=png`;
                    }}
                  />
                )}
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {book.titulo}
                </h3>
                <div className="flex items-center justify-center gap-2 mb-3">
                  {author.imagen_url && (
                    <img
                      src={author.imagen_url}
                      alt={author.nombre}
                      className="w-6 h-6 rounded-full object-cover"
                    />
                  )}
                  <p className="text-sm text-gray-600 font-medium">
                    por {author.nombre}
                  </p>
                </div>
                {book.descripcion && (
                  <p className="text-gray-600 text-sm line-clamp-3 leading-relaxed">
                    {book.descripcion}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="flex justify-center gap-4 pt-8">
        <a href={`/authors/${author.id}`} className="btn btn-secondary">
          Ver Perfil Completo
        </a>
        <a href={`/authors/${author.id}/quotes`} className="btn btn-primary">
          Ver Citas del Autor
        </a>
      </div>
    </div>
  );
}
