# kl

Backend API for kl

## Tech Stack

- **Frontend**: React
- **Backend**: FastAPI + SQLAlchemy
- **Frontend Source**: GitHub ([Repository](https://github.com/HimaShankarReddyEguturi/Hotelbookinguidesign))

## Project Structure

```
kl/
├── frontend/          # Frontend application
├── backend/           # Backend API
├── README.md          # This file
└── docker-compose.yml # Docker configuration (if applicable)
```

## Getting Started

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for Python backends)
- Docker (optional, for containerized setup)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
# Follow backend-specific setup instructions in backend/README.md
```

## Features

- account management
- password reset
- profile management

## API Endpoints

- `POST /api/register` - Create a new user account
- `POST /api/login` - Log in to the application
- `POST /api/reset-password` - Reset the user's password
- `GET /api/profile` - Get the user's account information
- `PUT /api/profile` - Update the user's account information
- `DELETE /api/profile` - Delete the user's account

## License

MIT
