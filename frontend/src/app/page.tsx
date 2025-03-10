'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [apiStatus, setApiStatus] = useState<'loading' | 'online' | 'offline'>('loading');
  
  useEffect(() => {
    // ตรวจสอบสถานะของ Backend API
    fetch('http://localhost:3001/')
      .then(response => {
        if (response.ok) {
          setApiStatus('online');
        } else {
          setApiStatus('offline');
        }
      })
      .catch(() => {
        setApiStatus('offline');
      });
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm flex flex-col">
        <h1 className="text-4xl font-bold mb-8">FaceSocial</h1>
        <p className="text-xl mb-6">แพลตฟอร์มโซเชียลมีเดียด้วยเทคโนโลยีจดจำใบหน้า</p>
        
        <div className="flex flex-col gap-4 items-center">
          <div className="flex items-center gap-2">
            <span>API Status:</span>
            <span 
              className={`inline-block w-3 h-3 rounded-full ${
                apiStatus === 'online' 
                  ? 'bg-green-500' 
                  : apiStatus === 'offline' 
                  ? 'bg-red-500' 
                  : 'bg-yellow-500'
              }`}
            />
            <span>
              {apiStatus === 'online' 
                ? 'Backend API พร้อมใช้งาน' 
                : apiStatus === 'offline' 
                ? 'Backend API ไม่พร้อมใช้งาน' 
                : 'กำลังตรวจสอบ...'}
            </span>
          </div>
        </div>
        
        <div className="mt-10 flex flex-col gap-4">
          <Link 
            href="/login" 
            className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-center"
          >
            เข้าสู่ระบบ
          </Link>
          <Link 
            href="/register" 
            className="px-6 py-3 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 transition-colors text-center"
          >
            สมัครสมาชิก
          </Link>
        </div>
      </div>
    </main>
  );
}