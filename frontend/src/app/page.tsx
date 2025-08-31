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
    <div className="min-h-screen flex items-center justify-center px-4">
      {/* Content */}
      <div className="text-center max-w-4xl mx-auto">
        <h1 className="text-6xl font-bold text-gray-800 mb-8 drop-shadow-lg">
          🏴‍☠️ Pirate Philosopher
        </h1>
        
        {quote && (
          <div className="card max-w-3xl mx-auto">
            <blockquote className="border-l-4 border-amber-500 pl-6">
              <p className="text-2xl text-gray-800 italic mb-6 font-medium">"{quote.texto}"</p>
              <footer className="text-lg text-gray-700 font-semibold">
                — {authorName || `Autor #${quote.autor_id}`}
              </footer>
            </blockquote>
          </div>
        )}
      </div>
    </div>
  );
}


