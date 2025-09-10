# 🏛️ Pirate Philosopher

Modern web application to explore philosophy through authors, philosophical schools, books, and inspirational quotes.

🌐 **[View live application →](https://www.piratephilosopher.com)**

## 🌟 Current Status

**Architecture:** Fully migrated to **GCP Serverless + Firestore**

- ✅ **Backend:** FastAPI on Google Cloud Run
- ✅ **Database:** Google Firestore (NoSQL)
- ✅ **Frontend:** Next.js 14 with TypeScript deployed on Vercel
- ✅ **Domain:** www.piratephilosopher.com
- ✅ **Infrastructure:** Terraform for GCP

## ✨ Content

- **200+ Philosophers** with complete biographies
- **20+ Philosophical Schools** throughout history
- **182 Books** with real titles from LibriVox
- **60+ Inspirational Quotes** verified

## 🛠️ Tech Stack

**Frontend:**
- Next.js 14 with App Router
- TypeScript & Tailwind CSS
- Optimized Server-Side Rendering

**Backend:**
- FastAPI (Python) optimized for Cloud Functions
- Google Firestore as NoSQL database
- Pydantic for data validation

**Infrastructure:**
- Google Cloud Run (Backend Serverless)
- Google Firestore (Database)
- Vercel (Frontend Deployment)
- Terraform for Infrastructure as Code

## 🚀 Local Development

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend)
- Google Cloud credentials configured

### Quick Start

```bash
# Clone repository
git clone https://github.com/your-username/pirate-philosopher
cd pirate-philosopher

# Configure environment variables
cp .env.gcp .env.gcp.local
# Edit .env.gcp.local with your configurations

# Start backend (Docker)
docker-compose -f docker-compose-gcp.yml up -d backend

# Start frontend (local)
cd frontend
npm install
npm run dev
```

### Development URLs
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📚 Features

- **🔍 Search** philosophers by name and era
- **📖 Book Catalog** with audiobook links
- **🏛️ Philosophical Schools** with their representatives
- **💬 Inspirational Quotes** categorized
- **📱 Responsive** mobile-optimized design
- **⚡ Performance** with SSR and Next.js optimizations

## 🚧 Roadmap

| Feature | Status |
|---------|--------|
| 🧱 **Firestore Database** | ✅ **Completed** |
| 📚 **Complete REST API** | ✅ **Completed** |
| 🎨 **Modern Frontend** | ✅ **Completed** |
| 🔍 **Advanced Search** | 🔄 In Progress |
| 🤖 **AI Integration** | 🔜 Coming Soon |
| 🌐 **PWA** | 🔜 Coming Soon |

## 📄 Documentation

Complete technical documentation is available at:
- **API Docs** - http://localhost:8000/docs (when running backend)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-functionality`)
3. Commit changes (`git commit -m 'Add new functionality'`)
4. Push to branch (`git push origin feature/new-functionality`)
5. Open Pull Request

## 📜 License

This project is under the MIT License. See `LICENSE` for more details.

---

*Developed with ❤️ to democratize access to philosophical knowledge*

<!-- CI/CD Test - Trigger deployment -->