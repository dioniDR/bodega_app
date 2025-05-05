<template>
  <div class="bg-white p-4 rounded shadow">
    <h2 class="text-xl font-bold mb-4">📄 Libro de Ventas</h2>

    <!-- 🖋️ Formulario para registrar venta -->
    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-2">Registrar nueva venta</h3>
      <div class="grid grid-cols-2 gap-2 mb-2">
        <input v-model="nuevaVenta.fecha" type="date" class="border rounded px-2 py-1" />
        <input v-model="nuevaVenta.cliente" type="text" class="border rounded px-2 py-1" placeholder="Cliente" />
      </div>

      <!-- Productos seleccionados -->
      <div v-for="(p, i) in nuevaVenta.productos" :key="i" class="grid grid-cols-4 gap-2 mb-1">
        <select v-model="p.codigo" class="border rounded px-2 py-1">
          <option disabled value="">-- Producto --</option>
          <option v-for="prod in inventario" :key="prod.codigo" :value="prod.codigo">
            {{ prod.codigo }} - {{ prod.nombre }}
          </option>
        </select>
        <input v-model.number="p.cantidad" type="number" class="border rounded px-2 py-1" placeholder="Cantidad" />
        <input v-model.number="p.precio" type="number" class="border rounded px-2 py-1" placeholder="Precio" />
        <span class="px-2 py-1 text-right">{{ (p.precio * p.cantidad).toFixed(2) }}</span>
      </div>

      <button @click="agregarProducto" class="text-sm text-blue-600 mb-2">+ Agregar otro producto</button>

      <!-- IVA y total -->
      <div class="grid grid-cols-2 gap-2">
        <input v-model.number="nuevaVenta.iva" type="number" class="border rounded px-2 py-1" placeholder="IVA Bs" />
        <span class="px-2 py-1 text-right">💵 Total: {{ calcularTotal().toFixed(2) }}</span>
      </div>

      <button
        @click="guardarVenta"
        class="mt-3 px-4 py-1 bg-green-600 text-white rounded"
      >
        Guardar venta
      </button>
    </div>

    <!-- 📋 Tabla de ventas -->
    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-2">Ventas registradas</h3>
      <table class="w-full border text-sm">
        <thead class="bg-gray-100">
          <tr>
            <th class="p-2 border">Fecha</th>
            <th class="p-2 border">Cliente</th>
            <th class="p-2 border">Productos</th>
            <th class="p-2 border text-right">IVA</th>
            <th class="p-2 border text-right">Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(v, i) in ventas" :key="i" class="hover:bg-gray-50">
            <td class="p-2 border">{{ v.fecha }}</td>
            <td class="p-2 border">{{ v.cliente }}</td>
            <td class="p-2 border">
              <ul>
                <li v-for="(p, j) in v.productos" :key="j">
                  {{ p.cantidad }} x {{ p.codigo }} @ {{ p.precio.toFixed(2) }} Bs
                </li>
              </ul>
            </td>
            <td class="p-2 border text-right">{{ v.iva.toFixed(2) }}</td>
            <td class="p-2 border text-right">{{ v.total.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 📲 QR recibidos -->
    <div>
      <h3 class="text-lg font-semibold mb-2">QR recibidos desde el backend</h3>
      <ul class="bg-gray-50 rounded p-2 text-sm space-y-1">
        <li v-for="(qr, i) in codigosQR" :key="i" class="text-gray-700">
          🔍 {{ qr }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const ventas = ref([])
const inventario = ref([])
const codigosQR = ref([])

const nuevaVenta = ref({
  fecha: new Date().toISOString().slice(0, 10),
  cliente: '',
  productos: [{ codigo: '', cantidad: 1, precio: 0 }],
  iva: 0,
  total: 0
})

function agregarProducto() {
  nuevaVenta.value.productos.push({ codigo: '', cantidad: 1, precio: 0 })
}

function calcularTotal() {
  const subtotal = nuevaVenta.value.productos.reduce((sum, p) => {
    return sum + (p.precio * p.cantidad)
  }, 0)
  return subtotal + (nuevaVenta.value.iva || 0)
}

// 🧮 Generar asiento contable al guardar una venta
function generarAsientoContable(venta) {
  const descripcion = venta.cliente && venta.cliente !== 'VACÍO'
    ? `Venta a ${venta.cliente}`
    : 'Venta del día';

  const asiento = [
    {
      fecha: venta.fecha,
      descripcion,
      cuenta: 'Clientes',
      debe: venta.total,
      haber: 0
    },
    {
      fecha: venta.fecha,
      descripcion,
      cuenta: 'Ventas',
      debe: 0,
      haber: venta.total - venta.iva
    }
  ];

  if (venta.iva > 0) {
    asiento.push({
      fecha: venta.fecha,
      descripcion,
      cuenta: 'IVA por pagar',
      debe: 0,
      haber: venta.iva
    });
  }

  const asientos = JSON.parse(localStorage.getItem('asientos') || '[]');
  asientos.push(...asiento);
  localStorage.setItem('asientos', JSON.stringify(asientos));
}

// Modificar guardarVenta para incluir la generación del asiento contable
function guardarVenta() {
  const venta = {
    ...nuevaVenta.value,
    total: calcularTotal()
  };
  ventas.value.push(venta);
  localStorage.setItem('ventas', JSON.stringify(ventas.value));

  // Generar asiento contable
  generarAsientoContable(venta);

  nuevaVenta.value = {
    fecha: new Date().toISOString().slice(0, 10),
    cliente: '',
    productos: [{ codigo: '', cantidad: 1, precio: 0 }],
    iva: 0,
    total: 0
  };
}

function sincronizarVentasConLibroDiario() {
  const ventas = JSON.parse(localStorage.getItem('ventas') || '[]');
  let asientos = JSON.parse(localStorage.getItem('asientos') || '[]');

  ventas.forEach((venta) => {
    const descripcion = venta.cliente && venta.cliente !== 'VACÍO'
      ? `Venta a ${venta.cliente}`
      : 'Venta del día';

    const asiento = [
      {
        fecha: venta.fecha,
        descripcion,
        cuenta: 'Clientes',
        debe: venta.total,
        haber: 0
      },
      {
        fecha: venta.fecha,
        descripcion,
        cuenta: 'Ventas',
        debe: 0,
        haber: venta.total - venta.iva
      }
    ];

    if (venta.iva > 0) {
      asiento.push({
        fecha: venta.fecha,
        descripcion,
        cuenta: 'IVA por pagar',
        debe: 0,
        haber: venta.iva
      });
    }

    asientos.push(...asiento);
  });

  localStorage.setItem('asientos', JSON.stringify(asientos));
  alert('✅ Sincronización completa: asientos generados.');
}

function cargarDatos() {
  const v = localStorage.getItem('ventas')
  if (v) ventas.value = JSON.parse(v)

  const inv = localStorage.getItem('inventario')
  if (inv) inventario.value = JSON.parse(inv)

  const qr = localStorage.getItem('qr_codes')
  if (qr) codigosQR.value = JSON.parse(qr)
}

onMounted(cargarDatos)
</script>
