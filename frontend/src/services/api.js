import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

// Agent 채팅
export const chat = async (query, sessionId = null) => {
    const response = await axios.post(`${BASE_URL}/agent/chat`, {
        query,
        session_id: sessionId
    });
    return response.data;
};

// 브리핑 수동 실행
export const runBriefing = async () => {
    const response = await axios.post(`${BASE_URL}/papers/briefing`);
    return response.data;
};

// 논문 수집
export const fetchPapers = async () => {
    const response = await axios.post(`${BASE_URL}/papers/fetch`);
    return response.data;
};