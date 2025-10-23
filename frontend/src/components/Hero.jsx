import React from 'react'

export default function Hero({ onGetStarted }) {
  return (
    <div className="bg-gradient-to-br from-primary-50 to-white">
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Stop Spending Hours Researching<br />
            Start Closing More Deals in Minutes
          </h1>

          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Get perfectly prepared for every client meeting with comprehensive prospect
            reports delivered under 5 minutes. Save your weekends, sound like an expert,
            and finally compete with bigger players.
          </p>

          <button
            onClick={onGetStarted}
            className="px-8 py-4 bg-primary-600 text-white text-lg font-semibold rounded-lg hover:bg-primary-700 transition-colors shadow-lg"
          >
            Start Your FREE Trial
          </button>

          <p className="text-sm text-gray-500 mt-4">
            No credit card required • 3 reports/month free
          </p>
        </div>

        <div className="mt-20 grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-primary-600 text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-bold mb-2">5-Minute Reports</h3>
            <p className="text-gray-600">
              Complete prospect analysis in under 5 minutes. What used to take 2+ hours
              is now instant.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-primary-600 text-4xl mb-4">🎯</div>
            <h3 className="text-xl font-bold mb-2">Perfect Talking Points</h3>
            <p className="text-gray-600">
              AI-generated conversation starters, personality insights, and recommended
              approaches for every meeting.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-primary-600 text-4xl mb-4">📈</div>
            <h3 className="text-xl font-bold mb-2">Close 30% More Deals</h3>
            <p className="text-gray-600">
              Walk into every meeting perfectly prepared with enterprise-quality
              intelligence at SMB prices.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
