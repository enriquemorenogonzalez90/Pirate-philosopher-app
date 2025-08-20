#!/usr/bin/env python3
"""Script to debug date serialization issues"""

import json
from datetime import date
from app.database import engine
from sqlalchemy.orm import Session
from app.models import Author
from app.schemas import AuthorRead

def main():
    print("🔍 Debugging date serialization...")
    
    with Session(engine) as session:
        # Get first few authors
        authors = session.query(Author).limit(5).all()
        print(f"Found {len(authors)} authors in database")
        
        for author in authors:
            print(f"\n📖 Author: {author.nombre}")
            print(f"   ID: {author.id}")
            print(f"   Birth: {author.fecha_nacimiento} (type: {type(author.fecha_nacimiento)})")
            print(f"   Death: {author.fecha_defuncion} (type: {type(author.fecha_defuncion)})")
            
            # Test Pydantic serialization
            try:
                author_schema = AuthorRead.model_validate(author)
                print(f"   ✅ Pydantic validation: OK")
                
                # Test JSON serialization
                json_data = author_schema.model_dump_json()
                print(f"   ✅ JSON serialization: OK")
                print(f"   JSON: {json_data[:100]}...")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print(f"   Error type: {type(e)}")
                
                # Check if the issue is with dates specifically
                if author.fecha_nacimiento:
                    try:
                        json.dumps(author.fecha_nacimiento, default=str)
                        print(f"   Date serialization with str(): OK")
                    except Exception as date_e:
                        print(f"   Date error: {date_e}")

if __name__ == "__main__":
    main()