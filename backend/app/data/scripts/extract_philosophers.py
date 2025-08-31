#!/usr/bin/env python3
"""
Script unificado para extraer datos completos desde philosophersapi.com
Extrae filósofos, biografías, imágenes, fechas, libros y quotes.
"""

import json
import requests
import time
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PhilosophersAPIClient:
    """Cliente para la API de philosophersapi.com"""
    
    BASE_URL = "https://philosophersapi.com/api"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Filosofia-App/1.0'
        })
    
    def get_all_philosophers(self) -> List[Dict[str, Any]]:
        """Obtiene la lista completa de filósofos"""
        try:
            url = f"{self.BASE_URL}/philosophers"
            logger.info(f"Obteniendo filósofos desde: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            philosophers = response.json()
            logger.info(f"Obtenidos {len(philosophers)} filósofos de la API")
            return philosophers
        except requests.RequestException as e:
            logger.error(f"Error obteniendo filósofos: {e}")
            return []
    
    def get_all_quotes(self) -> List[Dict[str, Any]]:
        """Obtiene todas las quotes de la API"""
        try:
            url = f"{self.BASE_URL}/quotes"
            logger.info(f"Obteniendo quotes desde: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            quotes = response.json()
            logger.info(f"Obtenidas {len(quotes)} quotes de la API")
            return quotes
        except requests.RequestException as e:
            logger.error(f"Error obteniendo quotes: {e}")
            return []
    
    def get_philosopher_ebooks(self, philosopher_id: str) -> Dict[str, Any]:
        """Obtiene los libros de un filósofo específico"""
        try:
            url = f"{self.BASE_URL}/philosophers/ebooks/{philosopher_id}"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except requests.RequestException as e:
            logger.warning(f"Error obteniendo libros para {philosopher_id}: {e}")
            return {}
    
    def extract_philosopher_data(self, philosopher: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae y estructura los datos de un filósofo"""
        
        # Información básica
        data = {
            'id': philosopher.get('id'),
            'name': philosopher.get('name', '').strip(),
            'username': philosopher.get('username', '').strip(),
            'life': philosopher.get('life', '').strip(),
            'topical_description': philosopher.get('topicalDescription', '').strip(),
            'interests': philosopher.get('interests', '').strip(),
        }
        
        # Fechas de nacimiento y muerte
        data.update({
            'birth_date': philosopher.get('birthDate', '').strip(),
            'death_date': philosopher.get('deathDate', '').strip(),
            'birth_year': philosopher.get('birthYear', '').strip(),
            'death_year': philosopher.get('deathYear', '').strip(),
        })
        
        # Escuela filosófica y lugar de nacimiento (si está disponible)
        data.update({
            'school': philosopher.get('school', '').strip(),
            'birth_place': philosopher.get('birthPlace', '').strip(),  # Por si lo agregan
        })
        
        # Enlaces - biografía principal en iep_link
        data.update({
            'iep_link': philosopher.get('iepLink', '').strip(),  # Biografía principal
            'spe_link': philosopher.get('speLink', '').strip(),
            'wiki_title': philosopher.get('wikiTitle', '').strip(),
        })
        
        # Imágenes organizadas - convertir URLs relativas a absolutas
        images = philosopher.get('images', {})
        
        def convert_image_urls(image_dict):
            """Convierte URLs relativas a absolutas"""
            converted = {}
            for key, url in image_dict.items():
                if isinstance(url, str) and url.startswith('/'):
                    converted[key] = f"https://philosophersapi.com{url}"
                else:
                    converted[key] = url
            return converted
        
        data['images'] = {
            'face_images': convert_image_urls(images.get('faceImages', {})),
            'full_images': convert_image_urls(images.get('fullImages', {})),
            'illustrations': convert_image_urls(images.get('illustrations', {})),
            'thumbnail_illustrations': convert_image_urls(images.get('thumbnailIllustrations', {})),
        }
        
        # Información sobre libros
        data.update({
            'has_ebooks': philosopher.get('hasEBooks', False),
            'librivox_ids': philosopher.get('libriVoxIDs', []),
            'librivox_get_request_links': philosopher.get('libriVoxGetRequestLinks', []),
        })
        
        return data
    
    def extract_quote_data(self, quote: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae y estructura los datos de una quote"""
        
        data = {
            'id': quote.get('id'),
            'quote': quote.get('quote', '').strip(),
            'work': quote.get('work', '').strip(),
            'year': quote.get('year', '').strip(),
            'internal_id': quote.get('internalID'),
        }
        
        # Información del filósofo asociado
        philosopher = quote.get('philosopher', {})
        data['philosopher_id'] = philosopher.get('id') if philosopher else None
        
        return data
    
    def extract_biography_from_url(self, url: str, philosopher_name: str) -> str:
        """Extrae biografía desde enlaces IEP o Stanford Encyclopedia"""
        if not url:
            return ""
            
        try:
            logger.debug(f"Extrayendo biografía de {url} para {philosopher_name}")
            response = self.session.get(url, timeout=8)  # Timeout más corto
            response.raise_for_status()
            
            html_content = response.text
            
            # Estrategias específicas por sitio usando regex
            if 'iep.utm.edu' in url:
                return self._extract_iep_biography_regex(html_content, philosopher_name)
            elif 'plato.stanford.edu' in url:
                return self._extract_stanford_biography_regex(html_content, philosopher_name)
            else:
                return ""
                
        except Exception as e:
            logger.warning(f"Error extrayendo biografía de {url}: {e}")
            return ""
    
    def _extract_iep_biography_regex(self, html_content: str, name: str) -> str:
        """Extrae SOLO el primer párrafo de biografía de IEP"""
        try:
            # Buscar párrafos después del contenido principal
            paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL | re.IGNORECASE)
            
            # Buscar solo el PRIMER párrafo útil
            for p in paragraphs[:8]:  # Revisar máximo 8 párrafos
                # Limpiar HTML tags
                text = re.sub(r'<[^>]+>', '', p)
                text = re.sub(r'\s+', ' ', text).strip()
                
                # Filtrar primer párrafo útil (que mencione al filósofo y tenga contenido)
                if len(text) > 80 and (name.split()[0] in text or name.split()[-1] in text):
                    return text[:500] + "..." if len(text) > 500 else text
            
            # Si no encuentra párrafo específico, tomar el primer párrafo largo
            for p in paragraphs[:5]:
                text = re.sub(r'<[^>]+>', '', p)
                text = re.sub(r'\s+', ' ', text).strip()
                if len(text) > 100:
                    return text[:500] + "..." if len(text) > 500 else text
                
        except Exception as e:
            logger.warning(f"Error extrayendo de IEP para {name}: {e}")
        
        return ""
    
    def _extract_stanford_biography_regex(self, html_content: str, name: str) -> str:
        """Extrae SOLO el primer párrafo de Stanford Encyclopedia"""
        try:
            # Buscar párrafos
            paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL | re.IGNORECASE)
            
            # Buscar solo el PRIMER párrafo útil
            for p in paragraphs[:8]:  # Revisar máximo 8 párrafos
                # Limpiar HTML tags y referencias
                text = re.sub(r'<[^>]+>', '', p)
                text = re.sub(r'\[\d+\]', '', text)  # Eliminar [1], [2], etc.
                text = re.sub(r'\s+', ' ', text).strip()
                
                # Filtrar primer párrafo útil (que mencione al filósofo y tenga contenido)
                if len(text) > 80 and (name.split()[0] in text or name.split()[-1] in text):
                    return text[:500] + "..." if len(text) > 500 else text
            
            # Si no encuentra párrafo específico, tomar el primer párrafo largo
            for p in paragraphs[:5]:
                text = re.sub(r'<[^>]+>', '', p)
                text = re.sub(r'\[\d+\]', '', text)
                text = re.sub(r'\s+', ' ', text).strip()
                if len(text) > 100:
                    return text[:500] + "..." if len(text) > 500 else text
                
        except Exception as e:
            logger.warning(f"Error extrayendo de Stanford para {name}: {e}")
        
        return ""
    
    def get_complete_philosopher_data(self, philosopher: Dict[str, Any]) -> Dict[str, Any]:
        """Obtiene datos completos de un filósofo incluyendo libros"""
        
        # Datos básicos del filósofo
        data = self.extract_philosopher_data(philosopher)
        
        # Extraer biografía desde IEP o Stanford
        name = data.get('name', '')
        iep_link = data.get('iep_link', '')
        stanford_link = data.get('spe_link', '')
        
        biography = ""
        if iep_link:
            biography = self.extract_biography_from_url(iep_link, name)
        elif stanford_link:
            biography = self.extract_biography_from_url(stanford_link, name)
        
        # Si no hay biografía web, crear una sintética
        if not biography:
            topical_desc = data.get('topical_description', '')
            interests = data.get('interests', '')
            school = data.get('school', '')
            
            if topical_desc:
                biography = topical_desc
            elif interests:
                biography = f"Filósofo especializado en: {interests}."
                if school:
                    biography += f" Pertenece a la escuela {school}."
            elif school:
                biography = f"Filósofo de la escuela {school}."
        
        # Añadir biografía a los datos
        data['extracted_biography'] = biography
        
        # Obtener libros si están disponibles
        if data['has_ebooks'] or data['librivox_ids']:
            philosopher_id = data['id']
            if philosopher_id:
                logger.debug(f"Obteniendo libros para {data['name']}")
                ebooks_data = self.get_philosopher_ebooks(philosopher_id)
                
                if ebooks_data:
                    # Agregar información de libros con imágenes
                    data['librivox_audiobooks'] = ebooks_data.get('librivoxAudiobooks', [])
                    data['ebooks'] = ebooks_data.get('ebooks', [])
                else:
                    data['librivox_audiobooks'] = []
                    data['ebooks'] = []
            else:
                data['librivox_audiobooks'] = []
                data['ebooks'] = []
        else:
            data['librivox_audiobooks'] = []
            data['ebooks'] = []
        
        return data
    
    def fetch_all_data(self, limit: Optional[int] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Extrae todos los datos: filósofos y quotes"""
        
        logger.info("=== EXTRAYENDO FILÓSOFOS ===")
        philosophers_raw = self.get_all_philosophers()
        if not philosophers_raw:
            logger.error("No se pudieron obtener filósofos de la API")
            return {'philosophers': [], 'quotes': []}
        
        # Limitar para pruebas si se especifica
        if limit:
            philosophers_raw = philosophers_raw[:limit]
            logger.info(f"Limitando a {limit} filósofos para prueba")
        
        # Procesar filósofos
        philosophers_data = []
        total = len(philosophers_raw)
        
        for i, philosopher in enumerate(philosophers_raw, 1):
            name = philosopher.get('name', 'Sin nombre')
            logger.info(f"Procesando filósofo {i}/{total}: {name}")
            
            try:
                complete_philosopher = self.get_complete_philosopher_data(philosopher)
                philosophers_data.append(complete_philosopher)
                
                # Pausa pequeña para no sobrecargar la API
                time.sleep(0.2)
                
            except Exception as e:
                logger.error(f"Error procesando {name}: {e}")
                continue
        
        logger.info(f"Filósofos procesados: {len(philosophers_data)}")
        
        # Procesar quotes
        logger.info("=== EXTRAYENDO QUOTES ===")
        quotes_raw = self.get_all_quotes()
        quotes_data = []
        
        if quotes_raw:
            for i, quote in enumerate(quotes_raw, 1):
                try:
                    quote_data = self.extract_quote_data(quote)
                    quotes_data.append(quote_data)
                    
                    if i % 100 == 0:  # Log cada 100 quotes
                        logger.info(f"Procesadas {i}/{len(quotes_raw)} quotes")
                        
                except Exception as e:
                    logger.error(f"Error procesando quote {i}: {e}")
                    continue
            
            logger.info(f"Quotes procesadas: {len(quotes_data)}")
        
        return {
            'philosophers': philosophers_data,
            'quotes': quotes_data
        }
    
    def save_to_json(self, data: Dict[str, List[Dict[str, Any]]], base_filename: str = 'philosophers_complete_data'):
        """Guarda los datos en archivos JSON separados"""
        try:
            # Asegurar que el directorio data/json existe
            backend_root = Path(__file__).parent.parent
            json_dir = backend_root / 'json'
            json_dir.mkdir(exist_ok=True)
            
            # Guardar SOLO el archivo combinado
            complete_file = json_dir / f'{base_filename}.json'
            with open(complete_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📁 Archivo guardado:")
            logger.info(f"  - Completo: {complete_file} ({complete_file.stat().st_size / 1024:.1f} KB)")
            
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")
    
    def print_statistics(self, data: Dict[str, List[Dict[str, Any]]]):
        """Imprime estadísticas de los datos extraídos"""
        philosophers = data.get('philosophers', [])
        quotes = data.get('quotes', [])
        
        if not philosophers and not quotes:
            return
        
        logger.info("=== ESTADÍSTICAS DE EXTRACCIÓN ===")
        
        # Estadísticas de filósofos
        if philosophers:
            total_philosophers = len(philosophers)
            with_books = sum(1 for p in philosophers if p.get('librivox_audiobooks'))
            with_face_images = sum(1 for p in philosophers if p.get('images', {}).get('face_images'))
            with_biography = sum(1 for p in philosophers if p.get('iep_link'))
            with_school = sum(1 for p in philosophers if p.get('school'))
            
            logger.info(f"📚 FILÓSOFOS:")
            logger.info(f"  Total: {total_philosophers}")
            logger.info(f"  Con libros: {with_books}")
            logger.info(f"  Con imágenes faciales: {with_face_images}")
            logger.info(f"  Con enlaces de biografía: {with_biography}")
            logger.info(f"  Con escuela filosófica: {with_school}")
            
            # Escuelas más comunes
            schools = [p.get('school', '') for p in philosophers if p.get('school')]
            if schools:
                from collections import Counter
                common_schools = Counter(schools).most_common(5)
                logger.info("  Escuelas más comunes:")
                for school, count in common_schools:
                    logger.info(f"    - {school}: {count}")
        
        # Estadísticas de quotes
        if quotes:
            total_quotes = len(quotes)
            with_work = sum(1 for q in quotes if q.get('work'))
            with_year = sum(1 for q in quotes if q.get('year'))
            with_philosopher = sum(1 for q in quotes if q.get('philosopher_id'))
            
            logger.info(f"💭 QUOTES:")
            logger.info(f"  Total: {total_quotes}")
            logger.info(f"  Con obra especificada: {with_work}")
            logger.info(f"  Con año: {with_year}")
            logger.info(f"  Con filósofo asociado: {with_philosopher}")
            
            # Distribución de quotes por filósofo
            if philosophers:
                philosopher_names = {p['id']: p['name'] for p in philosophers}
                quote_counts = {}
                
                for quote in quotes:
                    phil_id = quote.get('philosopher_id')
                    if phil_id and phil_id in philosopher_names:
                        name = philosopher_names[phil_id]
                        quote_counts[name] = quote_counts.get(name, 0) + 1
                
                if quote_counts:
                    top_philosophers = sorted(quote_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                    logger.info("  Filósofos con más quotes:")
                    for name, count in top_philosophers:
                        logger.info(f"    - {name}: {count}")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extraer datos completos desde philosophersapi.com')
    parser.add_argument('--limit', type=int, help='Limitar número de filósofos (para pruebas)')
    parser.add_argument('--output', default='philosophers_complete_data', help='Nombre base de archivos de salida')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verbose')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    client = PhilosophersAPIClient()
    
    logger.info("=== INICIANDO EXTRACCIÓN COMPLETA DE DATOS ===")
    logger.info("📡 Extrayendo filósofos, libros y quotes desde philosophersapi.com")
    
    try:
        data = client.fetch_all_data(limit=args.limit)
        
        if data['philosophers'] or data['quotes']:
            client.save_to_json(data, args.output)
            client.print_statistics(data)
            logger.info("✅ Extracción completada exitosamente")
        else:
            logger.error("❌ No se pudieron extraer datos")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Extracción interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()