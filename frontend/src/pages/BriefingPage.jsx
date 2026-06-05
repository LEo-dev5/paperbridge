import { useState } from 'react'
import { runBriefing } from '../services/api'

function BriefingPage() {
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleBriefing = async () => {
    setLoading(true)
    setMessage('')
    try {
      const response = await runBriefing()
      setMessage(response.message)
    } catch (err) {
      setMessage('브리핑 실행 중 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="briefing-page">
      <h2>📚 논문 브리핑</h2>
      <p>최신 논문을 수집하고 디스코드로 브리핑을 전송합니다.</p>
      <button onClick={handleBriefing} disabled={loading} className="briefing-btn">
        {loading ? '브리핑 중...' : '브리핑 실행'}
      </button>
      {message && <p className="briefing-message">{message}</p>}
    </div>
  )
}

export default BriefingPage