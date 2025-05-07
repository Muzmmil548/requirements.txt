import React from "react"; import { Card, CardContent } from "@/components/ui/card"; import { Button } from "@/components/ui/button"; import { Moon, Signal, LayoutGrid, LineChart, PanelLeft } from "lucide-react";

export default function UrduScalpingChecklistApp() { return ( <div className="bg-black text-white min-h-screen p-4"> <header className="flex justify-between items-center border-b border-gray-800 pb-2 mb-4"> <h1 className="text-2xl font-bold">Urdu Scalping Checklist App</h1> <div className="flex gap-4 items-center"> <Moon /> <span>Top s</span> <Signal /> <span>AI Signass</span> <Signal /> <span>AI Signals</span> <LayoutGrid /> <span>Patterns</span> </div> </header>

<div className="flex">
    <aside className="w-1/5 space-y-4 border-r border-gray-800 pr-4">
      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <PanelLeft /> <span>Live</span>
        </div>
        <div className="flex items-center gap-2">
          <LineChart /> <span>Chart</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-lg">🕒</span> <span>Top 50</span>
        </div>
        <div className="flex items-center gap-2">
          <Signal /> <span>AI Signals</span>
        </div>
      </div>
    </aside>

    <main className="w-4/5 pl-4">
      <Card className="bg-gray-900 mb-4">
        <CardContent>
          <h2 className="text-xl mb-2">Live Chart</h2>
          <div className="bg-black h-64 flex justify-center items-center border border-gray-700">
            <span className="text-gray-500">[Chart Placeholder]</span>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-3 gap-4">
        <Card className="bg-gray-900">
          <CardContent>
            <h3 className="text-lg mb-2">Coin Selector</h3>
            <select className="bg-gray-800 text-white p-2 rounded w-full">
              <option>TOP 10</option>
              <option>TOP 50</option>
            </select>
          </CardContent>
        </Card>

        <Card className="bg-gray-900">
          <CardContent>
            <h3 className="text-lg mb-2">AI Assistant Signals</h3>
            <ul className="space-y-2">
              <li className="flex items-center gap-2"><span className="w-3 h-3 bg-green-500 rounded-full"></span> Buy</li>
              <li className="flex items-center gap-2"><span className="w-3 h-3 bg-yellow-500 rounded-full"></span> Hold</li>
              <li className="flex items-center gap-2"><span className="w-3 h-3 bg-red-500 rounded-full"></span> Sell</li>
            </ul>
          </CardContent>
        </Card>

        <Card className="bg-gray-900">
          <CardContent>
            <h3 className="text-lg mb-2">Chart Patterns</h3>
            <ul className="space-y-2">
              <li className="flex items-center gap-2"><span className="w-3 h-3 bg-green-500 rounded-full"></span> Head & Shoulders</li>
              <li className="flex items-center gap-2"><span className="w-3 h-3 bg-green-500 rounded-full"></span> Triangle</li>
              <li className="flex items-center gap-2"><span className="w-3 h-3 bg-green-500 rounded-full"></span> Double Top</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </main>
  </div>
</div>

); }

