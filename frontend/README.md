# Coca-Cola Sora-2 Video Studio - Frontend

React + TypeScript frontend for the Coca-Cola Video Studio application.

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TailwindCSS** - Styling
- **React Router** - Navigation
- **TanStack Query** - Data fetching and caching
- **Axios** - HTTP client
- **Lucide React** - Icons

## Project Structure

```
frontend/
├── src/
│   ├── components/    # Reusable UI components
│   ├── pages/         # Page components
│   ├── services/      # API service functions
│   ├── types/         # TypeScript type definitions
│   ├── hooks/         # Custom React hooks
│   ├── store/         # State management
│   ├── App.tsx        # Main app component
│   └── main.tsx       # Entry point
├── public/            # Static assets
├── index.html         # HTML template
└── vite.config.ts     # Vite configuration
```

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create a `.env` file:

```env
VITE_API_URL=/api/v1
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm test` - Run tests

## Features

### Dashboard
- Overview of video generation statistics
- Recent videos list
- Quick access to projects

### Projects
- Create and manage video projects
- Organize videos by project
- Project-specific settings

### Video Generation
- Text-to-video generation with Sora-2
- Customizable duration (4, 8, or 12 seconds)
- Resolution selection (HD or Full HD)
- Project association
- Real-time status tracking

## Styling

The application uses TailwindCSS with Coca-Cola brand colors:
- Primary Red: `#F40009`
- Dark: `#1E1E1E`
- White: `#FFFFFF`

Custom utility classes are available:
- `.btn-primary` - Primary button style
- `.btn-secondary` - Secondary button style
- `.card` - Card container style

## API Integration

The frontend communicates with the backend API through the services layer:
- `videoService` - Video generation and management
- `projectService` - Project CRUD operations

All API calls include automatic:
- Authentication token injection
- Error handling
- Response caching (via TanStack Query)

## Docker

### Build

```bash
docker build -t coca-cola-video-studio-frontend .
```

### Run

```bash
docker run -p 80:80 coca-cola-video-studio-frontend
```

## Deployment

See `../docs/deployment.md` for Azure Container Apps deployment instructions.
