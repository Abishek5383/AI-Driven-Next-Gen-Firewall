import React, { useState, useEffect } from 'react';
import { Activity, ShieldAlert, ShieldCheck, History } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const mockData = [
  { time: '10:00', traffic: 400, threats: 2 },
  { time: '10:05', traffic: 300, threats: 1 },
  { time: '10:10', traffic: 550, threats: 0 },
  { time: '10:15', traffic: 900, threats: 15 },
  { time: '10:20', traffic: 450, threats: 3 }
];

export default function App() {
  const [stats, setStats] = useState({
    total_traffic_gb: 1.5,
    active_threats: 2,
    blocked_ips: 12,
    system_health: 99.2
  });
  const [threats, setThreats] = useState([]);

  useEffect(() => {
    // Simulating API fetch
    const fetchStats = () => {
        setThreats([
            { id: 1, ip: '192.168.1.5', type: 'High Risk Anomaly', score: 0.95, action: 'blocked' },
            { id: 2, ip: '10.0.0.22', type: 'Suspicious Traffic', score: 0.65, action: 'quarantined' },
        ]);
    };
    fetchStats();
  }, []);

  return (
    <div className="min-h-screen p-8 bg-gray-900 text-gray-100 font-sans">
      <header className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
            Next-Gen AI Firewall
          </h1>
          <p className="text-gray-400 mt-2">Zero Trust & Dynamic Threat Detection</p>
        </div>
        <div className="flex items-center space-x-2 bg-gray-800 px-4 py-2 rounded-lg border border-gray-700">
          <ShieldCheck className="text-emerald-400 w-6 h-6" />
          <span className="font-semibold text-emerald-400">System Healthy</span>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {[
          { label: 'Total Traffic', value: `${stats.total_traffic_gb} GB`, icon: Activity, color: 'text-blue-400' },
          { label: 'Active Threats', value: stats.active_threats, icon: ShieldAlert, color: 'text-rose-400' },
          { label: 'Blocked IPs', value: stats.blocked_ips, icon: ShieldAlert, color: 'text-orange-400' },
          { label: 'Health Score', value: `${stats.system_health}%`, icon: ShieldCheck, color: 'text-emerald-400' },
        ].map((stat, i) => (
          <div key={i} className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-lg">
            <div className="flex justify-between items-start mb-4">
              <div className={`p-3 rounded-lg bg-gray-900/50 ${stat.color}`}>
                <stat.icon className="w-6 h-6" />
              </div>
            </div>
            <h3 className="text-gray-400 text-sm font-medium">{stat.label}</h3>
            <p className="text-2xl font-bold mt-1">{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-lg">
          <h2 className="text-xl font-bold mb-6 flex items-center">
            <Activity className="w-5 h-5 mr-2 text-blue-400" />
            Live Network Traffic
          </h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="time" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '0.5rem' }}
                  itemStyle={{ color: '#E5E7EB' }}
                />
                <Line type="monotone" dataKey="traffic" stroke="#3B82F6" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="threats" stroke="#F43F5E" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-lg">
          <h2 className="text-xl font-bold mb-6 flex items-center">
            <History className="w-5 h-5 mr-2 text-rose-400" />
            Recent Threats
          </h2>
          <div className="space-y-4">
            {threats.map((threat) => (
              <div key={threat.id} className="bg-gray-900/50 rounded-lg p-4 border border-gray-700/50">
                <div className="flex justify-between items-start mb-2">
                  <span className="font-mono text-sm text-red-400">{threat.ip}</span>
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                    threat.action === 'blocked' ? 'bg-rose-500/20 text-rose-400' : 'bg-orange-500/20 text-orange-400'
                  }`}>
                    {threat.action.toUpperCase()}
                  </span>
                </div>
                <p className="text-sm font-medium text-gray-300 mb-1">{threat.type}</p>
                <div className="flex justify-between items-center text-xs text-gray-500">
                  <span>Score: {(threat.score * 100).toFixed(1)}%</span>
                  <span>Just now</span>
                </div>
              </div>
            ))}
            {threats.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                No recent threats detected
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
