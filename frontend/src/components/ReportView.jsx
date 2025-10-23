import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function ReportView({ reportId }) {
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let interval

    const fetchReport = async () => {
      try {
        const response = await axios.get(`/api/reports/${reportId}`)
        const data = response.data

        if (data.status === 'completed') {
          setReport(data)
          setLoading(false)
          if (interval) clearInterval(interval)
        } else if (data.status === 'failed') {
          setError(data.error_message || 'Report generation failed')
          setLoading(false)
          if (interval) clearInterval(interval)
        }
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to fetch report')
        setLoading(false)
        if (interval) clearInterval(interval)
      }
    }

    // Initial fetch
    fetchReport()

    // Poll every 5 seconds until complete
    interval = setInterval(fetchReport, 5000)

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [reportId])

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-12 text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
        <h3 className="text-xl font-semibold mb-2">Generating Your Report...</h3>
        <p className="text-gray-600">
          This typically takes 3-5 minutes. We're researching the prospect,
          analyzing data, and generating personalized insights.
        </p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-red-900 mb-2">Error</h3>
        <p className="text-red-700">{error}</p>
      </div>
    )
  }

  if (!report || !report.data) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
        <p className="text-gray-700">No report data available</p>
      </div>
    )
  }

  const { data } = report

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          {report.prospect_name}
        </h1>
        <p className="text-xl text-gray-600">{report.company_name}</p>

        {/* Export Buttons */}
        <div className="mt-6 flex space-x-4">
          <a
            href={`/${report.pdf_path}`}
            download
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Download PDF
          </a>
          <a
            href={`/${report.docx_path}`}
            download
            className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Download Word
          </a>
        </div>
      </div>

      {/* Executive Summary */}
      {data.executive_summary && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Executive Summary</h2>
          <p className="text-gray-700 leading-relaxed">{data.executive_summary}</p>
        </div>
      )}

      {/* Quick Facts */}
      {data.quick_facts && Object.keys(data.quick_facts).length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Facts</h2>
          <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(data.quick_facts).map(([key, value]) => (
              <div key={key} className="border-b pb-2">
                <dt className="font-semibold text-gray-700">{key}</dt>
                <dd className="text-gray-600">{value}</dd>
              </div>
            ))}
          </dl>
        </div>
      )}

      {/* Conversation Starters */}
      {data.conversation_starters && data.conversation_starters.length > 0 && (
        <div className="bg-primary-50 rounded-lg shadow-md p-6 border-2 border-primary-200">
          <h2 className="text-2xl font-bold text-primary-900 mb-4">
            🎯 Conversation Starters
          </h2>
          <ul className="space-y-3">
            {data.conversation_starters.map((starter, index) => (
              <li key={index} className="flex items-start">
                <span className="text-primary-600 mr-2">•</span>
                <span className="text-gray-700">{starter}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Talking Points */}
      {data.talking_points && data.talking_points.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Perfect Talking Points</h2>
          <ol className="space-y-3">
            {data.talking_points.map((point, index) => (
              <li key={index} className="flex items-start">
                <span className="font-bold text-primary-600 mr-3">{index + 1}.</span>
                <span className="text-gray-700">{point}</span>
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* Personality Analysis */}
      {data.personality_analysis && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Personality Insights</h2>
          <div className="prose max-w-none text-gray-700 whitespace-pre-line">
            {data.personality_analysis}
          </div>
        </div>
      )}

      {/* Recommended Approach */}
      {data.recommended_approach && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Recommended Approach</h2>
          <div className="prose max-w-none text-gray-700 whitespace-pre-line">
            {data.recommended_approach}
          </div>
        </div>
      )}

      {/* Company Background */}
      {data.company_data && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Company Background</h2>

          {data.company_data.description && (
            <p className="text-gray-700 mb-4">{data.company_data.description}</p>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            {data.company_data.industry && (
              <div>
                <span className="font-semibold">Industry:</span> {data.company_data.industry}
              </div>
            )}
            {data.company_data.size && (
              <div>
                <span className="font-semibold">Size:</span> {data.company_data.size}
              </div>
            )}
            {data.company_data.website && (
              <div>
                <span className="font-semibold">Website:</span>{' '}
                <a
                  href={data.company_data.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary-600 hover:underline"
                >
                  {data.company_data.website}
                </a>
              </div>
            )}
          </div>

          {data.company_data.funding && (
            <div className="mt-4 p-4 bg-gray-50 rounded">
              <span className="font-semibold">Funding:</span> {data.company_data.funding}
            </div>
          )}
        </div>
      )}

      {/* Recent News */}
      {data.news_data && data.news_data.company_news && data.news_data.company_news.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Recent News & Events</h2>
          <div className="space-y-4">
            {data.news_data.company_news.slice(0, 5).map((news, index) => (
              <div key={index} className="border-b pb-4 last:border-b-0">
                <h3 className="font-semibold text-gray-900 mb-1">{news.title}</h3>
                <p className="text-gray-600 text-sm mb-2">{news.snippet}</p>
                <a
                  href={news.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary-600 hover:underline text-sm"
                >
                  Read more →
                </a>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
