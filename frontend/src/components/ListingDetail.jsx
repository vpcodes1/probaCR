import React, { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { api } from '../utils/api'

export default function ListingDetail({ user }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const [listing, setListing] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showMessageForm, setShowMessageForm] = useState(false)
  const [message, setMessage] = useState({ subject: '', message: '' })
  const [sendingMessage, setSendingMessage] = useState(false)

  useEffect(() => {
    fetchListing()
  }, [id])

  const fetchListing = async () => {
    setLoading(true)
    const data = await api.getListing(id)
    if (data.id) {
      setListing(data)
      setMessage(prev => ({ ...prev, subject: `Upit za: ${data.title}` }))
    } else {
      navigate('/listings')
    }
    setLoading(false)
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!user) {
      navigate('/login')
      return
    }

    setSendingMessage(true)
    const data = await api.sendMessage({
      receiver_id: listing.company_id,
      ...message
    })

    if (data.id) {
      alert('Poruka uspešno poslata!')
      setShowMessageForm(false)
      setMessage({ subject: `Upit za: ${listing.title}`, message: '' })
    } else {
      alert('Greška pri slanju poruke.')
    }
    setSendingMessage(false)
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Učitavanje...</p>
      </div>
    )
  }

  if (!listing) {
    return null
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <div className="mb-6 text-sm text-gray-600">
        <Link to="/" className="hover:text-indigo-600">Početna</Link>
        {' / '}
        <Link to="/listings" className="hover:text-indigo-600">Oglasi</Link>
        {' / '}
        <span className="text-gray-900">{listing.title}</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            {listing.image_url ? (
              <img src={listing.image_url} alt={listing.title} className="w-full h-96 object-cover" />
            ) : (
              <div className="w-full h-96 bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center">
                <span className="text-9xl">📦</span>
              </div>
            )}

            <div className="p-8">
              <div className="flex items-center justify-between mb-4">
                <span className="bg-indigo-100 text-indigo-800 text-sm font-semibold px-4 py-2 rounded-full">
                  {listing.category}
                </span>
                <span className="text-gray-500 text-sm">
                  {new Date(listing.created_at).toLocaleDateString('sr-RS')}
                </span>
              </div>

              <h1 className="text-4xl font-bold text-gray-900 mb-4">{listing.title}</h1>

              {listing.price_range && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
                  <div className="text-sm text-green-800 font-medium">Cena</div>
                  <div className="text-2xl font-bold text-green-900">{listing.price_range}</div>
                </div>
              )}

              <div className="prose max-w-none mb-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-3">Opis</h2>
                <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{listing.description}</p>
              </div>

              {listing.location && (
                <div className="flex items-center text-gray-600 mb-4">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span>{listing.location}</span>
                </div>
              )}

              <div className="flex items-center text-gray-600">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <span>{listing.views_count} pregleda</span>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1">
          {/* Company Info */}
          {listing.company && (
            <div className="bg-white rounded-xl shadow-md p-6 mb-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Kompanija</h3>
              {listing.company.logo_url && (
                <img src={listing.company.logo_url} alt={listing.company.company_name} className="w-full h-32 object-contain mb-4" />
              )}
              <div className="space-y-3">
                <div>
                  <div className="flex items-center">
                    <h4 className="text-lg font-semibold text-gray-900">{listing.company.company_name}</h4>
                    {listing.company.is_verified && (
                      <span className="ml-2 text-green-500" title="Verifikovana kompanija">✓</span>
                    )}
                  </div>
                  {listing.company.city && (
                    <p className="text-gray-600 text-sm">{listing.company.city}</p>
                  )}
                </div>

                {listing.company.description && (
                  <p className="text-gray-700 text-sm">{listing.company.description}</p>
                )}

                {listing.company.website && (
                  <a href={listing.company.website} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-700 text-sm flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                    Website
                  </a>
                )}

                {listing.company.phone && (
                  <a href={`tel:${listing.company.phone}`} className="text-indigo-600 hover:text-indigo-700 text-sm flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                    {listing.company.phone}
                  </a>
                )}
              </div>
            </div>
          )}

          {/* Contact Form */}
          {user && user.id !== listing.company_id ? (
            <div className="bg-white rounded-xl shadow-md p-6">
              {!showMessageForm ? (
                <button
                  onClick={() => setShowMessageForm(true)}
                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-lg transition"
                >
                  Pošalji Poruku
                </button>
              ) : (
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-4">Pošalji Poruku</h3>
                  <form onSubmit={handleSendMessage} className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Naslov</label>
                      <input
                        type="text"
                        value={message.subject}
                        onChange={(e) => setMessage(prev => ({ ...prev, subject: e.target.value }))}
                        required
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Poruka</label>
                      <textarea
                        value={message.message}
                        onChange={(e) => setMessage(prev => ({ ...prev, message: e.target.value }))}
                        required
                        rows="4"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                        placeholder="Vaša poruka..."
                      />
                    </div>
                    <div className="flex gap-2">
                      <button
                        type="submit"
                        disabled={sendingMessage}
                        className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition disabled:opacity-50"
                      >
                        {sendingMessage ? 'Slanje...' : 'Pošalji'}
                      </button>
                      <button
                        type="button"
                        onClick={() => setShowMessageForm(false)}
                        className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                      >
                        Otkaži
                      </button>
                    </div>
                  </form>
                </div>
              )}
            </div>
          ) : !user ? (
            <div className="bg-white rounded-xl shadow-md p-6">
              <p className="text-gray-700 mb-4">Prijavite se da biste kontaktirali kompaniju</p>
              <Link
                to="/login"
                className="block w-full bg-indigo-600 hover:bg-indigo-700 text-white text-center font-semibold py-3 px-4 rounded-lg transition"
              >
                Prijavi se
              </Link>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}
