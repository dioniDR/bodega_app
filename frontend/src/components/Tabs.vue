<script setup>
import { ref } from 'vue'
import LibroDiario from './LibroDiario.vue'
import FormularioAsiento from './FormularioAsiento.vue' // ✅ nuevo
import LibroVentas from './LibroVentas.vue' // ✅ si está en /src/components
import ListaProductos from './ListaProductos.vue'
import Inventario from './Inventario.vue'




const tab = ref('diario')
const asientos = ref([])

const agregar = (nuevos) => {
  asientos.value.push(...nuevos)
}
</script>

<template>
  <div>
    <div class="flex gap-2 mb-4">
      <button @click="tab = 'ventas'" class="px-4 py-2 rounded bg-blue-500 text-white">Libro de Ventas</button>
      <button @click="tab = 'diario'" class="px-4 py-2 rounded bg-blue-500 text-white" :class="{ 'bg-blue-700': tab === 'diario' }">Libro Diario</button>
      <button @click="tab = 'mayor'" class="px-4 py-2 rounded bg-blue-500 text-white" :class="{ 'bg-blue-700': tab === 'mayor' }">Libro Mayor</button>
      <button @click="tab = 'productos'" class="px-4 py-2 rounded bg-blue-500 text-white" :class="{ 'bg-blue-700': tab === 'productos' }">Lista de Productos</button>
      <button @click="tab = 'inventario'" class="px-4 py-2 rounded bg-blue-500 text-white" :class="{ 'bg-blue-700': tab === 'inventario' }">Inventario</button>
    </div>

    <FormularioAsiento v-if="tab === 'diario'" @agregar="agregar" />
    <LibroVentas v-if="tab === 'ventas'" @registrarAsiento="agregar" />
    <LibroDiario v-if="tab === 'diario'" :asientos="asientos" />
    <ListaProductos v-if="tab === 'productos'" @registrarAsiento="agregar" />
    <Inventario v-if="tab === 'inventario'" @registrarAsiento="agregar" />
    <div v-if="tab === 'mayor'" class="text-gray-500">[Libro Mayor próximamente]</div>
  </div>
</template>
