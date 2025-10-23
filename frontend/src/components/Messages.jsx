import React, { useState, useEffect } from 'react'
import { api } from '../utils/api'

export default function Messages({ user }) {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('received')
  const [selectedMessage, setSelectedMessage] = useState(null)

  useEffect(() => {
    fetchMessages()
  }, [filter])

  const fetchMessages = async () => {
    setLoading(true)
    const data = await api.getMessages(filter)
    if (data.messages) {
      setMessages(data.messages)
    }
    setLoading(false)
  }

  const handleMessageClick = async (message) => {
    setSelectedMessage(message)
    if (!message.is_read && message.receiver_id === user.id) {
      await api.markAsRead(message.id)
      fetchMessages()
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString('sr-RS', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Poruke</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Messages List */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            {/* Filter Tabs */}
            <div className="flex border-b">
              <button
                onClick={() => setFilter('received')}
                className={`flex-1 px-4 py-3 text-sm font-medium transition ${
                  filter === 'received'
                    ? 'bg-indigo-50 text-indigo-600 border-b-2 border-indigo-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                Primljene
              </button>
              <button
                onClick={() => setFilter('sent')}
                className={`flex-1 px-4 py-3 text-sm font-medium transition ${
                  filter === 'sent'
                    ? 'bg-indigo-50 text-indigo-600 border-b-2 border-indigo-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                Poslate
              </button>
            </div>

            {/* Messages */}
            <div className="divide-y max-h-[600px] overflow-y-auto">
              {loading ? (
                <div className="p-8 text-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
                </div>
              ) : messages.length === 0 ? (
                <div className="p-8 text-center">
                  <div className="text-4xl mb-2">📭</div>
                  <p className="text-gray-600">Nema poruka</p>
                </div>
              ) : (
                messages.map(message => (
                  <button
                    key={message.id}
                    onClick={() => handleMessageClick(message)}
                    className={`w-full text-left p-4 hover:bg-gray-50 transition ${
                      selectedMessage?.id === message.id ? 'bg-indigo-50' : ''
                    } ${!message.is_read && message.receiver_id === user.id ? 'bg-blue-50' : ''}`}
                  >
                    <div className="flex items-start justify-between mb-1">
                      <span className="font-semibold text-gray-900 text-sm">
                        {filter === 'received' ? message.sender_name : message.receiver_name}
                      </span>
                      {!message.is_read && message.receiver_id === user.id && (
                        <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                      )}
                    </div>
                    <p className="text-sm font-medium text-gray-800 mb-1 line-clamp-1">{message.subject}</p>
                    <p className="text-xs text-gray-500">{formatDate(message.created_at)}</p>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Message Detail */}
        <div className="lg:col-span-2">
          {selectedMessage ? (
            <div className="bg-white rounded-xl shadow-md p-6">
              <div className="border-b pb-4 mb-4">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">{selectedMessage.subject}</h2>
                <div className="flex items-center justify-between text-sm text-gray-600">
                  <div>
                    <span className="font-medium">
                      {filter === 'received' ? 'Od: ' : 'Za: '}
                      {filter === 'received' ? selectedMessage.sender_name : selectedMessage.receiver_name}
                    </span>
                  </div>
                  <span>{formatDate(selectedMessage.created_at)}</span>
                </div>
              </div>
              <div className="prose max-w-none">
                <p className="text-gray-700 whitespace-pre-wrap">{selectedMessage.message}</p>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-md p-12 text-center">
              <div className="text-6xl mb-4">💬</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Izaberite poruku</h3>
              <p className="text-gray-600">Kliknite na poruku sa leve strane da je pročitate</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
