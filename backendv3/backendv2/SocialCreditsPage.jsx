import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SocialCreditForm = () => {
  const [socialData, setSocialData] = useState({
    email: '',
    instagram: {
      handle: '',
      followers: '',
      posts: '',
      engagementRate: '',
      accountAge: '',
      businessAccount: false,
      niche: ''
    },
    linkedin: {
      connections: '',
      experience: '',
      education: '',
      certifications: '',
      endorsements: '',
      posts: ''
    },
    youtube: {
      subscribers: '',
      videos: '',
      views: '',
      channelAge: '',
      niche: ''
    }
  });
  
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch('http://127.0.0.1:5000/api/social-credit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(socialData)
      });
      
      const data = await response.json();
      navigate('http://127.0.0.1:5000/credit-report', { state: { report: data }});
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (platform, field, value) => {
    setSocialData(prev => ({
      ...prev,
      [platform]: {
        ...prev[platform],
        [field]: value
      }
    }));
  };

  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-800 py-24">
      <div className="container mx-auto text-center px-4">
        <h1 className="text-5xl font-extrabold text-white mb-6 leading-tight">
          Social Credit <span className="text-yellow-400">Assessment</span>
        </h1>
        <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
          Share your social media presence details to enhance your loan application
        </p>

        <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
          <div className="bg-white bg-opacity-10 p-6 rounded-lg mb-6">
            <input
              type="email"
              placeholder="Email Address"
              className="w-full px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100 mb-4"
              value={socialData.email}
              onChange={(e) => setSocialData({...socialData, email: e.target.value})}
            />
          </div>

          {/* Instagram Section */}
          <div className="bg-white bg-opacity-10 p-6 rounded-lg mb-6">
            <h3 className="text-2xl font-bold text-white mb-4">Instagram Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <input
                type="number"
                placeholder="Followers Count"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.instagram.followers}
                onChange={(e) => handleChange('instagram', 'followers', e.target.value)}
              />
              <input
                type="number"
                placeholder="Number of Posts"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.instagram.posts}
                onChange={(e) => handleChange('instagram', 'posts', e.target.value)}
              />
              <input
                type="text"
                placeholder="Engagement Rate (%)"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.instagram.engagementRate}
                onChange={(e) => handleChange('instagram', 'engagementRate', e.target.value)}
              />
              <input
                type="text"
                placeholder="Account Age (years)"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.instagram.accountAge}
                onChange={(e) => handleChange('instagram', 'accountAge', e.target.value)}
              />
              <input
                type="text"
                placeholder="Instagram Handle"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100 col-span-2"
                value={socialData.instagram.handle}
                onChange={(e) => handleChange('instagram', 'handle', e.target.value)}
                />

            </div>
          </div>

          {/* LinkedIn Section */}
          <div className="bg-white bg-opacity-10 p-6 rounded-lg mb-6">
            <h3 className="text-2xl font-bold text-white mb-4">LinkedIn Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <input
                type="number"
                placeholder="Connection Count"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.linkedin.connections}
                onChange={(e) => handleChange('linkedin', 'connections', e.target.value)}
              />
              <input
                type="text"
                placeholder="Years of Experience"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.linkedin.experience}
                onChange={(e) => handleChange('linkedin', 'experience', e.target.value)}
              />
              <input
                type="text"
                placeholder="Education Level"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.linkedin.education}
                onChange={(e) => handleChange('linkedin', 'education', e.target.value)}
              />
              <input
                type="number"
                placeholder="Number of Endorsements"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.linkedin.endorsements}
                onChange={(e) => handleChange('linkedin', 'endorsements', e.target.value)}
              />
            </div>
          </div>

          {/* YouTube Section */}
          <div className="bg-white bg-opacity-10 p-6 rounded-lg mb-6">
            <h3 className="text-2xl font-bold text-white mb-4">YouTube Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <input
                type="number"
                placeholder="Subscriber Count"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.youtube.subscribers}
                onChange={(e) => handleChange('youtube', 'subscribers', e.target.value)}
              />
              <input
                type="number"
                placeholder="Total Videos"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.youtube.videos}
                onChange={(e) => handleChange('youtube', 'videos', e.target.value)}
              />
              <input
                type="number"
                placeholder="Total Views"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.youtube.views}
                onChange={(e) => handleChange('youtube', 'views', e.target.value)}
              />
              <input
                type="text"
                placeholder="Channel Age (years)"
                className="px-4 py-3 rounded-lg bg-white bg-opacity-20 text-white placeholder-blue-100"
                value={socialData.youtube.channelAge}
                onChange={(e) => handleChange('youtube', 'channelAge', e.target.value)}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-yellow-400 text-blue-900 px-8 py-3 rounded-full font-bold hover:bg-yellow-300 transition duration-300"
          >
            {loading ? 'Analyzing...' : 'Generate Social Credit Report'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default SocialCreditForm;
