"""
🖼️ Wikipedia Image Extractor para Filosofía App
Extrae imágenes reales de filósofos desde Wikipedia
"""

import requests
import wikipedia
from bs4 import BeautifulSoup
from typing import Optional
import urllib.parse
import time

class WikipediaImageExtractor:
    def __init__(self):
        # Configurar Wikipedia en español
        wikipedia.set_lang("es")
        
    def get_philosopher_image(self, name: str) -> Optional[str]:
        """
        Extrae la imagen principal de un filósofo desde Wikipedia
        Retorna la URL de la imagen o None si no encuentra
        """
        try:
            print(f"🔍 Buscando imagen de {name} en Wikipedia...")
            
            # Diccionario de variantes de nombres para filósofos
            name_variants = {
                # Griegos clásicos
                "Cleantes": ["Cleanthes", "Cleantes de Assos"],
                "Gorgias": ["Gorgias", "Gorgias de Leontinos", "Gorgias of Leontini"], 
                "Crisipo": ["Chrysippus", "Crisipo de Soli"],
                "Zenón de Citio": ["Zeno of Citium", "Zenón de Citio"],
                "Diógenes": ["Diogenes of Sinope", "Diógenes de Sinope"],
                "Protágoras": ["Protagoras", "Protágoras de Abdera"],
                "Empédocles": ["Empedocles", "Empédocles de Agrigento"],
                "Anaxágoras": ["Anaxagoras", "Anaxágoras de Clazómenas"],
                "Demócrito": ["Democritus", "Demócrito de Abdera"],
                "Jenófanes": ["Xenophanes", "Jenófanes de Colofón"],
                "Antístenes": ["Antisthenes", "Antístenes de Atenas"],
                "Tales de Mileto": ["Thales", "Tales de Mileto"],
                "Anaximandro": ["Anaximander", "Anaximandro de Mileto"],
                "Anaxímenes": ["Anaximenes", "Anaxímenes de Mileto"],
                "Pitágoras": ["Pythagoras", "Pitágoras de Samos"],
                "Heráclito": ["Heraclitus", "Heráclito de Éfeso"],
                "Parménides": ["Parmenides", "Parménides de Elea"],
                
                # Romanos
                "Séneca": ["Seneca the Younger", "Lucius Annaeus Seneca"],
                "Marco Aurelio": ["Marcus Aurelius", "Marco Aurelio"],
                "Epicteto": ["Epictetus", "Epicteto"],
                
                # Neoplatónicos
                "Plotino": ["Plotinus", "Plotino"],
                "Proclo": ["Proclus", "Proclo Diadoco"],
                "Porfirio": ["Porphyry", "Porfirio de Tiro"],
                "Jámblico": ["Iamblichus", "Jámblico de Calcis"],
                "Simplicio": ["Simplicius", "Simplicio de Cilicia"],
                
                # Medievales islámicos
                "Al-Kindi": ["Al-Kindi", "Alkindus"],
                "Al-Farabi": ["Al-Farabi", "Alfarabi"],
                "Avicena": ["Avicenna", "Ibn Sina"],
                "Al-Ghazali": ["Al-Ghazali", "Algazel"],
                "Averroes": ["Averroes", "Ibn Rushd"],
                "Ibn Khaldun": ["Ibn Khaldun", "Ibn Jaldún"],
                "Maimonides": ["Maimonides", "Moses Maimonides"],
                
                # Medievales cristianos
                "Tomás de Aquino": ["Thomas Aquinas", "Santo Tomás de Aquino"],
                "San Agustín": ["Augustine of Hippo", "Saint Augustine"],
                "Anselmo de Canterbury": ["Anselm of Canterbury", "San Anselmo"],
                "Pedro Abelardo": ["Peter Abelard", "Pierre Abélard"],
                "Duns Escoto": ["Duns Scotus", "John Duns Scotus"],
                "Guillermo de Ockham": ["William of Ockham", "Guillermo de Occam"],
                "Alberto Magno": ["Albertus Magnus", "Albert the Great"],
                "Roger Bacon": ["Roger Bacon", "Doctor Mirabilis"],
                "Boecio": ["Boethius", "Anicius Manlius Severinus Boethius"],
                "Meister Eckhart": ["Meister Eckhart", "Johannes Eckhart"],
                
                # Modernos
                "René Descartes": ["René Descartes", "Descartes"],
                "Baruch Spinoza": ["Baruch Spinoza", "Benedict de Spinoza"],
                "Gottfried Leibniz": ["Gottfried Wilhelm Leibniz", "Leibniz"],
                "John Locke": ["John Locke", "Locke"],
                "David Hume": ["David Hume", "Hume"],
                "Immanuel Kant": ["Immanuel Kant", "Kant"],
                "Georg Hegel": ["Georg Wilhelm Friedrich Hegel", "Hegel"],
                "Arthur Schopenhauer": ["Arthur Schopenhauer", "Schopenhauer"],
                "Friedrich Nietzsche": ["Friedrich Nietzsche", "Nietzsche"],
                "Søren Kierkegaard": ["Søren Kierkegaard", "Kierkegaard"],
                
                # Contemporáneos
                "Martin Heidegger": ["Martin Heidegger", "Heidegger"],
                "Jean-Paul Sartre": ["Jean-Paul Sartre", "Sartre"],
                "Ludwig Wittgenstein": ["Ludwig Wittgenstein", "Wittgenstein"],
                "Hannah Arendt": ["Hannah Arendt", "Arendt"],
                "Michel Foucault": ["Michel Foucault", "Foucault"],
                "Jacques Derrida": ["Jacques Derrida", "Derrida"],
                
                # Asiáticos
                "Confucio": ["Confucius", "Kong Qiu"],
                "Lao Tzu": ["Laozi", "Lao Tse"],
                "Buda": ["Buddha", "Gautama Buddha", "Siddhartha Gautama"],
                "Nagarjuna": ["Nagarjuna", "Nāgārjuna"],
                "Shankara": ["Adi Shankara", "Śaṅkara"]
            }
            
            # Lista de nombres a probar (original + variantes)
            names_to_try = [name]
            if name in name_variants:
                names_to_try.extend(name_variants[name])
            
            page = None
            for name_to_try in names_to_try:
                try:
                    print(f"  🔄 Probando: {name_to_try}")
                    page = wikipedia.page(name_to_try)
                    break
                except wikipedia.exceptions.DisambiguationError as e:
                    # Si hay ambigüedad, tomar la primera opción que contenga "filósofo"
                    for option in e.options[:5]:
                        if any(word in option.lower() for word in ['filósofo', 'filosofo', 'philosopher']):
                            page = wikipedia.page(option)
                            break
                    if page:
                        break
                    else:
                        # Si no encuentra, tomar la primera opción
                        page = wikipedia.page(e.options[0])
                        break
                except wikipedia.exceptions.PageError:
                    continue
            
            if not page:
                print(f"❌ No se encontró página de Wikipedia para {name}")
                return None
            
            # Buscar imagen en el HTML de la página
            image_url = self._extract_main_image(page.url)
            
            if image_url:
                print(f"✅ Imagen encontrada para {name}: {image_url[:50]}...")
                return image_url
            else:
                print(f"⚠️ No se encontró imagen para {name}")
                return None
                
        except Exception as e:
            print(f"❌ Error buscando imagen de {name}: {e}")
            return None
    
    def _extract_main_image(self, wikipedia_url: str) -> Optional[str]:
        """
        Extrae la imagen principal de una página de Wikipedia
        """
        try:
            # Añadir delay para evitar rate limiting
            time.sleep(0.5)
            
            headers = {
                'User-Agent': 'FilosofiaApp/1.0 (https://github.com/balladOfAThinMan/Pirate-philosopher-app; enrique@filosofiaapp.com) requests/2.31.0'
            }
            
            response = requests.get(wikipedia_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar la imagen en el infobox
            infobox_image = soup.find('table', class_='infobox')
            if infobox_image:
                img = infobox_image.find('img')
                if img and img.get('src'):
                    # Convertir URL relativa a absoluta
                    img_src = img['src']
                    if img_src.startswith('//'):
                        img_src = 'https:' + img_src
                    elif img_src.startswith('/'):
                        img_src = 'https://es.wikipedia.org' + img_src
                    return img_src
            
            # Si no hay infobox, buscar la primera imagen significativa
            # Buscar en la zona de contenido principal
            content_div = soup.find('div', {'id': 'mw-content-text'})
            if content_div:
                # Buscar imágenes que no sean iconos
                images = content_div.find_all('img')
                for img in images:
                    src = img.get('src', '')
                    # Filtrar iconos y imágenes pequeñas
                    if (src and 
                        not any(skip in src.lower() for skip in ['edit', 'icon', 'commons', 'wikimedia', 'symbol']) and
                        'width' in img.attrs and 
                        int(img.get('width', 0)) >= 150):
                        
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            src = 'https://es.wikipedia.org' + src
                        return src
                        
            return None
            
        except Exception as e:
            print(f"❌ Error extrayendo imagen: {e}")
            return None

# Instancia global
wikipedia_extractor = WikipediaImageExtractor()

def get_wikipedia_image_url(philosopher_name: str) -> Optional[str]:
    """
    Función helper para obtener imagen de Wikipedia
    """
    return wikipedia_extractor.get_philosopher_image(philosopher_name)
