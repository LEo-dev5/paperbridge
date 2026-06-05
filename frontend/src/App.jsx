import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import ChatPage from './pages/ChatPage'
import BriefingPage from './pages/BriefingPage'
import SettingsPage from './pages/SettingsPage'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <nav className="navbar">
          <h1>📚 PaperBridge</h1>
          <div className="nav-links">
            <Link to="/">채팅</Link>
            <Link to="/briefing">브리핑</Link>
            <Link to="/settings">설정</Link>
          </div>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/briefing" element={<BriefingPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App