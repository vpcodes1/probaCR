import React, { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { api } from '../utils/api'

export default function Listings() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [listings, setListings] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    category: searchParams.get('category') || '',
    search: searchParams.get('search') || '',
    location: searchParams.get('location') || ''
  })
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 12,
    total: 0,
    total_pages: 0
  })

  useEffect(() => {
    api.getCategories().then(data => {
      if (data.categories) {
        setCategories(data.categories)
      }
    })
  }, [])

  useEffect(() => {
    fetchListings()
  }, [filters, pagination.page])

  const fetchListings = async () => {
    setLoading(true)
    const params = {
      ...filters,
      page: pagination.page,
      per_page: pagination.per_page
    }

    // Remove empty params
    Object.keys(params).forEach(key => {
      if (!params[key]) delete params[key]
    })

    const data = await api.getListings(params)
    if (data.listings) {
      setListings(data.listings)
      setPagination(prev => ({
        ...prev,
        total: data.total,
        total_pages: data.total_pages
      }))
    }
    setLoading(false)
  }

  const handleFilterChange = (e) => {
    const { name, value } = e.target
    setFilters(prev => ({ ...prev, [name]: value }))
    setPagination(prev => ({ ...prev, page: 1 }))

    // Update URL params
    const newParams = new URLSearchParams(searchParams)
    if (value) {
      newParams.set(name, value)
    } else {
      newParams.delete(name)
    }
    setSearchParams(newParams)
  }

  const handleSearch = (e) => {
    e.preventDefault()
    fetchListings()
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Oglasi</h1>
        <p className="text-gray-600">Pronađite transportere, dobavljače i poslovne partnere</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <form onSubmit={handleSearch} className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Kategorija</label>
            <select
              name="category"
              value={filters.category}
              onChange={handleFilterChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">Sve kategorije</option>
              {categories.map(cat => (
                <option key={cat.value} value={cat.value}>{cat.label}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Lokacija</label>
            <input
              type="text"
              name="location"
              value={filters.location}
              onChange={handleFilterChange}
              placeholder="Grad..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">Pretraga</label>
            <div className="flex gap-2">
              <input
                type="text"
                name="search"
                value={filters.search}
                onChange={handleFilterChange}
                placeholder="Pretražite oglase..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
              <button
                type="submit"
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg font-medium transition"
              >
                Pretraži
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* Results */}
      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Učitavanje oglasa...</p>
        </div>
      ) : listings.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-12 text-center">
          <div className="text-6xl mb-4">🔍</div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Nema rezultata</h3>
          <p className="text-gray-600">Pokušajte sa drugačijim filterima</p>
        </div>
      ) : (
        <>
          <div className="mb-4 text-gray-600">
            Pronađeno {pagination.total} oglasa
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {listings.map(listing => (
              <Link
                key={listing.id}
                to={`/listings/${listing.id}`}
                className="bg-white rounded-xl shadow-md hover:shadow-xl transition overflow-hidden group"
              >
                {listing.image_url ? (
                  <img src={listing.image_url} alt={listing.title} className="w-full h-48 object-cover group-hover:scale-105 transition" />
                ) : (
                  <div className="w-full h-48 bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center">
                    <span className="text-6xl">📦</span>
                  </div>
                )}
                <div className="p-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="bg-indigo-100 text-indigo-800 text-xs font-semibold px-3 py-1 rounded-full">
                      {categories.find(c => c.value === listing.category)?.label || listing.category}
                    </span>
                    {listing.company?.is_verified && (
                      <span className="text-green-500 text-sm">✓</span>
                    )}
                  </div>
                  <h3 className="text-xl font-bold text-gray-800 mb-2 group-hover:text-indigo-600 transition">
                    {listing.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">{listing.description}</p>
                  {listing.company && (
                    <div className="flex items-center text-sm text-gray-500 border-t pt-3">
                      <span className="font-medium">{listing.company.company_name}</span>
                      {listing.company.city && <span className="ml-2">• {listing.company.city}</span>}
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>

          {/* Pagination */}
          {pagination.total_pages > 1 && (
            <div className="flex justify-center gap-2">
              <button
                onClick={() => setPagination(prev => ({ ...prev, page: prev.page - 1 }))}
                disabled={pagination.page === 1}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Prethodna
              </button>
              <span className="px-4 py-2 text-gray-700">
                Strana {pagination.page} od {pagination.total_pages}
              </span>
              <button
                onClick={() => setPagination(prev => ({ ...prev, page: prev.page + 1 }))}
                disabled={pagination.page === pagination.total_pages}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Sledeća
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
