# 🚀 Guía de Implementación - Sistema Bodega App

## 📋 Visión General

Sistema modular para gestión de inventario que combina:
- **Backend FastAPI**: API REST con CRUD completo
- **Frontend Vue**: Interfaz reactiva con TailwindCSS
- **Base de Datos**: MySQL con estructura flexible
- **Agentes IA**: Procesamiento de lenguaje natural

## 🏗️ Arquitectura Recomendada

### 1. Estructura de Directorios
```
bodega_app/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── schemas/
│   │   │   ├── products.py
│   │   │   ├── sales.py
│   │   │   └── movements.py
│   │   └── routes/
│   │       ├── products.py
│   │       ├── sales.py
│   │       └── movements.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── config/
│   │   │   └── api.js
│   │   ├── services/
│   │   ├── stores/
│   │   └── views/
│   ├── public/
│   └── package.json
├── .env
├── .env.example
└── README.md
```

### 2. Esquema de Base de Datos
```sql
CREATE DATABASE bodega_inventory;

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(15) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100),
    precio DECIMAL(10,2) NOT NULL,
    stock_actual INT DEFAULT 0,
    stock_minimo INT DEFAULT 0,
    ubicacion VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    tipo_movimiento ENUM('entrada', 'salida') NOT NULL,
    cantidad INT NOT NULL,
    motivo VARCHAR(255),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario VARCHAR(100),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente VARCHAR(255),
    fecha_venta DATE,
    total DECIMAL(10,2),
    iva DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE detalles_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT,
    producto_id INT,
    cantidad INT,
    precio_unitario DECIMAL(10,2),
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
```

## 💻 Implementación Modular

### Backend FastAPI

#### 1. Configuración Principal
```python
# backend/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import products, sales, movements

app = FastAPI(title="Bodega API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(sales.router, prefix="/api/sales", tags=["sales"])
app.include_router(movements.router, prefix="/api/movements", tags=["movements"])
```

#### 2. Esquemas Pydantic
```python
# backend/api/schemas/products.py
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    categoria: str
    precio: float
    stock_actual: int = 0
    stock_minimo: int = 0
    ubicacion: Optional[str] = None
    
    @validator('codigo')
    def validate_codigo(cls, v):
        if not re.match(r'^\d{3}-\d{3}-\d{3}$', v):
            raise ValueError("Formato de código inválido. Use: XXX-XXX-XXX")
        return v

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock_minimo: Optional[int] = None
    # ... otros campos opcionales

class ProductResponse(ProductBase):
    id: int
    activo: bool
    created_at: datetime
    
    class Config:
        orm_mode = True
```

#### 3. Rutas Modulares
```python
# backend/api/routes/products.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..schemas.products import ProductCreate, ProductUpdate, ProductResponse
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    db = Depends(get_db)
):
    # Implementación
    pass

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db = Depends(get_db)):
    # Implementación
    pass
```

### Frontend Vue 3

#### 1. Configuración de API
```javascript
// frontend/src/config/api.js
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = {
  async get(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`)
    if (!response.ok) throw new Error('Network error')
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
    if (!response.ok) throw new Error('Network error')
    return response.json()
  }
}

export const productsApi = {
  getAll: () => api.get('/api/products'),
  create: (product) => api.post('/api/products', product),
  getById: (id) => api.get(`/api/products/${id}`),
  update: (id, product) => api.put(`/api/products/${id}`, product),
  delete: (id) => api.delete(`/api/products/${id}`)
}
```

#### 2. Componente de Producto
```vue
<!-- frontend/src/components/ProductForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="bg-white p-4 rounded shadow">
    <div class="mb-4">
      <label class="block text-sm mb-1">Código</label>
      <input v-model="form.codigo" class="w-full border px-2 py-1 rounded" 
             pattern="[0-9]{3}-[0-9]{3}-[0-9]{3}" placeholder="000-000-000" />
    </div>
    <!-- Más campos -->
    <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
      {{ isEditing ? 'Actualizar' : 'Crear' }} Producto
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { productsApi } from '../config/api'

const props = defineProps({
  initialData: Object,
  isEditing: Boolean
})

const form = ref({
  codigo: '',
  nombre: '',
  precio: 0,
  stock_actual: 0,
  // ... otros campos
})

