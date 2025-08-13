'use client';

export const dynamic = 'force-dynamic';

import { useState, useEffect } from 'react';

type Author = {
  id: number;
  nombre: string;
  epoca?: string | null;
  fecha_nacimiento?: string | null;
  fecha_defuncion?: string | null;
  imagen_url?: string | null;
  biografia?: string | null;
  schools?: { id: number; nombre: string }[];
  books?: { id: number; titulo: string; imagen_url?: string | null; descripcion?: string | null }[];
};

async function fetchAuthor(id: string) {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000';
  const res = await fetch(`${base}/authors/${id}/`, { cache: 'no-store' });
  if (!res.ok) return null;
  return res.json();
}

export default function AuthorDetail({ params }: { params: { id: string } }) {
  const [author, setAuthor] = useState<Author | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAuthor() {
      setLoading(true);
      const data = await fetchAuthor(params.id);
      setAuthor(data);
      setLoading(false);
    }
    loadAuthor();
  }, [params.id]);
  
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Cargando información del autor...</p>
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
        <a href="/authors" className="btn btn-secondary">
          ← Volver
        </a>
        <h1 className="text-3xl font-bold text-gray-900">{author.nombre}</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Información principal */}
        <div className="lg:col-span-2 space-y-6">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Información Personal</h2>
            <div className="space-y-4">
              {(author.fecha_nacimiento || author.fecha_defuncion) && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="font-medium text-gray-700 mb-3">Fechas</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {author.fecha_nacimiento && (
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-600">Nacimiento:</span>
                        <span className="text-sm font-medium text-gray-900">
                          {new Date(author.fecha_nacimiento).toLocaleDateString('es-ES', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                          })}
                        </span>
                      </div>
                    )}
                    {author.fecha_defuncion && (
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-600">Defunción:</span>
                        <span className="text-sm font-medium text-gray-900">
                          {new Date(author.fecha_defuncion).toLocaleDateString('es-ES', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                          })}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              {author.epoca && (
                <div className="flex items-center gap-3">
                  <span className="font-medium text-gray-700">Época:</span>
                  <span className="inline-block bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm">
                    {author.epoca}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Biografía extendida */}
          {author.biografia && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Biografía</h2>
              <div className="prose prose-gray max-w-none">
                <p className="text-gray-700 leading-relaxed text-justify">
                  {author.biografia}
                </p>
              </div>
            </div>
          )}

          {/* Escuelas */}
          {author.schools && author.schools.length > 0 && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Escuelas Filosóficas</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {author.schools.map(school => (
                  <a
                    key={school.id}
                    href={`/schools/${school.id}`}
                    className="block p-3 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
                  >
                    <span className="font-medium text-gray-900">{school.nombre}</span>
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Libros */}
          {author.books && author.books.length > 0 && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Obras Principales</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {author.books.map((book: any) => (
                  <div key={book.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="text-center">
                      {book.imagen_url && (
                        <img
                          src={book.imagen_url}
                          alt={book.titulo}
                          className="w-16 h-20 rounded-md mx-auto mb-3 object-cover shadow-sm"
                          onError={(e) => {
                            // Fallback si la imagen no carga
                            (e.target as HTMLImageElement).src = `https://ui-avatars.com/api/?name=${encodeURIComponent(book.titulo.slice(0, 30))}&background=2563eb&color=fff&size=200&bold=true&format=png`;
                          }}
                        />
                      )}
                      <h3 className="font-medium text-gray-900 text-sm leading-tight">
                        {book.titulo}
                      </h3>
                      {book.descripcion && (
                        <p className="text-xs text-gray-600 mt-2 line-clamp-2">
                          {book.descripcion}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {author.imagen_url && (
            <div className="card text-center">
              <img
                src={author.imagen_url}
                alt={author.nombre}
                className="w-32 h-32 rounded-full mx-auto mb-4 object-cover shadow-lg"
              />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{author.nombre}</h3>
              {(author.fecha_nacimiento && author.fecha_defuncion) && (
                <p className="text-sm text-gray-600">
                  ({new Date(author.fecha_nacimiento).getFullYear()} - {new Date(author.fecha_defuncion).getFullYear()})
                </p>
              )}
            </div>
          )}

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Resumen</h3>
            <div className="space-y-3 text-sm">
              {author.epoca && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Época:</span>
                  <span className="font-medium text-gray-900">{author.epoca}</span>
                </div>
              )}
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Escuelas:</span>
                <span className="font-medium text-gray-900">{author.schools?.length || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Libros:</span>
                <span className="font-medium text-gray-900">{author.books?.length || 0}</span>
              </div>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Explorar</h3>
            <div className="space-y-3">
              <a href={`/authors/${author.id}/quotes`} className="btn btn-primary w-full text-center block">
                📜 Ver Citas
              </a>
              <a href={`/authors/${author.id}/books`} className="btn btn-secondary w-full text-center block">
                📚 Ver Libros
              </a>
              <a href="/authors" className="btn btn-outline w-full text-center block">
                👥 Otros Filósofos
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}


