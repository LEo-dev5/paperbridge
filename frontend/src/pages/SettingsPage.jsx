import { useState, useEffect } from 'react'
import axios from 'axios'

function SettingsPage() {
  const [categories, setCategories] = useState('')
  const [keywords, setKeywords] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    axios.get('http://localhost:8000/settings/')
      .then(res => {
        setCategories(res.data.categories.join(', '))
        setKeywords(res.data.keywords.join(', '))
      })
  }, [])

  const handleSave = async () => {
    try {
      await axios.post('http://localhost:8000/settings/update', {
        categories: categories.split(',').map(c => c.trim()),
        keywords: keywords.split(',').map(k => k.trim())
      })
      setMessage('설정이 저장됐습니다.')
    } catch (err) {
      setMessage('저장 중 오류가 발생했습니다.')
    }
  }

  return (
    <div className="settings-page">
      <h2>⚙️ 설정</h2>
      <div className="setting-item">
        <label>카테고리 (쉼표로 구분)</label>
        <input
          type="text"
          value={categories}
          onChange={(e) => setCategories(e.target.value)}
          placeholder="cs.RO, cs.CV"
        />
        <p className="setting-hint">예: cs.RO (로보틱스), cs.CV (컴퓨터비전), cs.AI (AI)</p>
      </div>
      <div className="setting-item">
        <label>키워드 (쉼표로 구분)</label>
        <input
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          placeholder="SLAM, LiDAR"
        />
      </div>
      <button onClick={handleSave} className="briefing-btn">저장</button>
      {message && <p className="briefing-message">{message}</p>}
    </div>
  )
}

export default SettingsPage