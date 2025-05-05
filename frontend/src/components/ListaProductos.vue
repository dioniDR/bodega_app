<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">📦 Lista de Productos</h2>

    <table class="w-full text-sm border">
      <thead class="bg-gray-100">
        <tr>
          <th class="border p-2">Código</th>
          <th class="border p-2">Nombre</th>
          <th class="border p-2 text-right">Precio (Bs)</th>
          <th class="border p-2 text-right">Stock</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(producto, index) in productos"
          :key="index"
          class="hover:bg-gray-50"
        >
          <td class="border p-2">{{ producto.codigo }}</td>
          <td class="border p-2">{{ producto.nombre }}</td>
          <td class="border p-2 text-right">{{ producto.precio.toFixed(2) }}</td>
          <td class="border p-2 text-right">{{ producto.stock }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const productos = ref([])

onMounted(async () => {
  const local = localStorage.getItem('inventario')
  if (local) {
    productos.value = JSON.parse(local)
  } else {
    const res = await fetch('../data/productos_base.json')
    const data = await res.json()
    productos.value = Object.values(data)
    localStorage.setItem('inventario', JSON.stringify(productos.value))
  }
})
</script>
