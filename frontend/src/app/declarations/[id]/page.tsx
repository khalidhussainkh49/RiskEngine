"use client";

import { useParams } from "next/navigation";
import { AlertCircle, ArrowLeft, Container, FileText, Info, TrendingDown } from "lucide-react";

export default function DeclarationDetails() {
  const params = useParams();
  const id = params.id;

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-6xl mx-auto">
        <button className="flex items-center text-slate-500 hover:text-slate-800 mb-6">
          <ArrowLeft size={18} className="mr-2" />
          Back to Queue
        </button>

        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Declaration SGD-2023-X921</h1>
            <p className="text-slate-500">Processed on Nov 20, 2026 • Office: Tincan Island Port</p>
          </div>
          <div className="flex space-x-4">
            <div className="bg-red-50 border border-red-200 p-4 rounded-lg text-center">
              <p className="text-xs text-red-600 font-bold uppercase tracking-wider mb-1">Risk Score</p>
              <p className="text-3xl font-black text-red-700">84.5</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Details & Items */}
          <div className="lg:col-span-2 space-y-8">
            <section className="bg-white rounded-xl border p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <FileText size={20} className="mr-2 text-slate-400" />
                Declaration Metadata
              </h3>
              <div className="grid grid-cols-2 gap-6 text-sm">
                <div>
                  <p className="text-slate-500 mb-1">Importer</p>
                  <p className="font-medium">MULTI-BOND LTD (RC123456)</p>
                </div>
                <div>
                  <p className="text-slate-500 mb-1">Exporter</p>
                  <p className="font-medium">GLOBAL LOGISTICS GMBH</p>
                </div>
                <div>
                  <p className="text-slate-500 mb-1">Total CIF Value</p>
                  <p className="font-medium">NGN 45,230,000.00</p>
                </div>
                <div>
                  <p className="text-slate-500 mb-1">Bank</p>
                  <p className="font-medium">ACCESS BANK PLC</p>
                </div>
              </div>
            </section>

            <section className="bg-white rounded-xl border p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Container size={20} className="mr-2 text-slate-400" />
                Goods & Items
              </h3>
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-slate-500 border-b">
                    <th className="pb-3 text-left">HS Code</th>
                    <th className="pb-3 text-left">Description</th>
                    <th className="pb-3 text-right">Value</th>
                    <th className="pb-3 text-right">Weight</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  <tr>
                    <td className="py-3 font-mono">8703.23.00</td>
                    <td className="py-3">USED TOYOTA CAMRY 2018</td>
                    <td className="py-3 text-right">NGN 8,500,000</td>
                    <td className="py-3 text-right">1,600 kg</td>
                  </tr>
                </tbody>
              </table>
            </section>
          </div>

          {/* Right Column: Risk Findings & Intelligence */}
          <div className="space-y-8">
            <section className="bg-white rounded-xl border border-red-100 p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center text-red-700">
                <AlertCircle size={20} className="mr-2" />
                Risk Intelligence
              </h3>
              <div className="space-y-4">
                <RiskFinding
                  title="Undervaluation Suspected"
                  description="Unit price is 42% below historical average for this HS code."
                  severity="high"
                />
                <RiskFinding
                  title="Weight Anomaly"
                  description="Declared weight per unit is inconsistent with cargo type."
                  severity="medium"
                />
              </div>
            </section>

            <section className="bg-slate-900 text-white rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <TrendingDown size={20} className="mr-2 text-emerald-400" />
                Historical Pattern
              </h3>
              <p className="text-sm text-slate-400 mb-4">
                Importer has 4 prior flags in the last 12 months related to HS code 8703.
              </p>
              <div className="h-32 bg-slate-800 rounded flex items-end p-4 space-x-2">
                 <div className="flex-1 bg-emerald-500 h-[20%]"></div>
                 <div className="flex-1 bg-emerald-500 h-[35%]"></div>
                 <div className="flex-1 bg-red-500 h-[85%]"></div>
                 <div className="flex-1 bg-emerald-500 h-[25%]"></div>
                 <div className="flex-1 bg-red-500 h-[95%]"></div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}

function RiskFinding({ title, description, severity }: { title: string, description: string, severity: 'high' | 'medium' | 'low' }) {
  return (
    <div className={`p-4 rounded-lg border-l-4 ${severity === 'high' ? 'bg-red-50 border-red-500' : 'bg-orange-50 border-orange-500'}`}>
      <h4 className="font-bold text-sm mb-1">{title}</h4>
      <p className="text-xs text-slate-600 leading-relaxed">{description}</p>
    </div>
  );
}
