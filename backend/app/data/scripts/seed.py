#!/usr/bin/env python3
"""
Seed script unificado que utiliza datos de philosophersapi.com
Reemplaza seed.py anterior con datos más completos y actualizados.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import re
import requests
import time

# Agregar el directorio app al path para poder importar
# Ahora data/ está dentro de app/, así que subimos 2 niveles para llegar a app/
app_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(app_path))

from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.models import Author, School, Book, Quote

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PhilosopherSeeder:
    """Seeder para datos de filósofos desde la API"""
    
    def __init__(self, db: Session):
        self.db = db
        self.data_dir = Path(__file__).parent.parent / "json"
        
    def parse_date_string(self, date_str: str) -> Optional[datetime]:
        """Intenta parsear una fecha en formato de texto a datetime"""
        if not date_str or date_str.strip() == "":
            return None
            
        # Patrones comunes de fecha
        patterns = [
            r"(\d{1,2})\s+(\w+)\s+(\d{4})",  # "16 June 1723"
            r"(\d{4})",                       # "1723"
        ]
        
        months = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        
        try:
            # Patrón completo: "16 June 1723"
            match = re.search(patterns[0], date_str, re.IGNORECASE)
            if match:
                day, month_name, year = match.groups()
                month = months.get(month_name.lower())
                if month:
                    return datetime(int(year), month, int(day))
            
            # Solo año: "1723"
            match = re.search(patterns[1], date_str)
            if match:
                year = int(match.group(1))
                return datetime(year, 1, 1)  # Primer día del año
                
        except (ValueError, KeyError) as e:
            logger.warning(f"No se pudo parsear fecha '{date_str}': {e}")
            
        return None
    
    def get_or_create_school(self, school_name: str) -> Optional[School]:
        """Obtiene o crea una escuela filosófica"""
        if not school_name or school_name.strip() == "":
            return None
            
        school_name = school_name.strip()
        
        # Buscar escuela existente
        school = self.db.query(School).filter(School.nombre == school_name).first()
        
        if not school:
            school = School(
                nombre=school_name,
                descripcion=f"Escuela filosófica: {school_name}"
            )
            self.db.add(school)
            self.db.flush()  # Para obtener el ID
            logger.info(f"Creada nueva escuela: {school_name}")
            
        return school
    
    def get_librivox_book_title(self, librivox_url: str, book_id: str) -> str:
        """Obtiene el título real de un libro desde LibriVox API"""
        try:
            response = requests.get(librivox_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            books = data.get('books', [])
            if books and len(books) > 0:
                book = books[0]
                title = book.get('title', f'LibriVox Audio Book {book_id}')
                return title
            
        except Exception as e:
            logger.warning(f"Error obteniendo título de LibriVox para ID {book_id}: {e}")
        
        return f'LibriVox Audio Book {book_id}'
    
    def create_author(self, philosopher_data: Dict[str, Any]) -> Author:
        """Crea un autor desde los datos de la API"""
        
        # Parsear fechas
        birth_date = self.parse_date_string(philosopher_data.get('birth_date', ''))
        death_date = self.parse_date_string(philosopher_data.get('death_date', ''))
        
        # Obtener URL de imagen principal
        images = philosopher_data.get('images', {})
        face_images = images.get('face_images', {})
        main_image_url = face_images.get('face500x500', '') or face_images.get('face250x250', '') or ""
        
        # Usar biografía extraída o topical_description como fallback
        extracted_bio = philosopher_data.get('extracted_biography', '')
        topical_desc = philosopher_data.get('topical_description', '')
        iep_link = philosopher_data.get('iep_link', '')
        
        # Priorizar biografía extraída, luego topical_description
        biografia = extracted_bio or topical_desc
        
        # Si hay enlace IEP, añadirlo al final para más información
        if biografia and iep_link and not extracted_bio:
            biografia = f"{biografia}\n\nMás información: {iep_link}"
        
        # Crear el autor
        author = Author(
            external_id=philosopher_data.get('id'),
            nombre=philosopher_data.get('name', ''),
            username=philosopher_data.get('username', ''),
            vida=philosopher_data.get('life', ''),
            descripcion_topica=topical_desc,
            areas_interes=philosopher_data.get('interests', ''),
            biografia=biografia,
            
            # Fechas completas de la API
            fecha_nacimiento_completa=philosopher_data.get('birth_date', ''),
            fecha_muerte_completa=philosopher_data.get('death_date', ''),
            año_nacimiento=philosopher_data.get('birth_year', ''),
            año_muerte=philosopher_data.get('death_year', ''),
            
            # Fechas parseadas
            fecha_nacimiento=birth_date.date() if birth_date else None,
            fecha_defuncion=death_date.date() if death_date else None,
            epoca=philosopher_data.get('life', ''),
            
            # Escuela principal
            escuela_principal=philosopher_data.get('school', ''),
            
            # Enlaces
            enlace_iep=philosopher_data.get('iep_link', ''),
            enlace_stanford=philosopher_data.get('spe_link', ''),
            titulo_wiki=philosopher_data.get('wiki_title', ''),
            
            # Imágenes
            imagenes=images,
            imagen_url=main_image_url,
            
            # Información de libros
            tiene_libros=philosopher_data.get('has_ebooks', False),
            libros_librivox=philosopher_data.get('librivox_audiobooks', []),
        )
        
        return author
    
    def create_books_for_author(self, author: Author, philosopher_data: Dict[str, Any]):
        """Crea libros para un autor desde los datos de LibriVox"""
        
        librivox_books = philosopher_data.get('librivox_audiobooks', [])
        
        for book_data in librivox_books:
            librivox_id = book_data.get('id', '')
            librivox_url = book_data.get('getRequestURL', '')
            
            # Obtener título real desde LibriVox
            titulo = self.get_librivox_book_title(librivox_url, librivox_id)
            
            # Convertir cover path a URL absoluta
            cover_path = book_data.get('coverArtPath', '')
            cover_url = f"https://philosophersapi.com{cover_path}" if cover_path else ""
            
            # Crear el libro
            book = Book(
                librivox_id=librivox_id,
                titulo=titulo,
                cover_art_path=cover_path,
                imagen_url=cover_url,
                librivox_url=librivox_url,
                es_audiolibro=True,
                es_ebook=False,
                autor_id=author.id
            )
            
            self.db.add(book)
            
            # Pausa para no sobrecargar LibriVox
            time.sleep(0.2)
        
        # También agregar ebooks si existen
        ebooks = philosopher_data.get('ebooks', [])
        for ebook_data in ebooks:
            book = Book(
                titulo=ebook_data.get('title', 'Ebook sin título'),
                descripcion=ebook_data.get('description', ''),
                es_audiolibro=False,
                es_ebook=True,
                autor_id=author.id
            )
            self.db.add(book)
    
    def seed_philosophers(self) -> int:
        """Seed de filósofos desde el archivo JSON único"""
        
        complete_data_file = self.data_dir / "philosophers_complete_data.json"
        
        if not complete_data_file.exists():
            logger.error(f"Archivo no encontrado: {complete_data_file}")
            logger.info("Ejecuta primero: python data/scripts/extract_philosophers.py")
            return 0
        
        logger.info(f"Cargando datos completos desde: {complete_data_file}")
        
        with open(complete_data_file, 'r', encoding='utf-8') as f:
            complete_data = json.load(f)
        
        philosophers_data = complete_data.get('philosophers', [])
        
        created_count = 0
        
        for philosopher_data in philosophers_data:
            external_id = philosopher_data.get('id')
            name = philosopher_data.get('name', 'Sin nombre')
            
            # Verificar si ya existe
            existing = self.db.query(Author).filter(Author.external_id == external_id).first()
            if existing:
                logger.debug(f"Filósofo ya existe: {name}")
                continue
            
            try:
                # Crear el autor
                author = self.create_author(philosopher_data)
                self.db.add(author)
                self.db.flush()  # Para obtener el ID
                
                # Crear libros
                self.create_books_for_author(author, philosopher_data)
                
                # Asociar con escuela si existe
                school_name = philosopher_data.get('school')
                if school_name:
                    school = self.get_or_create_school(school_name)
                    if school and school not in author.schools:
                        author.schools.append(school)
                
                created_count += 1
                logger.info(f"Creado filósofo: {name}")
                
            except Exception as e:
                logger.error(f"Error creando filósofo {name}: {e}")
                self.db.rollback()
                continue
        
        self.db.commit()
        logger.info(f"Filósofos creados: {created_count}")
        return created_count
    
    def seed_quotes(self) -> int:
        """Seed de quotes desde el archivo JSON único"""
        
        complete_data_file = self.data_dir / "philosophers_complete_data.json"
        
        if not complete_data_file.exists():
            logger.error(f"Archivo no encontrado: {complete_data_file}")
            return 0
        
        logger.info(f"Cargando quotes desde archivo completo: {complete_data_file}")
        
        with open(complete_data_file, 'r', encoding='utf-8') as f:
            complete_data = json.load(f)
        
        quotes_data = complete_data.get('quotes', [])
        
        # Crear mapa de external_id -> author_id para mapear quotes
        philosophers_map = {}
        authors = self.db.query(Author).all()
        for author in authors:
            if author.external_id:
                philosophers_map[author.external_id] = author.id
        
        created_count = 0
        
        for quote_data in quotes_data:
            external_id = quote_data.get('id')
            text = quote_data.get('quote', '').strip()
            
            if not text:
                continue
                
            # Verificar si ya existe
            existing = self.db.query(Quote).filter(Quote.external_id == external_id).first()
            if existing:
                continue
            
            try:
                # Buscar el autor correspondiente
                philosopher_id = quote_data.get('philosopher_id')
                author_id = philosophers_map.get(philosopher_id)
                
                quote = Quote(
                    external_id=external_id,
                    internal_id=quote_data.get('internal_id'),
                    texto=text,
                    obra=quote_data.get('work', ''),
                    año=quote_data.get('year', ''),
                    autor_id=author_id,
                    philosopher_external_id=philosopher_id
                )
                
                self.db.add(quote)
                created_count += 1
                
                if created_count % 100 == 0:
                    logger.info(f"Procesadas {created_count} quotes...")
                
            except Exception as e:
                logger.error(f"Error creando quote: {e}")
                continue
        
        self.db.commit()
        logger.info(f"Quotes creadas: {created_count}")
        return created_count
    
    def seed_all(self):
        """Ejecuta todo el proceso de seeding"""
        
        logger.info("=== INICIANDO SEED DE DATOS ===")
        
        try:
            # Seed filósofos
            philosophers_count = self.seed_philosophers()
            
            # Seed quotes
            quotes_count = self.seed_quotes()
            
            # Estadísticas finales
            total_authors = self.db.query(Author).count()
            total_schools = self.db.query(School).count()
            total_books = self.db.query(Book).count()
            total_quotes = self.db.query(Quote).count()
            
            logger.info("=== SEED COMPLETADO ===")
            logger.info(f"📊 Estadísticas finales:")
            logger.info(f"   - Autores: {total_authors}")
            logger.info(f"   - Escuelas: {total_schools}")
            logger.info(f"   - Libros: {total_books}")
            logger.info(f"   - Quotes: {total_quotes}")
            logger.info(f"✅ Nuevos en esta ejecución:")
            logger.info(f"   - Filósofos: {philosophers_count}")
            logger.info(f"   - Quotes: {quotes_count}")
            
        except Exception as e:
            logger.error(f"Error durante el seed: {e}")
            self.db.rollback()
            raise

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Seed de datos desde philosophersapi.com')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verbose')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    db = SessionLocal()
    
    try:
        seeder = PhilosopherSeeder(db)
        seeder.seed_all()
        
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        sys.exit(1)
        
    finally:
        db.close()

if __name__ == "__main__":
    main()