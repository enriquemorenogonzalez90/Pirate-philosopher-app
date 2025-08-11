'use client';

import { useState, useEffect } from 'react';

type Author = {
  id: number;
  nombre: string;
  epoca?: string | null;
  imagen_url?: string | null;
};

export default function AuthorsPage() {
  const [authors, setAuthors] = useState<Author[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 12;

  useEffect(() => {
    fetchAuthors();
  }, [searchTerm, currentPage]);

  async function fetchAuthors() {
    setLoading(true);
    const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const url = new URL(`${base}/authors/`);
    url.searchParams.set('limit', itemsPerPage.toString());
    url.searchParams.set('offset', ((currentPage - 1) * itemsPerPage).toString());
    if (searchTerm) url.searchParams.set('q', searchTerm);
    
    try {
      const res = await fetch(url.toString());
      if (res.ok) {
        const data = await res.json();
        setAuthors(data);
        // Simular total de páginas (en un caso real vendría del backend)
        setTotalPages(Math.ceil(40 / itemsPerPage)); // 40 autores del seed
      }
    } catch (error) {
      console.error('Error fetching authors:', error);
    } finally {
      setLoading(false);
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
  };

  const filteredAuthors = authors.filter(author =>
    author.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (author.epoca && author.epoca.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-3xl font-bold text-gray-900">Autores Filosóficos</h1>
        <form onSubmit={handleSearch} className="flex gap-2 w-full sm:w-auto">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar por nombre o época..."
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
          <p className="mt-4 text-gray-600">Cargando autores...</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredAuthors.map((author: Author) => (
              <div key={author.id} className="card hover:shadow-md transition-shadow">
                <div className="text-center">
                  {author.imagen_url && (
                    <img
                      src={author.imagen_url}
                      alt={author.nombre}
                      className="w-20 h-20 rounded-full mx-auto mb-4 object-cover"
                    />
                  )}
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    <a href={`/authors/${author.id}`} className="hover:text-primary-600">
                      {author.nombre}
                    </a>
                  </h3>
                  {author.epoca && (
                    <span className="inline-block bg-primary-100 text-primary-800 text-sm px-3 py-1 rounded-full">
                      {author.epoca}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {filteredAuthors.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-600">No se encontraron autores que coincidan con tu búsqueda.</p>
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


