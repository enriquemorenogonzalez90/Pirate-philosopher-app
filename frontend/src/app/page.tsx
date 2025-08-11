export const dynamic = 'force-dynamic';

type Quote = {
  id: number;
  texto: string;
  autor_id: number;
  autor_nombre?: string;
};

async function fetchRandomQuote() {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const res = await fetch(`${base}/random-quotes?limit=1`, { cache: 'no-store' });
  if (!res.ok) return null;
  const quotes = await res.json();
  return quotes.length > 0 ? quotes[0] : null;
}

async function fetchAuthorName(authorId: number) {
  const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const res = await fetch(`${base}/authors/${authorId}`, { cache: 'no-store' });
  if (!res.ok) return null;
  const author = await res.json();
  return author.nombre;
}

export default async function Page() {
  const quote = await fetchRandomQuote();
  let authorName = null;
  
  if (quote) {
    authorName = await fetchAuthorName(quote.autor_id);
  }

  return (
    <div className="min-h-screen relative flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: 'url(/images/philosophers-pirates.jpg)',
          filter: 'blur(1px) brightness(0.3)'
        }}
      />
      
      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black bg-opacity-50" />
      
      {/* Content */}
      <div className="relative z-10 text-center max-w-4xl mx-auto px-4">
        <h1 className="text-6xl font-bold text-white mb-8 drop-shadow-2xl">
          Pirate Philosopher
        </h1>
        
        {quote && (
          <div className="backdrop-blur-sm bg-white/90 rounded-lg shadow-2xl p-8 max-w-3xl mx-auto border border-white/20">
            <blockquote className="border-l-4 border-amber-500 pl-6">
              <p className="text-2xl text-gray-800 italic mb-6 font-medium">"{quote.texto}"</p>
              <footer className="text-lg text-gray-700 font-semibold">
                — {authorName || `Autor #${quote.autor_id}`}
              </footer>
            </blockquote>
            <div className="mt-8 text-center">
              <p className="text-sm text-gray-600">
                La cita cambia cada vez que recargas la página
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}


