"use client";

import { useEffect, useState } from "react";
import { AlertTriangle, BarChart3, Clock, LayoutDashboard, Search, ShieldCheck, Users } from "lucide-react";

export default function Dashboard() {
  const [stats, setStats] = useState({
    pending: 124,
    highRisk: 12,
    today: 450,
  });

  return (
    <div className="flex h-screen bg-slate-100">
      {/* Sidebar */}
      <div className="w-64 bg-slate-900 text-white p-6">
        <h1 className="text-xl font-bold mb-10 text-emerald-400">NCDIPS</h1>
        <nav className="space-y-4">
          <NavItem icon={<LayoutDashboard size={20} />} label="Overview" active />
          <NavItem icon={<AlertTriangle size={20} />} label="High-Risk Queue" />
          <NavItem icon={<Search size={20} />} label="Explorer" />
          <NavItem icon={<Users size={20} />} label="Entities" />
          <NavItem icon={<BarChart3 size={20} />} label="Valuation" />
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 bg-white border-b px-8 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Intelligence Overview</h2>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-slate-500">Welcome, Analyst</span>
            <div className="w-8 h-8 rounded-full bg-slate-200"></div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="flex-1 overflow-y-auto p-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <StatCard
              label="Declarations Today"
              value={stats.today.toString()}
              icon={<Clock className="text-blue-500" />}
            />
            <StatCard
              label="High Risk Flagged"
              value={stats.highRisk.toString()}
              icon={<AlertTriangle className="text-red-500" />}
            />
            <StatCard
              label="System Compliance"
              value="94.2%"
              icon={<ShieldCheck className="text-emerald-500" />}
            />
          </div>

          <div className="bg-white rounded-xl border p-6">
            <h3 className="text-lg font-semibold mb-6">Recent High-Risk Declarations</h3>
            <table className="w-full text-left">
              <thead>
                <tr className="text-slate-500 text-sm border-b">
                  <th className="pb-4">SGD ID</th>
                  <th className="pb-4">Importer</th>
                  <th className="pb-4">Score</th>
                  <th className="pb-4">Risk Level</th>
                  <th className="pb-4">Status</th>
                  <th className="pb-4">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                <tr className="text-sm">
                  <td className="py-4 font-mono">SGD-2023-X921</td>
                  <td className="py-4 font-medium">MULTI-BOND LTD</td>
                  <td className="py-4">84.5</td>
                  <td className="py-4"><span className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs font-bold">CRITICAL</span></td>
                  <td className="py-4">Flagged</td>
                  <td className="py-4"><button className="text-blue-600 hover:underline">Review</button></td>
                </tr>
                {/* More rows would be mapped here */}
              </tbody>
            </table>
          </div>
        </main>
      </div>
    </div>
  );
}

function NavItem({ icon, label, active = false }: { icon: any, label: string, active?: boolean }) {
  return (
    <div className={`flex items-center space-x-3 p-3 rounded-lg cursor-pointer transition ${active ? 'bg-emerald-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}>
      {icon}
      <span className="font-medium">{label}</span>
    </div>
  );
}

function StatCard({ label, value, icon }: { label: string, value: string, icon: any }) {
  return (
    <div className="bg-white p-6 rounded-xl border flex items-center justify-between">
      <div>
        <p className="text-sm text-slate-500 mb-1">{label}</p>
        <p className="text-2xl font-bold">{value}</p>
      </div>
      <div className="p-3 bg-slate-50 rounded-lg">{icon}</div>
    </div>
  );
}
