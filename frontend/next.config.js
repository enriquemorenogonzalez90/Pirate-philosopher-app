/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Optimizaciones para producción
  swcMinify: true,
  output: 'standalone',
  
  // Configuración de imágenes para AWS S3/CloudFront
  images: {
    domains: [
      'ui-avatars.com',
      'filosofia-app-images.s3.amazonaws.com',
      's3.amazonaws.com',
      'cloudfront.net'
    ],
    unoptimized: false,
  },
  
  // Variables de entorno públicas
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000',
    NEXT_PUBLIC_CDN_URL: process.env.NEXT_PUBLIC_CDN_URL || '',
  },
  
  // Headers de seguridad
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ];
  },
  
  // Compresión
  compress: true,
  
  // Configuración experimental
  experimental: {
    runtime: 'experimental-edge',
  },
};

module.exports = nextConfig;


