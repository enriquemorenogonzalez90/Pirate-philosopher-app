"""
🚀 AWS S3 Integration para Filosofía App
Manejo de imágenes y archivos estáticos en S3
"""

import boto3
import os
from typing import Optional
from botocore.exceptions import ClientError
import requests
from io import BytesIO

class S3Manager:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bucket_images = os.getenv('S3_BUCKET_IMAGES', 'filosofia-app-images')
        self.cloudfront_domain = os.getenv('CLOUDFRONT_DOMAIN', '')
    
    def upload_image_from_url(self, image_url: str, s3_key: str) -> Optional[str]:
        """
        Descarga una imagen de una URL y la sube a S3
        Retorna la URL de CloudFront si es exitoso
        """
        try:
            # Descargar imagen
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Determinar content type
            content_type = response.headers.get('content-type', 'image/jpeg')
            
            # Subir a S3
            self.s3_client.upload_fileobj(
                BytesIO(response.content),
                self.bucket_images,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'public-read'
                }
            )
            
            # Retornar URL de CloudFront
            if self.cloudfront_domain:
                return f"{self.cloudfront_domain}/{s3_key}"
            else:
                return f"https://{self.bucket_images}.s3.amazonaws.com/{s3_key}"
                
        except Exception as e:
            print(f"Error uploading image to S3: {e}")
            return None
    
    def upload_file(self, file_content: bytes, s3_key: str, content_type: str = 'application/octet-stream') -> Optional[str]:
        """
        Sube un archivo directamente a S3
        """
        try:
            self.s3_client.upload_fileobj(
                BytesIO(file_content),
                self.bucket_images,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'public-read'
                }
            )
            
            if self.cloudfront_domain:
                return f"{self.cloudfront_domain}/{s3_key}"
            else:
                return f"https://{self.bucket_images}.s3.amazonaws.com/{s3_key}"
                
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            return None
    
    def file_exists(self, s3_key: str) -> bool:
        """
        Verifica si un archivo existe en S3
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_images, Key=s3_key)
            return True
        except ClientError:
            return False
    
    def generate_author_image_key(self, author_name: str) -> str:
        """
        Genera una key única para la imagen de un autor
        """
        safe_name = author_name.lower().replace(' ', '-').replace('ñ', 'n')
        return f"authors/{safe_name}.jpg"
    
    def generate_school_image_key(self, school_name: str) -> str:
        """
        Genera una key única para la imagen de una escuela
        """
        safe_name = school_name.lower().replace(' ', '-').replace('ñ', 'n')
        return f"schools/{safe_name}.jpg"
    
    def generate_book_image_key(self, book_title: str, author_name: str) -> str:
        """
        Genera una key única para la portada de un libro
        """
        safe_title = book_title.lower().replace(' ', '-').replace('ñ', 'n')[:30]
        safe_author = author_name.lower().replace(' ', '-').replace('ñ', 'n')[:20]
        return f"books/{safe_author}-{safe_title}.jpg"

# Instancia global
s3_manager = S3Manager()

def migrate_images_to_s3():
    """
    Función para migrar todas las imágenes actuales a S3
    Se ejecuta una sola vez durante el despliegue
    """
    print("🚀 Iniciando migración de imágenes a S3...")
    
    # Esta función se puede ejecutar como un script separado
    # para migrar todas las imágenes existentes
    pass
