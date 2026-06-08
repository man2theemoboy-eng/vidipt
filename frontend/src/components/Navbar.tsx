import React from 'react';
import { Link } from 'react-router-dom';
import { Video } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 bg-slate-900/80 backdrop-blur border-b border-purple-500/20 z-50">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 text-2xl font-bold text-white hover:text-purple-400 transition">
          <Video className="text-purple-500" size={28} />
          vidipt
        </Link>
        <div className="flex items-center gap-6">
          <Link to="/" className="text-gray-300 hover:text-white transition text-sm font-medium">
            Home
          </Link>
          <Link to="/editor" className="text-gray-300 hover:text-white transition text-sm font-medium">
            Editor
          </Link>
        </div>
      </div>
    </nav>
  );
}
