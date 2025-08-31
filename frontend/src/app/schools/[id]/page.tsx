'use client';

export const dynamic = 'force-dynamic';

import { useState, useEffect } from 'react';

type Author = {
  id: number;
  nombre: string;
  epoca?: string | null;
  imagen_url?: string | null;
};

type School = {
  id: number;
  nombre: string;
  descripcion?: string | null;
  imagen_url?: string | null;
  authors?: Author[];
};

async function fetchSchool(id: string) {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const res = await fetch(`${base}/schools/${id}`, { cache: 'no-store' });
  if (!res.ok) return null;
  return res.json();
}

export default function SchoolDetail({ params }: { params: { id: string } }) {
  const [school, setSchool] = useState<School | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadSchool() {
      setLoading(true);
      const data = await fetchSchool(params.id);
      setSchool(data);
      setLoading(false);
    }
    loadSchool();
  }, [params.id]);
  
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Cargando información de la escuela...</p>
      </div>
    );
  }
  
  if (!school) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Escuela no encontrada</h1>
        <p className="text-gray-600">La escuela que buscas no existe.</p>
        <a href="/schools" className="btn btn-primary mt-4 inline-block">
          Volver a Escuelas
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-6">
        <a href="/schools" className="btn btn-secondary">
          ← Volver
        </a>
        <h1 className="text-3xl font-bold text-gray-900">{school.nombre}</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Información principal */}
        <div className="lg:col-span-2 space-y-6">
          {/* Descripción */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Descripción</h2>
            {school.descripcion ? (
              <p className="text-gray-700 leading-relaxed text-justify">
                {school.descripcion}
              </p>
            ) : (
              <p className="text-gray-500 italic">No hay descripción disponible.</p>
            )}
          </div>

          {/* Filósofos representativos */}
          {school.authors && school.authors.length > 0 && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Filósofos Representativos
                <span className="text-sm text-gray-500 font-normal ml-2">
                  ({school.authors.length} filósofo{school.authors.length !== 1 ? 's' : ''})
                </span>
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {school.authors.map(author => (
                  <a
                    key={author.id}
                    href={`/authors/${author.id}`}
                    className="block p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors group"
                  >
                    <div className="flex items-center gap-3">
                      {author.imagen_url && (
                        <img
                          src={author.imagen_url}
                          alt={author.nombre}
                          className="w-12 h-12 rounded-full object-cover"
                        />
                      )}
                      <div>
                        <h3 className="font-medium text-gray-900 group-hover:text-primary-700">
                          {author.nombre}
                        </h3>
                        {author.epoca && (
                          <span className="text-sm text-gray-500">
                            {author.epoca}
                          </span>
                        )}
                      </div>
                    </div>
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {school.imagen_url && (
            <div className="card text-center">
              <img
                src={school.imagen_url}
                alt={school.nombre}
                className="w-full h-48 rounded-lg mx-auto mb-4 object-cover"
              />
              <h3 className="text-lg font-semibold text-gray-900">{school.nombre}</h3>
            </div>
          )}

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Información</h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-center gap-2">
                <span className="font-medium text-gray-700">Filósofos:</span>
                <span className="text-gray-600">
                  {school.authors?.length || 0}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="font-medium text-gray-700">Tipo:</span>
                <span className="text-gray-600">Escuela Filosófica</span>
              </div>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Explorar</h3>
            <div className="space-y-3">
              <a href="/schools" className="btn btn-secondary w-full text-center block">
                🏛️ Ver Todas las Escuelas
              </a>
              <a href="/authors" className="btn btn-primary w-full text-center block">
                👥 Explorar Filósofos
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}


