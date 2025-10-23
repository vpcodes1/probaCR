import React, { useState } from 'react'
import { api } from '../utils/api'

export default function Profile({ user }) {
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState({
    company_name: user.company_name || '',
    company_type: user.company_type || '',
    description: user.description || '',
    website: user.website || '',
    phone: user.phone || '',
    address: user.address || '',
    city: user.city || '',
    country: user.country || '',
    logo_url: user.logo_url || ''
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    try {
      const response = await api.updateProfile(formData)

      if (response.error) {
        setError(response.error)
      } else if (response.id) {
        // Update local storage
        const updatedUser = { ...user, ...response }
        localStorage.setItem('user', JSON.stringify(updatedUser))
        setSuccess('Profil uspešno ažuriran!')
        setEditing(false)
        // Reload page to update user data everywhere
        setTimeout(() => window.location.reload(), 1500)
      }
    } catch (err) {
      setError('Greška pri ažuriranju profila.')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-8 py-6">
          <h1 className="text-3xl font-bold text-white">Profil Kompanije</h1>
          <p className="text-indigo-100 mt-1">Upravljajte informacijama o vašoj kompaniji</p>
        </div>

        <div className="p-8">
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {success && (
            <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
              {success}
            </div>
          )}

          {!editing ? (
            <div className="space-y-6">
              {/* View Mode */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">Email</label>
                  <p className="text-gray-900 font-medium">{user.email}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">Naziv Kompanije</label>
                  <p className="text-gray-900 font-medium">{user.company_name}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">Tip Kompanije</label>
                  <p className="text-gray-900 font-medium">{user.company_type || 'Nije postavljeno'}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">Telefon</label>
                  <p className="text-gray-900 font-medium">{user.phone || 'Nije postavljeno'}</p>
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-500 mb-1">Opis</label>
                  <p className="text-gray-900">{user.description || 'Nije postavljeno'}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">Website</label>
                  {user.website ? (
                    <a href={user.website} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-700">
                      {user.website}
                    </a>
                  ) : (
                    <p className="text-gray-900">Nije postavljeno</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">Grad</label>
                  <p className="text-gray-900 font-medium">{user.city || 'Nije postavljeno'}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">Adresa</label>
                  <p className="text-gray-900 font-medium">{user.address || 'Nije postavljeno'}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">Država</label>
                  <p className="text-gray-900 font-medium">{user.country || 'Nije postavljeno'}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">Status</label>
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                    user.is_verified ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {user.is_verified ? '✓ Verifikovano' : 'Nije verifikovano'}
                  </span>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 mb-1">Registrovan</label>
                  <p className="text-gray-900 font-medium">
                    {new Date(user.created_at).toLocaleDateString('sr-RS')}
                  </p>
                </div>
              </div>

              <div className="pt-6 border-t">
                <button
                  onClick={() => setEditing(true)}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-semibold transition"
                >
                  Izmeni Profil
                </button>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Edit Mode */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Naziv Kompanije</label>
                  <input
                    type="text"
                    name="company_name"
                    value={formData.company_name}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Tip Kompanije</label>
                  <input
                    type="text"
                    name="company_type"
                    value={formData.company_type}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Opis</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    rows="4"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Website</label>
                  <input
                    type="url"
                    name="website"
                    value={formData.website}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Telefon</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Adresa</label>
                  <input
                    type="text"
                    name="address"
                    value={formData.address}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Grad</label>
                  <input
                    type="text"
                    name="city"
                    value={formData.city}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Država</label>
                  <input
                    type="text"
                    name="country"
                    value={formData.country}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Logo URL</label>
                  <input
                    type="url"
                    name="logo_url"
                    value={formData.logo_url}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div className="flex gap-4 pt-6 border-t">
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-semibold transition disabled:opacity-50"
                >
                  {loading ? 'Čuvanje...' : 'Sačuvaj Izmene'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setEditing(false)
                    setFormData({
                      company_name: user.company_name || '',
                      company_type: user.company_type || '',
                      description: user.description || '',
                      website: user.website || '',
                      phone: user.phone || '',
                      address: user.address || '',
                      city: user.city || '',
                      country: user.country || '',
                      logo_url: user.logo_url || ''
                    })
                  }}
                  className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
                >
                  Otkaži
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}
