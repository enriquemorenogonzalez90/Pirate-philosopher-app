'use client';

import { useState, useEffect } from 'react';

type School = { 
  id: number; 
  nombre: string;
  descripcion?: string | null;
  imagen_url?: string | null;
};

// Colores temáticos para cada escuela
const SCHOOL_COLORS: Record<string, string> = {
  "Platonismo": "bg-blue-500",
  "Aristotelismo": "bg-amber-800", 
  "Estoicismo": "bg-green-600",
  "Epicureísmo": "bg-pink-500",
  "Escolástica": "bg-purple-600",
  "Humanismo": "bg-orange-400",
  "Racionalismo": "bg-blue-600",
  "Empirismo": "bg-green-500",
  "Idealismo": "bg-purple-500",
  "Materialismo": "bg-yellow-600",
  "Utilitarismo": "bg-green-400",
  "Deontología": "bg-blue-400",
  "Existencialismo": "bg-gray-700",
  "Fenomenología": "bg-indigo-400",
  "Marxismo": "bg-red-600",
  "Feminismo": "bg-pink-400",
  "Pragmatismo": "bg-yellow-700",
  "Positivismo": "bg-indigo-700",
  "Estructuralismo": "bg-gray-500",
  "Post-estructuralismo": "bg-gray-800",
  "Hermenéutica": "bg-purple-700",
  "Analítica": "bg-blue-900",
  "Continental": "bg-green-700",
  "Budismo": "bg-orange-500",
  "Confucianismo": "bg-red-700",
  "Taoísmo": "bg-teal-600",
  "Hinduismo": "bg-orange-600",
  "Nihilismo": "bg-black",
  "Relativismo": "bg-gray-500",
  "Absolutismo": "bg-white border"
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


