const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const getAuthHeader = () => {
  const token = localStorage.getItem('token')
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}

export const api = {
  // Auth
  async register(data) {
    const response = await fetch(`${API_URL}/api/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    return response.json()
  },

  async login(data) {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    return response.json()
  },

  // Listings
  async getListings(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const response = await fetch(`${API_URL}/api/listings?${queryString}`)
    return response.json()
  },

  async getListing(id) {
    const response = await fetch(`${API_URL}/api/listings/${id}`)
    return response.json()
  },

  async createListing(data) {
    const response = await fetch(`${API_URL}/api/listings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(data),
    })
    return response.json()
  },

  async updateListing(id, data) {
    const response = await fetch(`${API_URL}/api/listings/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(data),
    })
    return response.json()
  },

  async deleteListing(id) {
    const response = await fetch(`${API_URL}/api/listings/${id}`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    })
    return response.json()
  },

  async getMyListings() {
    const response = await fetch(`${API_URL}/api/listings/my`, {
      headers: getAuthHeader(),
    })
    return response.json()
  },

  async getCategories() {
    const response = await fetch(`${API_URL}/api/listings/categories`)
    return response.json()
  },

  // Messages
  async getMessages(type = 'received') {
    const response = await fetch(`${API_URL}/api/messages?type=${type}`, {
      headers: getAuthHeader(),
    })
    return response.json()
  },

  async sendMessage(data) {
    const response = await fetch(`${API_URL}/api/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(data),
    })
    return response.json()
  },

  async markAsRead(id) {
    const response = await fetch(`${API_URL}/api/messages/${id}/read`, {
      method: 'PUT',
      headers: getAuthHeader(),
    })
    return response.json()
  },

  async getUnreadCount() {
    const response = await fetch(`${API_URL}/api/messages/unread-count`, {
      headers: getAuthHeader(),
    })
    return response.json()
  },

  // Companies
  async getCompanies(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const response = await fetch(`${API_URL}/api/companies?${queryString}`)
    return response.json()
  },

  async getCompany(id) {
    const response = await fetch(`${API_URL}/api/companies/${id}`)
    return response.json()
  },

  async updateProfile(data) {
    const response = await fetch(`${API_URL}/api/companies/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(data),
    })
    return response.json()
  },
}
