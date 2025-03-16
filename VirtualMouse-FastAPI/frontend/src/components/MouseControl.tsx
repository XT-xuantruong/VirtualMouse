import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Button } from '@/components/ui/button';

const MouseControl: React.FC = () => {
  const [virtualMouseEnabled, setVirtualMouseEnabled] = useState<boolean>(true);
  const imgRef = useRef<HTMLImageElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const [wsConnected, setWsConnected] = useState<boolean>(false);

  const connectWebSocket = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) return;

    wsRef.current = new WebSocket('ws://localhost:8088/video_ws');

    wsRef.current.onopen = () => {
      console.log('WebSocket connected');
      setWsConnected(true);
    };

    wsRef.current.onmessage = (event) => {
      if (imgRef.current) {
        const blob = new Blob([event.data], { type: 'image/jpeg' });
        imgRef.current.src = URL.createObjectURL(blob);
      }
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setWsConnected(false);
    };

    wsRef.current.onclose = () => {
      console.log('WebSocket closed');
      setWsConnected(false);
      setTimeout(connectWebSocket, 1000); // Thử kết nối lại sau 1 giây
    };
  };

  useEffect(() => {
    connectWebSocket();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const toggleVirtualMouse = async () => {
    try {
      const response = await axios.post('http://localhost:8088/toggle_virtual_mouse');
      setVirtualMouseEnabled(response.data.enabled);
    } catch (error) {
      console.error('Error toggling Virtual Mouse:', error);
    }
  };

  return (
    <div className="text-center">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">Virtual Mouse Control</h1>
      <div className="max-w-2xl mx-auto">
        <img
          ref={imgRef}
          alt="Video Stream"
          className="w-full border-2 border-gray-300 rounded-lg shadow-lg"
        />
        <p className="mt-2">{wsConnected ? 'Connected' : 'Disconnected'}</p>
        <Button
          onClick={toggleVirtualMouse}
          className={`mt-4 ${virtualMouseEnabled ? 'bg-green-500 hover:bg-green-600' : 'bg-red-500 hover:bg-red-600'}`}
          disabled={!wsConnected}
        >
          {virtualMouseEnabled ? 'Turn OFF Virtual Mouse' : 'Turn ON Virtual Mouse'}
        </Button>
      </div>
    </div>
  );
};

export default MouseControl;