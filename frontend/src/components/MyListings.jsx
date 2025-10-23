import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../utils/api'

export default function MyListings() {
  const [listings, setListings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMyListings()
  }, [])

  const fetchMyListings = async () => {
    setLoading(true)
    const data = await api.getMyListings()
    if (data.listings) {
      setListings(data.listings)
    }
    setLoading(false)
  }

  const handleDelete = async (id) => {
    if (!confirm('Da li ste sigurni da želite da obrišete ovaj oglas?')) {
      return
    }

    const response = await api.deleteListing(id)
    if (response.message) {
      alert('Oglas uspešno obrisan!')
      fetchMyListings()
    } else {
      alert('Greška pri brisanju oglasa.')
    }
  }

  const toggleActive = async (id, currentStatus) => {
    const response = await api.updateListing(id, { is_active: !currentStatus })
    if (response.id) {
      fetchMyListings()
    } else {
      alert('Greška pri ažuriranju oglasa.')
    }
  }

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Učitavanje...</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Moji Oglasi</h1>
          <p className="text-gray-600">Upravljajte vašim oglasima</p>
        </div>
        <Link
          to="/create-listing"
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-semibold transition"
        >
          + Novi Oglas
        </Link>
      </div>

      {listings.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-12 text-center">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Nemate oglasa</h3>
          <p className="text-gray-600 mb-6">Kreirajte svoj prvi oglas i počnite da privlačite klijente</p>
          <Link
            to="/create-listing"
            className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-semibold transition"
          >
            Kreiraj Oglas
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {listings.map(listing => (
            <div key={listing.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition">
              <div className="flex flex-col md:flex-row">
                {/* Image */}
                <div className="md:w-48 h-48 flex-shrink-0">
                  {listing.image_url ? (
                    <img src={listing.image_url} alt={listing.title} className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center">
                      <span className="text-5xl">📦</span>
                    </div>
                  )}
                </div>

                {/* Content */}
                <div className="flex-1 p-6">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="bg-indigo-100 text-indigo-800 text-xs font-semibold px-3 py-1 rounded-full">
                          {listing.category}
                        </span>
                        <span className={`text-xs font-semibold px-3 py-1 rounded-full ${
                          listing.is_active
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {listing.is_active ? 'Aktivan' : 'Neaktivan'}
                        </span>
                      </div>
                      <h3 className="text-xl font-bold text-gray-900 mb-2">{listing.title}</h3>
                      <p className="text-gray-600 text-sm line-clamp-2 mb-3">{listing.description}</p>
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span>👁 {listing.views_count} pregleda</span>
                        <span>📅 {new Date(listing.created_at).toLocaleDateString('sr-RS')}</span>
                        {listing.price_range && <span>💰 {listing.price_range}</span>}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="p-6 border-t md:border-t-0 md:border-l flex md:flex-col gap-2 justify-end">
                  <Link
                    to={`/listings/${listing.id}`}
                    className="px-4 py-2 text-indigo-600 hover:bg-indigo-50 rounded-lg text-sm font-medium transition text-center"
                  >
                    Pregledaj
                  </Link>
                  <button
                    onClick={() => toggleActive(listing.id, listing.is_active)}
                    className="px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg text-sm font-medium transition"
                  >
                    {listing.is_active ? 'Deaktiviraj' : 'Aktiviraj'}
                  </button>
                  <button
                    onClick={() => handleDelete(listing.id)}
                    className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg text-sm font-medium transition"
                  >
                    Obriši
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
