import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from '@/components/ui/button';

const MouseControl: React.FC = () => {
  const [virtualMouseEnabled, setVirtualMouseEnabled] = useState<boolean>(true);

  const toggleVirtualMouse = async () => {
    try {
      const response = await axios.post('http://localhost:8088/toggle_virtual_mouse');
      setVirtualMouseEnabled(response.data.enabled);
    } catch (error) {
      console.error('Error toggling Virtual Mouse:', error);
    }
  };

  useEffect(() => {
    setVirtualMouseEnabled(true); // Trạng thái mặc định
  }, []);

  return (
    <div className="text-center">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">Virtual Mouse Control</h1>
      <div className="max-w-2xl mx-auto">
        <img
          src="http://localhost:8088/video_feed"
          alt="Video Stream"
          className="w-full border-2 border-gray-300 rounded-lg shadow-lg"
        />
        <Button
          onClick={toggleVirtualMouse}
          className={`mt-4 ${virtualMouseEnabled ? 'bg-green-500 hover:bg-green-600' : 'bg-red-500 hover:bg-red-600'}`}
        >
          {virtualMouseEnabled ? 'Turn OFF Virtual Mouse' : 'Turn ON Virtual Mouse'}
        </Button>
      </div>
    </div>
  );
};

export default MouseControl;