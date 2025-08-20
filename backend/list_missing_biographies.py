#!/usr/bin/env python3
"""
Script para listar autores que aún tienen biografías placeholder
"""

import os
import sys
sys.path.append('/opt/app')

from app.database import SessionLocal
from app.models import Author

def list_missing_biographies():
    """Lista autores que aún tienen biografías placeholder"""
    
    session = SessionLocal()
    
    print("📝 AUTORES SIN BIOGRAFÍA REAL")
    print("=" * 50)
    
    try:
        # Obtener autores con biografías placeholder
        authors_with_placeholder = session.query(Author).filter(
            Author.biografia.like('% fue un filósofo influyente.')
        ).order_by(Author.nombre).all()
        
        # Obtener autores con biografías reales
        authors_with_real = session.query(Author).filter(
            ~Author.biografia.like('% fue un filósofo influyente.')
        ).order_by(Author.nombre).all()
        
        total_authors = session.query(Author).count()
        
        print(f"📊 RESUMEN:")
        print(f"Total autores: {total_authors}")
        print(f"Con biografías reales: {len(authors_with_real)}")
        print(f"Con biografías placeholder: {len(authors_with_placeholder)}")
        print(f"Progreso: {len(authors_with_real)/total_authors*100:.1f}%")
        
        print(f"\n❌ AUTORES SIN BIOGRAFÍA REAL ({len(authors_with_placeholder)}):")
        print("-" * 60)
        
        for i, author in enumerate(authors_with_placeholder, 1):
            print(f"{i:2d}. {author.nombre}")
            
        print(f"\n✅ AUTORES CON BIOGRAFÍA REAL ({len(authors_with_real)}):")
        print("-" * 60)
        
        for i, author in enumerate(authors_with_real, 1):
            # Mostrar solo los primeros 50 caracteres de la biografía
            bio_preview = author.biografia[:50] + "..." if len(author.biografia) > 50 else author.biografia
            print(f"{i:2d}. {author.nombre} - {bio_preview}")
            
        print(f"\n📋 CATEGORÍAS DE AUTORES SIN BIOGRAFÍA:")
        print("-" * 50)
        
        # Categorizar autores faltantes
        medievales = [a.nombre for a in authors_with_placeholder if any(term in a.nombre for term in ['San ', 'Santo ', 'Bernardo', 'Hugo', 'Ricardo', 'Gregorio', 'Rábano', 'Alcuino', 'Gerbert', 'Fulberto', 'Hincmaro', 'Casiodoro', 'Isidoro', 'Beda', 'Juan Damasceno', 'Máximo el Confesor', 'Pseudo-Dionisio', 'Juan Escoto', 'Joaquín', 'Alano'])]
        
        orientales = [a.nombre for a in authors_with_placeholder if any(term in a.nombre for term in ['Huang', 'Hui', 'Shen', 'Ma Zu', 'Zhao', 'Yun', 'Fa Yan', 'Wei Yang', 'Bankei', 'Basho', 'Kukai', 'Saicho', 'Eisai', 'Myoan', 'Hakuin', 'Ikkyu', 'Ryokan', 'Suzuki', 'Asanga', 'Vasubandhu', 'Dignaga', 'Dharmakirti', 'Bodhidharma', 'Dogen', 'Nichiren', 'Honen', 'Shinran'])]
        
        antiguos = [a.nombre for a in authors_with_placeholder if any(term in a.nombre for term in ['Cleantes', 'Diógenes', 'Empédocles', 'Anaxágoras', 'Anaximandro', 'Anaxímenes', 'Jenófanes', 'Protágoras', 'Gorgias', 'Antístenes', 'Jámblico', 'Porfirio', 'Simplicio', 'Alejandro', 'Filón', 'Hierocles', 'Luciano', 'Galeno', 'Ptolomeo', 'Apolonio'])]
        
        modernos_contemporaneos = [a.nombre for a in authors_with_placeholder if any(term in a.nombre for term in ['George Berkeley', 'Friedrich Schelling', 'Daniel Dennett', 'Thomas Nagel', 'Isaiah Berlin', 'Alasdair MacIntyre', 'Charles Taylor'])]
        
        if medievales:
            print(f"\n🏰 Medievales/Cristianos ({len(medievales)}):")
            for name in medievales[:10]:  # Mostrar solo los primeros 10
                print(f"   - {name}")
            if len(medievales) > 10:
                print(f"   ... y {len(medievales) - 10} más")
                
        if orientales:
            print(f"\n🏯 Orientales/Asiáticos ({len(orientales)}):")
            for name in orientales[:10]:
                print(f"   - {name}")
            if len(orientales) > 10:
                print(f"   ... y {len(orientales) - 10} más")
                
        if antiguos:
            print(f"\n🏛️ Antiguos/Clásicos ({len(antiguos)}):")
            for name in antiguos[:10]:
                print(f"   - {name}")
            if len(antiguos) > 10:
                print(f"   ... y {len(antiguos) - 10} más")
                
        if modernos_contemporaneos:
            print(f"\n🎓 Modernos/Contemporáneos ({len(modernos_contemporaneos)}):")
            for name in modernos_contemporaneos:
                print(f"   - {name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    list_missing_biographies()