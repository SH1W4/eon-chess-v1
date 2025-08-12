import { useEffect, useRef, useState } from 'react';
import { API_BASE, getToken } from '../services/api';

export function useRealtime(gameId: string) {
  const wsRef = useRef<WebSocket | null>(null);
  const [messages, setMessages] = useState<string[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const token = getToken();
    if (!token) return;

    // Use header Authorization via subprotocol is unreliable in browsers; we'll send auth message first
    const wsUrl = `${API_BASE.replace('http', 'ws')}/ws/${gameId}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
      ws.send(JSON.stringify({ type: 'auth', token }));
    };
    ws.onmessage = (ev) => setMessages((prev) => [...prev, ev.data]);
    ws.onclose = () => setConnected(false);
    ws.onerror = () => setConnected(false);

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [gameId]);

  const send = (payload: any) => {
    if (!wsRef.current) return;
    wsRef.current.send(JSON.stringify(payload));
  };

  return { connected, messages, send };
}
