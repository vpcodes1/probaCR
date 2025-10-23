import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../utils/api'

export default function Home({ user }) {
  const [featuredListings, setFeaturedListings] = useState([])
  const [categories, setCategories] = useState([])
  const [stats, setStats] = useState({ listings: 0, companies: 0 })

  useEffect(() => {
    // Fetch featured listings
    api.getListings({ per_page: 6 }).then(data => {
      if (data.listings) {
        setFeaturedListings(data.listings)
        setStats(prev => ({ ...prev, listings: data.total }))
      }
    })

    // Fetch categories
    api.getCategories().then(data => {
      if (data.categories) {
        setCategories(data.categories)
      }
    })

    // Fetch companies count
    api.getCompanies({ per_page: 1 }).then(data => {
      if (data.total !== undefined) {
        setStats(prev => ({ ...prev, companies: data.total }))
      }
    })
  }, [])

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Dobrodošli na B2B Hub
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-indigo-100">
              Platforma koja povezuje firme - Pronađite transportere, dobavljače i poslovne partnere
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link
                to="/listings"
                className="bg-white text-indigo-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-50 transition shadow-lg"
              >
                Pregledaj Oglase
              </Link>
              {!user && (
                <Link
                  to="/register"
                  className="bg-indigo-800 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-900 transition shadow-lg"
                >
                  Registruj se
                </Link>
              )}
              {user && (
                <Link
                  to="/create-listing"
                  className="bg-green-500 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-green-600 transition shadow-lg"
                >
                  Postavi Oglas
                </Link>
              )}
            </div>
          </div>

          {/* Stats */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white bg-opacity-20 backdrop-blur-lg rounded-xl p-6 text-center">
              <div className="text-4xl font-bold mb-2">{stats.listings}+</div>
              <div className="text-indigo-100">Aktivnih Oglasa</div>
            </div>
            <div className="bg-white bg-opacity-20 backdrop-blur-lg rounded-xl p-6 text-center">
              <div className="text-4xl font-bold mb-2">{stats.companies}+</div>
              <div className="text-indigo-100">Registrovanih Kompanija</div>
            </div>
            <div className="bg-white bg-opacity-20 backdrop-blur-lg rounded-xl p-6 text-center">
              <div className="text-4xl font-bold mb-2">{categories.length}</div>
              <div className="text-indigo-100">Kategorija</div>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Kategorije</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {categories.map(category => (
              <Link
                key={category.value}
                to={`/listings?category=${category.value}`}
                className="bg-gradient-to-br from-indigo-50 to-purple-50 hover:from-indigo-100 hover:to-purple-100 rounded-xl p-6 text-center transition shadow-md hover:shadow-lg"
              >
                <div className="text-3xl mb-2">📦</div>
                <div className="font-semibold text-gray-800">{category.label}</div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Listings */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Najnoviji Oglasi</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredListings.map(listing => (
              <Link
                key={listing.id}
                to={`/listings/${listing.id}`}
                className="bg-white rounded-xl shadow-md hover:shadow-xl transition overflow-hidden"
              >
                {listing.image_url && (
                  <img src={listing.image_url} alt={listing.title} className="w-full h-48 object-cover" />
                )}
                <div className="p-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="bg-indigo-100 text-indigo-800 text-xs font-semibold px-3 py-1 rounded-full">
                      {listing.category}
                    </span>
                    {listing.company?.is_verified && (
                      <span className="text-green-500 text-sm">✓ Verifikovano</span>
                    )}
                  </div>
                  <h3 className="text-xl font-bold text-gray-800 mb-2">{listing.title}</h3>
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">{listing.description}</p>
                  {listing.company && (
                    <div className="flex items-center text-sm text-gray-500">
                      <span className="font-medium">{listing.company.company_name}</span>
                      {listing.company.city && <span className="ml-2">• {listing.company.city}</span>}
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>
          <div className="text-center mt-8">
            <Link
              to="/listings"
              className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-lg font-semibold transition"
            >
              Pogledaj Sve Oglase
            </Link>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Kako Funkcioniše</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">📝</span>
              </div>
              <h3 className="text-xl font-bold mb-2">1. Registrujte se</h3>
              <p className="text-gray-600">Napravite profil vaše kompanije u nekoliko koraka</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">🔍</span>
              </div>
              <h3 className="text-xl font-bold mb-2">2. Pretražujte</h3>
              <p className="text-gray-600">Pronađite transportere, dobavljače ili postavite svoj oglas</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">💼</span>
              </div>
              <h3 className="text-xl font-bold mb-2">3. Povežite se</h3>
              <p className="text-gray-600">Kontaktirajte kompanije i započnite saradnju</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
