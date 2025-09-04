"""
Migration script to transfer data from JSON files to Firestore
"""
import os
import json
import asyncio
import requests
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup
import time

# Firestore imports  
from services.firestore_service import FirestoreService
from models.firestore_models import AuthorModel, SchoolModel, BookModel, QuoteModel


class JSONToFirestoreMigrator:
    """Migrates data from JSON files to Firestore"""
    
    def __init__(self):
        # Firestore setup
        self.firestore_service = FirestoreService()
        
        # Data paths
        self.data_dir = Path(__file__).parent / "data" / "json"
        self.philosophers_file = self.data_dir / "philosophers_complete_data.json"
        
        # Mapping for relationships
        self.author_id_mapping = {}
        self.school_id_mapping = {}
    
    async def migrate_all(self):
        """Run complete migration"""
        print("🚀 Starting JSON to Firestore migration...")
        
        # Load JSON data
        await self.load_json_data()
        
        # Migrate in order (due to relationships)
        await self.migrate_schools()
        await self.migrate_authors() 
        await self.migrate_books()
        await self.migrate_quotes()
        
        print("✅ Migration completed successfully!")
        
        # Show stats
        await self.show_stats()
    
    async def load_json_data(self):
        """Load JSON data from file"""
        print("📂 Loading JSON data...")
        
        if not self.philosophers_file.exists():
            raise FileNotFoundError(f"JSON file not found: {self.philosophers_file}")
        
        with open(self.philosophers_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        philosophers = self.data.get('philosophers', [])
        print(f"📊 Loaded {len(philosophers)} philosophers from JSON")
    
    async def migrate_schools(self):
        """Extract and migrate philosophical schools"""
        print("\n📚 Migrating schools...")
        
        # Extract unique schools from philosophers
        schools_set = set()
        for philosopher in self.data.get('philosophers', []):
            school = philosopher.get('school', '').strip()
            if school and school not in ['', 'N/A', 'Unknown']:
                schools_set.add(school)
        
        schools_list = sorted(list(schools_set))
        print(f"📚 Found {len(schools_list)} unique schools")
        
        for school_name in schools_list:
            # Create Firestore school
            firestore_school = SchoolModel(
                nombre=school_name,
                descripcion=f"Escuela filosófica: {school_name}",
                author_ids=[],  # Will be populated when migrating authors
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            firestore_id = await self.firestore_service.create_school(firestore_school)
            self.school_id_mapping[school_name] = firestore_id
            
            print(f"  ✓ Migrated school: {school_name}")
        
        print(f"📚 Migrated {len(self.school_id_mapping)} schools")
    
    async def extract_biography_from_iep(self, iep_link):
        """Extrae biografía desde el enlace de IEP hasta Table of Contents"""
        if not iep_link or not iep_link.strip():
            return None
        
        try:
            print(f"    📖 Extrayendo biografía de: {iep_link}")
            
            # Pausa para ser respetuoso con el servidor
            time.sleep(1)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; PhilosophyBot/1.0; Educational purpose)'
            }
            
            response = requests.get(iep_link, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar el área de contenido principal
            content_div = soup.find('div', class_='entry-content') or soup.find('div', id='content')
            if not content_div:
                # Alternativa - buscar el primer div con muchos párrafos
                content_div = soup.find('div', lambda x: x and len(x.find_all('p')) > 3)
            
            if not content_div:
                return None
            
            # Extraer párrafos hasta "Table of Contents" o títulos similares
            biography_paragraphs = []
            stop_keywords = [
                'table of contents', 'contents', 'outline', 'references',
                'bibliography', 'further reading', 'see also'
            ]
            
            for element in content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4']):
                if element.name.startswith('h'):
                    # Verificar si este título indica el final de la biografía
                    heading_text = element.get_text().lower().strip()
                    if any(keyword in heading_text for keyword in stop_keywords):
                        break
                elif element.name == 'p':
                    # Añadir texto del párrafo
                    paragraph_text = element.get_text().strip()
                    if paragraph_text and len(paragraph_text) > 50:  # Filtrar párrafos muy cortos
                        biography_paragraphs.append(paragraph_text)
                
                # Parar si tenemos suficiente contenido (3-5 párrafos sustanciales)
                if len(biography_paragraphs) >= 5:
                    break
            
            if biography_paragraphs:
                biography = '\n\n'.join(biography_paragraphs)
                print(f"    ✓ Extraídos {len(biography_paragraphs)} párrafos ({len(biography)} caracteres)")
                return biography
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"    ❌ Error HTTP extrayendo de {iep_link}: {e}")
            return None
        except Exception as e:
            print(f"    ❌ Error extrayendo de {iep_link}: {e}")
            return None

    async def migrate_authors(self):
        """Migrate philosophers as authors"""
        print("\n👨‍🎓 Migrating authors...")
        
        philosophers = self.data.get('philosophers', [])
        
        for philosopher in philosophers:
            # Map school relationship
            school_ids = []
            school_name = philosopher.get('school', '').strip()
            if school_name and school_name in self.school_id_mapping:
                school_ids.append(self.school_id_mapping[school_name])
            
            # Extract biography from IEP link if available
            biography = None
            iep_link = philosopher.get('iep_link', '').strip()
            if iep_link:
                biography = await self.extract_biography_from_iep(iep_link)
            
            # Fallback to existing biography from JSON
            if not biography:
                biography = philosopher.get('biography', '')
            
            # Create Firestore author
            firestore_author = AuthorModel(
                external_id=philosopher.get('id'),
                nombre=philosopher.get('name', ''),
                username=philosopher.get('username', ''),
                vida=philosopher.get('life', ''),
                descripcion_topica=philosopher.get('topical_description', ''),
                areas_interes=philosopher.get('interests', ''),
                
                # Dates from JSON
                fecha_nacimiento_completa=philosopher.get('birth_date', ''),
                fecha_muerte_completa=philosopher.get('death_date', ''),
                año_nacimiento=philosopher.get('birth_year', ''),
                año_muerte=philosopher.get('death_year', ''),
                
                # Location
                lugar_nacimiento=philosopher.get('birth_place', ''),
                
                # School
                escuela_principal=school_name,
                school_ids=school_ids,
                
                # Links
                enlace_iep=philosopher.get('iep_link', ''),
                enlace_stanford=philosopher.get('spe_link', ''),
                titulo_wiki=philosopher.get('wiki_title', ''),
                
                # Images (keep JSON structure)
                imagenes=philosopher.get('images', {}),
                imagen_url=self.get_main_image_url(philosopher.get('images', {})),
                
                # Books info
                tiene_libros=philosopher.get('has_ebooks', False),
                libros_librivox={
                    'librivox_ids': philosopher.get('librivox_ids', []),
                    'has_ebooks': philosopher.get('has_ebooks', False)
                },
                
                # Biography (extracted from IEP or from JSON)
                biografia=biography or '',
                
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            firestore_id = await self.firestore_service.create_author(firestore_author)
            self.author_id_mapping[philosopher.get('id')] = firestore_id
            
            print(f"  ✓ Migrated author: {philosopher.get('name', 'Unknown')}")
        
        # Update schools with author references
        await self.update_schools_with_authors()
        
        print(f"👨‍🎓 Migrated {len(self.author_id_mapping)} authors")
    
    def get_main_image_url(self, images_dict):
        """Extract main image URL from images dict"""
        if not images_dict:
            return None
        
        # Try to get face image first
        face_images = images_dict.get('face_images', {})
        if face_images:
            return face_images.get('face500x500', face_images.get('face250x250', ''))
        
        # Fallback to full image
        full_images = images_dict.get('full_images', {})
        if full_images:
            return full_images.get('full600x800', '')
        
        return None
    
    async def update_schools_with_authors(self):
        """Update schools with their author IDs"""
        print("  🔗 Updating school-author relationships...")
        
        # Count authors by school
        school_author_counts = {}
        for philosopher in self.data.get('philosophers', []):
            school_name = philosopher.get('school', '').strip()
            if school_name and school_name in self.school_id_mapping:
                author_external_id = philosopher.get('id')
                if author_external_id in self.author_id_mapping:
                    if school_name not in school_author_counts:
                        school_author_counts[school_name] = []
                    school_author_counts[school_name].append(
                        self.author_id_mapping[author_external_id]
                    )
        
        # Update Firestore schools
        for school_name, author_ids in school_author_counts.items():
            if school_name in self.school_id_mapping:
                school_doc = self.firestore_service.db.collection('schools').document(
                    self.school_id_mapping[school_name]
                )
                school_doc.update({'author_ids': author_ids})
                print(f"    Updated {school_name} with {len(author_ids)} authors")
    
    async def migrate_books(self):
        """Create books from LibriVox data with cover art"""
        print("\n📖 Migrating books...")
        
        books_created = 0
        for philosopher in self.data.get('philosophers', []):
            if not philosopher.get('has_ebooks', False):
                continue
            
            # Get LibriVox books with detailed info
            librivox_books = philosopher.get('librivox_books', [])
            author_external_id = philosopher.get('id')
            author_firestore_id = self.author_id_mapping.get(author_external_id)
            
            if not librivox_books and philosopher.get('librivox_ids'):
                # Fallback: create books from just IDs
                for librivox_id in philosopher.get('librivox_ids', []):
                    librivox_books.append({
                        'id': str(librivox_id),
                        'coverArtPath': f'/Images/LibriVox/{librivox_id}.jpg'
                    })
            
            for book_data in librivox_books:
                librivox_id = book_data.get('id', '')
                cover_path = book_data.get('coverArtPath', '')
                
                # Build full image URLs
                cover_art_url = ''
                if cover_path:
                    if cover_path.startswith('/'):
                        cover_art_url = f"https://philosophersapi.com{cover_path}"
                    else:
                        cover_art_url = cover_path
                
                firestore_book = BookModel(
                    librivox_id=librivox_id,
                    titulo=f"Obra de {philosopher.get('name', 'Unknown')} (LibriVox {librivox_id})",
                    descripcion=f"Audiolibro disponible en LibriVox - ID: {librivox_id}",
                    
                    # Cover art
                    imagen_url=cover_art_url,
                    cover_art_path=cover_path,
                    
                    # LibriVox info
                    librivox_url=book_data.get('getRequestURL', f"https://librivox.org/api/feed/audiobooks/?id={librivox_id}"),
                    es_audiolibro=True,
                    
                    # Author relationship
                    autor_id=author_firestore_id,
                    autor_nombre=philosopher.get('name', ''),
                    
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                
                await self.firestore_service.create_book(firestore_book)
                books_created += 1
                
                if cover_art_url:
                    print(f"  ✓ Book: {philosopher.get('name')} - LibriVox {librivox_id} (with cover)")
                else:
                    print(f"  ✓ Book: {philosopher.get('name')} - LibriVox {librivox_id}")
        
        print(f"📖 Migrated {books_created} books with cover art")
    
    async def migrate_quotes(self):
        """Migrate real quotes from JSON data"""
        print("\n💬 Migrating quotes from JSON...")
        
        # Get real quotes from JSON
        json_quotes = self.data.get('quotes', [])
        print(f"💬 Found {len(json_quotes)} quotes in JSON")
        
        quotes_created = 0
        for quote_data in json_quotes:
            # Get quote info
            external_id = quote_data.get('id', '')
            quote_text = quote_data.get('quote', '').strip()
            work = quote_data.get('work', '').strip()
            year = quote_data.get('year', '').strip()
            philosopher_id = quote_data.get('philosopher_id', '')
            
            if not quote_text:
                continue
            
            # Find author by philosopher_id
            author_firestore_id = None
            author_name = None
            
            if philosopher_id and philosopher_id in self.author_id_mapping:
                author_firestore_id = self.author_id_mapping[philosopher_id]
                # Get author name
                for philosopher in self.data.get('philosophers', []):
                    if philosopher.get('id') == philosopher_id:
                        author_name = philosopher.get('name', '')
                        break
            
            # Create quote (even without author match)
            firestore_quote = QuoteModel(
                external_id=external_id,
                texto=quote_text,
                obra=work if work else None,
                año=year if year else None,
                autor_id=author_firestore_id,
                autor_nombre=author_name,
                philosopher_external_id=philosopher_id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            await self.firestore_service.create_quote(firestore_quote)
            quotes_created += 1
            
            if author_name:
                print(f"  ✓ Quote: {author_name} - '{quote_text[:50]}...'")
            else:
                print(f"  ✓ Quote: Unknown author - '{quote_text[:50]}...'")
        
        print(f"💬 Migrated {quotes_created} real quotes from JSON")
    
    async def show_stats(self):
        """Show final migration statistics"""
        print("\n📊 Migration Statistics:")
        stats = await self.firestore_service.get_stats()
        
        print(f"  Authors: {stats.get('authors_count', 0)}")
        print(f"  Schools: {stats.get('schools_count', 0)}")  
        print(f"  Books: {stats.get('books_count', 0)}")
        print(f"  Quotes: {stats.get('quotes_count', 0)}")
    
    async def fix_book_titles(self):
        """Fix book titles by fetching real titles from LibriVox API"""
        print("\n🔧 Fixing book titles from LibriVox...")
        
        # Get all books
        books = await self.firestore_service.get_books(limit=500)
        
        # Filter books with 'Obra de' titles
        books_to_fix = [book for book in books if book.titulo.startswith("Obra de")]
        
        print(f"📝 Found {len(books_to_fix)} books to fix")
        
        for i, book in enumerate(books_to_fix):
            try:
                print(f"[{i+1}/{len(books_to_fix)}] Processing: {book.titulo}")
                
                # Get LibriVox ID
                librivox_id = book.librivox_id
                if not librivox_id:
                    print(f"  ❌ No LibriVox ID for {book.titulo}")
                    continue
                    
                # Fetch real title from LibriVox API
                print(f"  🌐 Fetching title for LibriVox ID: {librivox_id}")
                url = f"https://librivox.org/api/feed/audiobooks/?id={librivox_id}&format=json"
                
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('books') and len(data['books']) > 0:
                        real_title = data['books'][0]['title']
                        
                        if real_title and real_title != book.titulo:
                            # Update in Firestore
                            print(f"  ✏️  Updating: '{book.titulo}' → '{real_title}'")
                            
                            doc_ref = self.firestore_service.db.collection('books').document(book.id)
                            doc_ref.update({
                                'titulo': real_title,
                                'updated_at': datetime.now(timezone.utc)
                            })
                            
                            print(f"  ✅ Updated successfully!")
                        else:
                            print(f"  ℹ️  No change needed")
                    else:
                        print(f"  ❌ No book data from LibriVox for ID {librivox_id}")
                else:
                    print(f"  ❌ LibriVox API error: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Error processing {book.titulo}: {e}")
                
            # Small delay to be respectful to LibriVox API
            time.sleep(0.5)
        
        print("🎉 Book title fix completed!")


async def fix_titles_only():
    """Run only the title fix without migration"""
    print("🏛️ Filosofía App - Book Title Fixer")
    
    migrator = JSONToFirestoreMigrator()
    
    try:
        await migrator.fix_book_titles()
        print("\n🎉 Title fix completed successfully!")
    except Exception as e:
        print(f"❌ Title fix failed: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Main migration function"""
    print("🏴‍☠️ PiratePhilosopher JSON → Firestore Migration")
    print("=" * 50)
    
    # Run migration
    migrator = JSONToFirestoreMigrator()
    
    try:
        await migrator.migrate_all()
        print("\n🎉 Migration completed successfully!")
        print("🔥 Your Firestore database is ready!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "fix-titles":
        # Run only the title fix
        asyncio.run(fix_titles_only())
    else:
        # Run full migration
        asyncio.run(main())