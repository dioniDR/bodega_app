# 📦 Sistema Contable Modular - Frontend

Este proyecto es una aplicación contable desarrollada con **Vue 3 + TailwindCSS (vía CDN)** y orientada a pequeñas bodegas, comercios y organizaciones que requieren una solución visual, offline y adaptable.

---

## 🧩 Módulos actuales

### ✅ `Libro de Ventas`
- Registro manual de ventas con fecha, cliente, productos vendidos.
- Cálculo automático de **IVA y Total**.
- Conexión con los productos del inventario (sugerencia de precio).
- Códigos QR recibidos desde una app Android de escaneo.
- Validación: cliente obligatorio o marcar como "VACÍO".

### ✅ `Libro Diario`
- Muestra todos los **asientos contables** generados a partir de las ventas.
- Estructura contable básica:
  - Debe: Clientes o Caja
  - Haber: Ventas, IVA por pagar
- Totales calculados automáticamente.

### ✅ `Inventario`
- Lista de productos con códigos tipo `XXX-XXX-XXX` (formato 3-3-3).
- Stock inicial por producto.
- Formulario inteligente para codificación:
  - Sugiere código según categoría
  - Valida duplicados
  - Precio editable solo si se marca

### ✅ `Lista de Productos`
- Visualiza todos los productos del inventario con su stock actual.
- Se carga desde `localStorage` o desde un archivo `.json` base si no hay datos.

---

## 🧠 Flujo del sistema (visual)

[ App Android QR ] → (envía códigos a backend FastAPI) ↓ [ Libro de Ventas ] ← (lectura de QR o venta manual) ↓ [ Libro Diario ] ← (asientos automáticos) ↓ [ Inventario / Productos ] (gestión de precios, stock y codificación)

yaml
Copy
Edit

---

## 📍 Estado actual

- Frontend funcional con 4 módulos integrados.
- No requiere base de datos aún (usa `localStorage`).
- Backend opcional con FastAPI para recibir códigos QR (`/enviar`).
- Puede ejecutarse en local (`npm run dev`).

---

## 📌 Próximos pasos

- [ ] Descuento automático de stock por ventas
- [ ] Validación cruzada entre ventas y productos existentes
- [ ] Panel de estadísticas básicas
- [ ] Exportar libros en `.csv` o `.pdf`
- [ ] Modo instalación tipo PWA
- [ ] Versión backend + autenticación

---

## ⚙️ Requisitos

- Node.js ≥ 16
- Navegador moderno
- Editor como VSCode

---

## 🧪 Modo de desarrollo

```bash
npm install
npm run dev
🗃️ Estructura principal
css
Copy
Edit
├── public/
├── src/
│   ├── App.vue
│   ├── main.js
│   └── components/
│       ├── Tabs.vue
│       ├── LibroVentas.vue
│       ├── LibroDiario.vue
│       ├── Inventario.vue
│       └── ListaProductos.vue
└── data/
    └── productos.json
📡 Backend (opcional)
Este frontend se puede conectar a un backend con FastAPI que reciba códigos desde la app Android en la ruta:

css
Copy
Edit
POST /enviar
Content-Type: application/json
Body: { "code": "123-456-789" }
📜 Licencia
MIT
