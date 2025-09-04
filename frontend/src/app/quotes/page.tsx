'use client';

import { useState, useEffect } from 'react';

type Author = {
  id: number;
  nombre: string;
  imagen_url?: string | null;
};

type Quote = { 
  id: string; 
  texto: string; 
  autor_id: string;
  autor_nombre?: string;
};

export default function QuotesPage() {
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 12;

  useEffect(() => {
    fetchQuotes();
  }, [searchTerm, currentPage]);

  async function fetchQuotes() {
    setLoading(true);
    const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const url = new URL(`${base}/quotes/`);
    url.searchParams.set('limit', itemsPerPage.toString());
    url.searchParams.set('offset', ((currentPage - 1) * itemsPerPage).toString());
    if (searchTerm) url.searchParams.set('q', searchTerm);
    
    try {
      const res = await fetch(url.toString());
      if (res.ok) {
        const data = await res.json();
        setQuotes(data);
        setTotalPages(Math.ceil(40 / itemsPerPage)); // 40 citas del seed
      }
    } catch (error) {
      console.error('Error fetching quotes:', error);
    } finally {
      setLoading(false);
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
  };

  const filteredQuotes = quotes.filter(quote =>
    quote.texto.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-3xl font-bold text-gray-900">Citas Filosóficas</h1>
        <form onSubmit={handleSearch} className="flex gap-2 w-full sm:w-auto">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar por texto..."
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
          <p className="mt-4 text-gray-600">Cargando citas...</p>
        </div>
      ) : (
        <>
          <div className="space-y-6">
            {filteredQuotes.map((quote: Quote) => (
              <div key={quote.id} className="card hover:shadow-md transition-shadow">
                <blockquote className="border-l-4 border-primary-500 pl-6">
                  <p className="text-lg text-gray-800 italic mb-4">"{quote.texto}"</p>
                  <footer className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-sm text-gray-600">
                        — {quote.autor_nombre || 'Autor desconocido'}
                      </span>
                    </div>
                    <a 
                      href={`/authors/${quote.autor_id}`}
                      className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                    >
                      Ver perfil de {quote.autor_nombre || 'Autor'} →
                    </a>
                  </footer>
                </blockquote>
              </div>
            ))}
          </div>

          {filteredQuotes.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-600">No se encontraron citas que coincidan con tu búsqueda.</p>
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


