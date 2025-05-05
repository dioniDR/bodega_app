// Se adapta automáticamente según el ambiente
export const API_BASE_URL = import.meta.env.VITE_API_URL

// Esto también funciona (detección automática)
export const API_BASE_URL = import.meta.env.VITE_API_URL ||
  (import.meta.env.MODE === 'production' ? '/api' : 'http://localhost:8000/api')

export const API_ENDPOINTS = {
  productos: '/productos',
  movimientos: '/movimientos',
  stockBajo: '/stock-bajo',
  reporteVentas: '/reportes/ventas',
  enviarQR: '/enviar'
}

export const api = {
  async get(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`)
    return response.json()
  },
  
  async post(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    })
    return response.json()
  }
}