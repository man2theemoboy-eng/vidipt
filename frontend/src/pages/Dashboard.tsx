import React from 'react';
import { Link } from 'react-router-dom';
import { Video, ArrowRight, Zap, Image, Music } from 'lucide-react';

export default function Dashboard() {
  const features = [
    {
      icon: Video,
      title: 'AI Video Generation',
      description: 'Convert scripts to professional videos with AI narration'
    },
    {
      icon: Image,
      title: 'Multi-Format Support',
      description: 'Upload images, GIFs, videos, and screenshots'
    },
    {
      icon: Zap,
      title: 'Effects & Animation',
      description: 'Professional effects, animations, and VFX'
    },
    {
      icon: Music,
      title: 'Copyright-Free Music',
      description: 'Extensive library of royalty-free background music'
    }
  ];

  return (
    <div className="pt-20 pb-20">
      <section className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
          Transform Your Ideas Into
          <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent"> Amazing Videos</span>
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
          Create professional AI-generated videos with multilingual support, animation effects, and copyright-free music. Completely free for personal use.
        </p>
        <Link
          to="/editor"
          className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-bold rounded-lg hover:shadow-lg hover:shadow-purple-500/50 transition"
        >
          Start Creating Now
          <ArrowRight size={20} />
        </Link>
      </section>

      <section className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-4xl font-bold text-white text-center mb-12">Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, idx) => (
            <div key={idx} className="bg-slate-800 rounded-lg p-6 border border-purple-500/20 hover:border-purple-500/50 transition">
              <feature.icon className="text-purple-400 mb-4" size={32} />
              <h3 className="text-lg font-bold text-white mb-2">{feature.title}</h3>
              <p className="text-gray-400 text-sm">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
