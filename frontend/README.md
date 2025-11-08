# Loan Document Intelligence System - Frontend

A modern, dark-themed React + Next.js frontend for the AI-powered Loan Document Intelligence System.

## 🚀 Features

- **Modern Dark UI**: Professional dark theme with teal/emerald accents
- **Responsive Design**: Fully responsive from mobile to desktop
- **Real-time Chat**: AI-powered chat interface with multiple LLM providers
- **Document Upload**: Drag-and-drop file upload with progress tracking
- **Smart Suggestions**: Context-aware query suggestions
- **Multi-Provider Support**: Switch between OpenAI, Anthropic, and Kimi K2
- **Smooth Animations**: Framer Motion powered transitions
- **Type-Safe**: Built with TypeScript

## 📦 Tech Stack

- **Framework**: Next.js 14
- **UI Library**: React 18
- **Styling**: TailwindCSS
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **File Upload**: React Dropzone
- **Type System**: TypeScript

## 🎨 Design System

### Color Palette
- **Primary Dark**: `#0a0c10` - `#1a1d29`
- **Slate Dark**: `#151820` - `#2a2f3f`
- **Accent Teal**: `#14b8a6`
- **Accent Emerald**: `#10b981`

### Typography
- **Sans**: Inter
- **Display**: Poppins

### Components
- Rounded corners: `2xl` (16px)
- Shadows: Custom dark shadows with glow effects
- Transitions: Smooth 200-300ms transitions

## 🛠️ Installation

1. **Install Dependencies**:
```bash
cd frontend
npm install
```

2. **Configure Environment**:
```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Run Development Server**:
```bash
npm run dev
```

4. **Open Browser**:
Navigate to http://localhost:3000

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js app directory
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Main page
│   │   └── globals.css        # Global styles
│   ├── components/            # React components
│   │   ├── Navbar.tsx         # Top navigation
│   │   ├── Sidebar.tsx        # Side navigation
│   │   ├── MessageBubble.tsx  # Chat message
│   │   ├── ChatInput.tsx      # Input with suggestions
│   │   └── UploadZone.tsx     # File upload
│   └── lib/                   # Utilities
│       ├── api.ts             # API client
│       └── utils.ts           # Helper functions
├── public/                    # Static assets
├── tailwind.config.js         # Tailwind configuration
├── tsconfig.json             # TypeScript config
└── package.json              # Dependencies
```

## 🔌 API Integration

The frontend is pre-configured to connect to the backend API:

### Chat API
```typescript
import { chatAPI } from '@/lib/api';

// Send message
const response = await chatAPI.sendMessage(
  'Summarize loan terms',
  'openai'
);

// Get sessions
const sessions = await chatAPI.getSessions();
```

### Document API
```typescript
import { documentAPI } from '@/lib/api';

// Upload document
const doc = await documentAPI.upload(file);

// Get all documents
const documents = await documentAPI.getAll();

// Search documents
const results = await documentAPI.search('payment terms');
```

## 🎯 Key Components

### Navbar
- Fixed top navigation
- Profile and settings icons
- Notification indicator

### Sidebar
- Collapsible navigation
- Active tab highlighting
- System status indicators

### Chat Interface
- Real-time message streaming
- Provider selection dropdown
- Smart suggestions panel
- Copy message functionality

### Upload Zone
- Drag-and-drop support
- Progress tracking
- File type validation
- Multi-file support

### Message Bubble
- User/AI differentiation
- Timestamp display
- Provider and token info
- Copy to clipboard

## 🎨 Customization

### Changing Colors

Edit `tailwind.config.js`:
```javascript
colors: {
  'accent': {
    teal: '#14b8a6',      // Primary accent
    emerald: '#10b981',   // Secondary accent
  }
}
```

### Adding New Tabs

1. Update `Sidebar.tsx`:
```typescript
const menuItems = [
  // ... existing items
  {
    id: 'analytics',
    label: 'Analytics',
    icon: BarChart,
    description: 'View Metrics',
  },
];
```

2. Add component in `page.tsx`:
```typescript
case 'analytics':
  return <AnalyticsView />;
```

## 🚀 Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## 📱 Responsive Breakpoints

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

All components are fully responsive and adapt to screen size.

## ⚡ Performance

- **Code Splitting**: Automatic with Next.js
- **Image Optimization**: Next.js Image component
- **CSS Purging**: Unused Tailwind classes removed
- **Lazy Loading**: Components loaded on demand
- **API Caching**: React Query integration ready

## 🔒 Security

- **Input Validation**: All user inputs sanitized
- **XSS Protection**: React's built-in protection
- **CSRF Tokens**: Ready for implementation
- **Auth Headers**: JWT token support included

## 🧪 Testing

```bash
# Run tests (when configured)
npm test

# Run linter
npm run lint
```

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `NEXT_PUBLIC_MAX_FILE_SIZE` | Max upload size | `52428800` (50MB) |
| `NEXT_PUBLIC_ENABLE_ANALYTICS` | Enable analytics | `true` |

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000

# Or use different port
npm run dev -- -p 3001
```

### API Connection Failed
1. Verify backend is running on port 8000
2. Check CORS settings in backend
3. Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### Styles Not Loading
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules
npm install
```

## 🤝 Contributing

1. Follow the existing code style
2. Use TypeScript for type safety
3. Add comments for complex logic
4. Test on multiple screen sizes
5. Ensure accessibility standards

## 📄 License

Same as the main project.

## 🎉 Ready to Use!

Your frontend is now ready to connect to the backend and provide a professional, responsive UI for the Loan Document Intelligence System.

**Start the dev server and begin building!**
```bash
npm run dev
```

Visit: http://localhost:3000
