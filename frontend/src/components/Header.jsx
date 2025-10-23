import React from 'react'

export default function Header({ onNewReport }) {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-xl">Y</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">YUSEARCH</h1>
        </div>

        <nav className="flex items-center space-x-4">
          <button
            onClick={onNewReport}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            New Report
          </button>
        </nav>
      </div>
    </header>
  )
}
