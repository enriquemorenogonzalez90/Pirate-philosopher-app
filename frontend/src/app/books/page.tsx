'use client';

import { useState, useEffect } from 'react';

type Author = {
  id: number;
  nombre: string;
  imagen_url?: string | null;
};

type Book = { 
  id: number; 
  titulo: string; 
  autor_id: number;
  author: Author;
  descripcion?: string | null;
  imagen_url?: string | null;
};

export default function BooksPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 12;

  useEffect(() => {
    fetchBooks();
  }, [searchTerm, currentPage]);

  async function fetchBooks() {
    setLoading(true);
    const base = process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000';
    const url = new URL(`${base}/books/`);
    url.searchParams.set('limit', itemsPerPage.toString());
    url.searchParams.set('offset', ((currentPage - 1) * itemsPerPage).toString());
    if (searchTerm) url.searchParams.set('q', searchTerm);
    
    try {
      const res = await fetch(url.toString());
      if (res.ok) {
        const data = await res.json();
        setBooks(data);
        setTotalPages(Math.ceil(40 / itemsPerPage)); // 40 libros del seed
      }
    } catch (error) {
      console.error('Error fetching books:', error);
    } finally {
      setLoading(false);
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
  };

  const filteredBooks = books.filter(book =>
    book.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (book.descripcion && book.descripcion.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-3xl font-bold text-gray-900">Libros Filosóficos</h1>
        <form onSubmit={handleSearch} className="flex gap-2 w-full sm:w-auto">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar por título o descripción..."
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
          <p className="mt-4 text-gray-600">Cargando libros...</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredBooks.map((book: Book) => (
              <div key={book.id} className="card hover:shadow-md transition-shadow">
                <div className="text-center">
                  {book.imagen_url && (
                    <img
                      src={book.imagen_url}
                      alt={book.titulo}
                      className="w-20 h-20 rounded-lg mx-auto mb-4 object-cover"
                    />
                  )}
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {book.titulo}
                  </h3>
                  <div className="flex items-center justify-center gap-2 mb-3">
                    {book.author.imagen_url && (
                      <img
                        src={book.author.imagen_url}
                        alt={book.author.nombre}
                        className="w-6 h-6 rounded-full object-cover"
                      />
                    )}
                    <p className="text-sm text-gray-600">
                      por {book.author.nombre}
                    </p>
                  </div>
                  {book.descripcion && (
                    <p className="text-gray-600 text-sm line-clamp-3">
                      {book.descripcion}
                    </p>
                  )}
                  <div className="mt-4">
                    <a 
                      href={`/authors/${book.autor_id}`}
                      className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                    >
                      Ver perfil de {book.author.nombre} →
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredBooks.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-600">No se encontraron libros que coincidan con tu búsqueda.</p>
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


