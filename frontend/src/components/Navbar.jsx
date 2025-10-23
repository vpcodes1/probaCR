import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../utils/api'

export default function Navbar({ user, onLogout }) {
  const navigate = useNavigate()
  const [unreadCount, setUnreadCount] = useState(0)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    if (user) {
      api.getUnreadCount().then(data => {
        if (data.unread_count !== undefined) {
          setUnreadCount(data.unread_count)
        }
      })
    }
  }, [user])

  const handleLogout = () => {
    onLogout()
    navigate('/')
  }

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">B2B</span>
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                B2B Hub
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <Link to="/listings" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
              Oglasi
            </Link>
            <Link to="/companies" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
              Kompanije
            </Link>

            {user ? (
              <>
                <Link to="/create-listing" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
                  Postavi Oglas
                </Link>
                <Link to="/my-listings" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
                  Moji Oglasi
                </Link>
                <Link to="/messages" className="relative text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
                  Poruke
                  {unreadCount > 0 && (
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                      {unreadCount}
                    </span>
                  )}
                </Link>
                <Link to="/profile" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
                  Profil
                </Link>
                <button
                  onClick={handleLogout}
                  className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition"
                >
                  Odjava
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
                  Prijava
                </Link>
                <Link to="/register" className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition">
                  Registracija
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-gray-700 hover:text-indigo-600"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <Link to="/listings" className="block text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 px-3 py-2 rounded-md text-base font-medium">
              Oglasi
            </Link>
            <Link to="/companies" className="block text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 px-3 py-2 rounded-md text-base font-medium">
              Kompanije
            </Link>

            {user ? (
              <>
                <Link to="/create-listing" className="block text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 px-3 py-2 rounded-md text-base font-medium">
                  Postavi Oglas
                </Link>
                <Link to="/my-listings" className="block text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 px-3 py-2 rounded-md text-base font-medium">
                  Moji Oglasi
                </Link>
                <Link to="/messages" className="block text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 px-3 py-2 rounded-md text-base font-medium">
                  Poruke {unreadCount > 0 && `(${unreadCount})`}
                </Link>
                <Link to="/profile" className="block text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 px-3 py-2 rounded-md text-base font-medium">
                  Profil
                </Link>
                <button
                  onClick={handleLogout}
                  className="block w-full text-left text-red-600 hover:bg-red-50 px-3 py-2 rounded-md text-base font-medium"
                >
                  Odjava
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="block text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 px-3 py-2 rounded-md text-base font-medium">
                  Prijava
                </Link>
                <Link to="/register" className="block bg-indigo-600 text-white hover:bg-indigo-700 px-3 py-2 rounded-md text-base font-medium">
                  Registracija
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}