const handleSubmit = async () => {
  try {
    if (props.isEditing) {
      await productsApi.update(props.initialData.id, form.value)
    } else {
      await productsApi.create(form.value)
    }
    // Emitir evento o recargar lista
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>
```

#### 3. Store con Pinia
```javascript
// frontend/src/stores/products.js
import { defineStore } from 'pinia'
import { productsApi } from '../config/api'

export const useProductsStore = defineStore('products', {
  state: () => ({
    products: [],
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchProducts() {
      this.loading = true
      try {
        const response = await productsApi.getAll()
        this.products = response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    async addProduct(product) {
      try {
        const response = await productsApi.create(product)
        this.products.push(response.data)
      } catch (error) {
        this.error = error.message
        throw error
      }
    }
  }
})
```

## 🔧 Variables de Entorno

### Backend (.env)
```env
# Base de datos
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
MYSQL_DATABASE=bodega_inventory

# API Keys para agentes IA
OPENAI_API_KEY=tu_clave_openai
ANTHROPIC_API_KEY=tu_clave_claude

# Configuración de aplicación
ENVIRONMENT=development
DEBUG=True
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_TITLE=Bodega App
```

## 🚀 Flujo de Desarrollo

### 1. Inicialización
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### 2. Construcción para Producción
```bash
# Frontend
cd frontend
npm run build

# Backend serve frontend + API
cd backend
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### 3. Patrones de Código Recomendados

#### Error Handling
```python
# Backend
from fastapi import HTTPException

@router.post("/products")
async def create_product(product: ProductCreate):
    try:
        # Lógica
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno")
```

```javascript
// Frontend
const handleSubmit = async () => {
  try {
    const response = await api.post('/products', form.value)
    notification.success('Producto creado')
  } catch (error) {
    if (error.response?.status === 400) {
      notification.error(error.response.data.detail)
    } else {
      notification.error('Error al crear producto')
    }
  }
}
```

#### Validación de Datos
```python
# Backend
from pydantic import BaseModel, validator

class ProductCreate(BaseModel):
    codigo: str
    
    @validator('codigo')
    def validate_codigo(cls, v):
        if not re.match(r'^\d{3}-\d{3}-\d{3}$', v):
            raise ValueError("Formato inválido")
        return v
```

```javascript
// Frontend
const validateForm = () => {
  const errors = {}
  
  if (!form.value.codigo.match(/^\d{3}-\d{3}-\d{3}$/)) {
    errors.codigo = 'Formato inválido'
  }
  
  if (form.value.precio <= 0) {
    errors.precio = 'El precio debe ser mayor a 0'
  }
  
  return errors
}
```

## 📊 Monitoreo y Logging

### Backend
```python
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

### Frontend
```javascript
// frontend/src/services/logger.js
export const logger = {
  info: (message, data = {}) => {
    console.log(`[INFO] ${message}`, data)
    // Enviar a servicio de logging si es necesario
  },
  
  error: (message, error) => {
    console.error(`[ERROR] ${message}`, error)
    // Reportar error a Sentry o similar
  }
}
```

## 🔐 Seguridad

### 1. Autenticación JWT (Opcional)
```python
# backend/api/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 2. Sanitización de Inputs
```python
import re
from fastapi import HTTPException

def sanitize_input(text: str) -> str:
    # Eliminar caracteres especiales peligrosos
    return re.sub(r'[^\w\s-]', '', text)

@router.post("/products")
async def create_product(product: ProductCreate):
    product.nombre = sanitize_input(product.nombre)
    product.descripcion = sanitize_input(product.descripcion)
    # ...
```

## 📈 Optimización y Escalabilidad

### 1. Caché
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@router.get("/products")
@cache(expire=60)  # Cache por 60 segundos
async def list_products():
    # ...
```

### 2. Paginación
```python
from fastapi import Depends, Query

class Pagination:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100)
    ):
        self.skip = skip
        self.limit = limit

@router.get("/products")
async def list_products(pagination: Pagination = Depends()):
    # ...
```

### 3. Compresión de Respuestas
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## 🧪 Testing

### Backend
```python
# tests/test_products.py
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_create_product():
    response = client.post("/api/products", json={
        "codigo": "001-001-001",
        "nombre": "Producto Test",
        "precio": 10.0
    })
    assert response.status_code == 200
    assert response.json()["codigo"] == "001-001-001"
```

### Frontend
```javascript
// frontend/tests/ProductForm.spec.js
import { mount } from '@vue/test-utils'
import ProductForm from '@/components/ProductForm.vue'

describe('ProductForm', () => {
  it('valida código correcto', async () => {
    const wrapper = mount(ProductForm)
    await wrapper.find('input').setValue('001-001-001')
    expect(wrapper.vm.validateCodigo()).toBe(true)
  })
})
```

## 📚 Documentación API

FastAPI genera documentación automática:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Para personalizar:
```python
app = FastAPI(
    title="Bodega API",
    description="API para gestión de inventario",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

## 🚀 Deploy a Producción

### Docker
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MYSQL_HOST=db
      - MYSQL_DATABASE=bodega_inventory
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=secret
      - MYSQL_DATABASE=bodega_inventory
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## 💡 Tips Finales

1. **Mantén la modularidad**: Cada entidad (producto, venta, etc.) en su propio módulo
2. **Usa TypeScript** en el frontend para mejor type safety
3. **Implementa rate limiting** en la API
4. **Configura CI/CD** con GitHub Actions
5. **Documenta todo** el código y mantén un CHANGELOG
6. **Usa variables de entorno** para todos los secretos
7. **Implementa logs centralizados** para monitoreo
8. **Realiza backups** regulares de la base de datos