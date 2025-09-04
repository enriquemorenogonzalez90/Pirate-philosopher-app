"""
Firestore service for database operations
"""
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from google.cloud import firestore
from google.cloud.exceptions import NotFound

from ..models.firestore_models import (
    AuthorModel, SchoolModel, BookModel, QuoteModel,
    AuthorResponse, SchoolResponse, BookResponse, QuoteResponse,
    COLLECTIONS
)


class FirestoreService:
    """Service for Firestore operations"""
    
    def __init__(self):
        # Initialize Firestore client
        # In production, credentials are automatically detected
        # For local development, set GOOGLE_APPLICATION_CREDENTIALS
        self.db = firestore.Client()
    
    # =====================
    # AUTHORS OPERATIONS
    # =====================
    
    async def create_author(self, author_data: AuthorModel) -> str:
        """Create a new author"""
        author_dict = author_data.dict()
        author_dict['created_at'] = datetime.now(timezone.utc)
        author_dict['updated_at'] = datetime.now(timezone.utc)
        
        doc_ref = self.db.collection(COLLECTIONS['authors']).document()
        doc_ref.set(author_dict)
        return doc_ref.id
    
    async def get_author(self, author_id: str) -> Optional[AuthorResponse]:
        """Get author by ID"""
        try:
            doc_ref = self.db.collection(COLLECTIONS['authors']).document(author_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return None
            
            data = doc.to_dict()
            data['id'] = doc.id
            
            # Count related documents
            data['books_count'] = await self._count_author_books(author_id)
            data['quotes_count'] = await self._count_author_quotes(author_id)
            
            return AuthorResponse(**data)
        except Exception as e:
            print(f"Error getting author {author_id}: {e}")
            return None
    
    async def get_authors(self, limit: int = 50, offset: int = 0) -> List[AuthorResponse]:
        """Get paginated list of authors"""
        query = (self.db.collection(COLLECTIONS['authors'])
                .order_by('nombre')
                .limit(limit)
                .offset(offset))
        
        docs = query.stream()
        authors = []
        
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            
            # For list view, we can skip counts to improve performance
            data['books_count'] = 0
            data['quotes_count'] = 0
            
            authors.append(AuthorResponse(**data))
        
        return authors
    
    async def search_authors(self, query: str, limit: int = 20) -> List[AuthorResponse]:
        """Search authors by name"""
        # Firestore doesn't have full-text search, so we'll do prefix matching
        # For production, consider using Algolia or Cloud Search
        authors_ref = self.db.collection(COLLECTIONS['authors'])
        
        # Search by name (prefix)
        query_ref = (authors_ref
                    .where('nombre', '>=', query)
                    .where('nombre', '<=', query + '\uf8ff')
                    .limit(limit))
        
        docs = query_ref.stream()
        authors = []
        
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            data['books_count'] = 0
            data['quotes_count'] = 0
            authors.append(AuthorResponse(**data))
        
        return authors
    
    # =====================
    # SCHOOLS OPERATIONS
    # =====================
    
    async def create_school(self, school_data: SchoolModel) -> str:
        """Create a new school"""
        school_dict = school_data.dict()
        school_dict['created_at'] = datetime.utcnow()
        school_dict['updated_at'] = datetime.utcnow()
        
        doc_ref = self.db.collection(COLLECTIONS['schools']).document()
        doc_ref.set(school_dict)
        return doc_ref.id
    
    async def get_school(self, school_id: str) -> Optional[SchoolResponse]:
        """Get school by ID"""
        try:
            doc_ref = self.db.collection(COLLECTIONS['schools']).document(school_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return None
            
            data = doc.to_dict()
            data['id'] = doc.id
            data['authors_count'] = len(data.get('author_ids', []))
            
            return SchoolResponse(**data)
        except Exception as e:
            print(f"Error getting school {school_id}: {e}")
            return None
    
    async def get_schools(self, limit: int = 50) -> List[SchoolResponse]:
        """Get list of schools"""
        query = (self.db.collection(COLLECTIONS['schools'])
                .order_by('nombre')
                .limit(limit))
        
        docs = query.stream()
        schools = []
        
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            data['authors_count'] = len(data.get('author_ids', []))
            schools.append(SchoolResponse(**data))
        
        return schools
    
    # =====================
    # BOOKS OPERATIONS
    # =====================
    
    async def create_book(self, book_data: BookModel) -> str:
        """Create a new book"""
        book_dict = book_data.dict()
        book_dict['created_at'] = datetime.utcnow()
        book_dict['updated_at'] = datetime.utcnow()
        
        doc_ref = self.db.collection(COLLECTIONS['books']).document()
        doc_ref.set(book_dict)
        return doc_ref.id
    
    async def get_books(self, limit: int = 50, offset: int = 0, autor_id: Optional[str] = None, search_query: Optional[str] = None) -> List[BookResponse]:
        """Get books with pagination, optional author filter and search"""
        query = self.db.collection(COLLECTIONS['books'])
        
        if autor_id:
            query = query.where('autor_id', '==', autor_id)
        
        # Note: Firestore doesn't support text search natively
        # For search_query, we'll fetch all matching books and filter in Python
        # This is not ideal for large datasets - consider using Algolia or similar for production
        
        query = query.order_by('titulo').offset(offset).limit(limit)
        docs = query.stream()
        
        books = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            
            # Apply text search filter if provided
            if search_query:
                titulo = data.get('titulo', '').lower()
                descripcion = data.get('descripcion', '') or ''
                descripcion = descripcion.lower()
                search_term = search_query.lower()
                
                if search_term not in titulo and search_term not in descripcion:
                    continue
            
            # Get author information for frontend compatibility
            if data.get('autor_id'):
                author_info = await self._get_author_info(data['autor_id'], data.get('autor_nombre'))
                if author_info:
                    data['author'] = {
                        'id': int(data['autor_id']) if data['autor_id'].isdigit() else data['autor_id'],
                        'nombre': author_info.get('nombre', data.get('autor_nombre', 'Autor desconocido')),
                        'imagen_url': author_info.get('imagen_url')
                    }
                else:
                    # Fallback if author not found
                    data['author'] = {
                        'id': int(data['autor_id']) if data['autor_id'].isdigit() else data['autor_id'],
                        'nombre': data.get('autor_nombre', 'Autor desconocido'),
                        'imagen_url': None
                    }
            
            books.append(BookResponse(**data))
        
        return books
    
    async def count_books(self, autor_id: Optional[str] = None, search_query: Optional[str] = None) -> int:
        """Count total books with optional filters"""
        query = self.db.collection(COLLECTIONS['books'])
        
        if autor_id:
            query = query.where('autor_id', '==', autor_id)
        
        docs = list(query.stream())
        
        if search_query:
            # Filter by search query
            filtered_count = 0
            search_term = search_query.lower()
            
            for doc in docs:
                data = doc.to_dict()
                titulo = data.get('titulo', '').lower()
                descripcion = data.get('descripcion', '') or ''
                descripcion = descripcion.lower()
                
                if search_term in titulo or search_term in descripcion:
                    filtered_count += 1
            
            return filtered_count
        
        return len(docs)
    
    # =====================
    # QUOTES OPERATIONS  
    # =====================
    
    async def create_quote(self, quote_data: QuoteModel) -> str:
        """Create a new quote"""
        quote_dict = quote_data.dict()
        quote_dict['created_at'] = datetime.utcnow()
        quote_dict['updated_at'] = datetime.utcnow()
        
        doc_ref = self.db.collection(COLLECTIONS['quotes']).document()
        doc_ref.set(quote_dict)
        return doc_ref.id
    
    async def get_quotes(self, limit: int = 50, autor_id: Optional[str] = None) -> List[QuoteResponse]:
        """Get quotes, optionally filtered by author"""
        query = self.db.collection(COLLECTIONS['quotes'])
        
        if autor_id:
            query = query.where('autor_id', '==', autor_id)
        
        query = query.order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
        docs = query.stream()
        
        quotes = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            quotes.append(QuoteResponse(**data))
        
        return quotes
    
    async def get_random_quote(self) -> Optional[QuoteResponse]:
        """Get a random quote"""
        # Firestore doesn't have native random sampling
        # This is a simple approach - for better performance, consider maintaining a separate collection
        quotes_ref = self.db.collection(COLLECTIONS['quotes'])
        docs = list(quotes_ref.limit(100).stream())
        
        if not docs:
            return None
        
        import random
        doc = random.choice(docs)
        data = doc.to_dict()
        data['id'] = doc.id
        
        return QuoteResponse(**data)
    
    # =====================
    # STATS OPERATIONS
    # =====================
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get application statistics"""
        stats = {}
        
        # Count documents in each collection
        for collection_name, collection_key in COLLECTIONS.items():
            try:
                # Note: This is not efficient for large collections
                # For production, consider maintaining counters in a separate document
                docs = list(self.db.collection(collection_key).limit(1000).stream())
                stats[f'{collection_name}_count'] = len(docs)
            except Exception as e:
                print(f"Error counting {collection_name}: {e}")
                stats[f'{collection_name}_count'] = 0
        
        return stats
    
    # =====================
    # HELPER METHODS
    # =====================
    
    async def _count_author_books(self, author_id: str) -> int:
        """Count books by author"""
        query = self.db.collection(COLLECTIONS['books']).where('autor_id', '==', author_id)
        docs = list(query.stream())
        return len(docs)
    
    async def _count_author_quotes(self, author_id: str) -> int:
        """Count quotes by author"""
        query = self.db.collection(COLLECTIONS['quotes']).where('autor_id', '==', author_id)
        docs = list(query.stream())
        return len(docs)
    
    async def _get_author_info(self, author_id: str, author_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get basic author information for book responses"""
        try:
            # First try by ID
            doc_ref = self.db.collection(COLLECTIONS['authors']).document(author_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                return {
                    'nombre': data.get('nombre'),
                    'imagen_url': data.get('imagen_url')
                }
            
            # Fallback: search by name if provided
            if author_name:
                query = self.db.collection(COLLECTIONS['authors']).where('nombre', '==', author_name).limit(1)
                docs = list(query.stream())
                
                if docs:
                    data = docs[0].to_dict()
                    return {
                        'nombre': data.get('nombre'),
                        'imagen_url': data.get('imagen_url')
                    }
            
            return None
        except Exception as e:
            print(f"Error getting author info for {author_id}/{author_name}: {e}")
            return None
    
    # =====================
    # BATCH OPERATIONS (for migration)
    # =====================
    
    async def batch_create_authors(self, authors: List[AuthorModel]) -> List[str]:
        """Batch create authors"""
        batch = self.db.batch()
        doc_ids = []
        
        for author_data in authors:
            doc_ref = self.db.collection(COLLECTIONS['authors']).document()
            author_dict = author_data.dict()
            author_dict['created_at'] = datetime.utcnow()
            author_dict['updated_at'] = datetime.utcnow()
            
            batch.set(doc_ref, author_dict)
            doc_ids.append(doc_ref.id)
        
        batch.commit()
        return doc_ids