import { useState } from 'react'
import { chat } from '../services/api'
import ReactMarkdown from 'react-markdown'

function ChatPage() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage = input
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      const response = await chat(userMessage, sessionId)
      setSessionId(response.session_id)
      setMessages(prev => [...prev, { role: 'assistant', content: response.answer }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: '오류가 발생했습니다.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSend()
  }

  return (
    <div className="chat-page">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="message-content">
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        {loading && <div className="message assistant"><div className="message-content">생각 중...</div></div>}
      </div>
      <div className="chat-input">
        <input
          type="text"
          placeholder="논문에 대해 질문해보세요..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? '...' : '전송'}
        </button>
      </div>
    </div>
  )
}

export default ChatPage