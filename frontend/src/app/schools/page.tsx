'use client';

import { useState, useEffect } from 'react';

type School = { 
  id: number; 
  nombre: string;
  descripcion?: string | null;
  imagen_url?: string | null;
};

export default function SchoolsPage() {
  const [schools, setSchools] = useState<School[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 12;

  useEffect(() => {
    fetchSchools();
  }, [searchTerm, currentPage]);

  async function fetchSchools() {
    setLoading(true);
    const base = process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000';
    const url = new URL(`${base}/schools/`);
    url.searchParams.set('limit', itemsPerPage.toString());
    url.searchParams.set('offset', ((currentPage - 1) * itemsPerPage).toString());
    if (searchTerm) url.searchParams.set('q', searchTerm);
    
    try {
      const res = await fetch(url.toString());
      if (res.ok) {
        const data = await res.json();
        setSchools(data);
        setTotalPages(Math.ceil(40 / itemsPerPage)); // 40 escuelas del seed
      }
    } catch (error) {
      console.error('Error fetching schools:', error);
    } finally {
      setLoading(false);
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
  };

  const filteredSchools = schools.filter(school =>
    school.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (school.descripcion && school.descripcion.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-3xl font-bold text-gray-900">Escuelas Filosóficas</h1>
        <form onSubmit={handleSearch} className="flex gap-2 w-full sm:w-auto">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar por nombre o descripción..."
            className="input flex-1 sm:w-64"
          />
          <button type="submit" className="btn btn-primary whitespace-nowrap">
            Buscar
          </button>
        </form>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando escuelas...</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSchools.map((school: School) => (
              <div key={school.id} className="card hover:shadow-md transition-shadow">
                <div className="text-center">
                  {school.imagen_url && (
                    <img
                      src={school.imagen_url}
                      alt={school.nombre}
                      className="w-20 h-20 rounded-lg mx-auto mb-4 object-cover"
                    />
                  )}
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    <a href={`/schools/${school.id}`} className="hover:text-primary-600">
                      {school.nombre}
                    </a>
                  </h3>
                  {school.descripcion && (
                    <p className="text-gray-600 text-sm line-clamp-2">
                      {school.descripcion}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>

          {filteredSchools.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-600">No se encontraron escuelas que coincidan con tu búsqueda.</p>
            </div>
          )}

          {/* Paginación */}
          {totalPages > 1 && (
            <div className="flex justify-center items-center gap-2 mt-8">
              <button
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
                className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Anterior
              </button>
              
              <span className="px-4 py-2 text-gray-600">
                Página {currentPage} de {totalPages}
              </span>
              
              <button
                onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                disabled={currentPage === totalPages}
                className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Siguiente
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}


