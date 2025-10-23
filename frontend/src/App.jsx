import React, { useState } from 'react'
import Header from './components/Header'
import ReportForm from './components/ReportForm'
import ReportView from './components/ReportView'
import Hero from './components/Hero'

function App() {
  const [currentReport, setCurrentReport] = useState(null)
  const [showForm, setShowForm] = useState(false)

  const handleReportGenerated = (reportId) => {
    setCurrentReport(reportId)
    setShowForm(false)
  }

  const handleNewReport = () => {
    setCurrentReport(null)
    setShowForm(true)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header onNewReport={handleNewReport} />

      <main>
        {!showForm && !currentReport && (
          <Hero onGetStarted={() => setShowForm(true)} />
        )}

        {showForm && (
          <div className="max-w-4xl mx-auto px-4 py-12">
            <ReportForm onReportGenerated={handleReportGenerated} />
          </div>
        )}

        {currentReport && (
          <div className="max-w-6xl mx-auto px-4 py-12">
            <ReportView reportId={currentReport} />
          </div>
        )}
      </main>

      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <p className="text-center text-gray-600">
            &copy; 2024 YUSEARCH. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
