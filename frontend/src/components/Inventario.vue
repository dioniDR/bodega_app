<template>
    <div class="p-4">
      <h2 class="text-xl font-bold mb-4">🛠️ Inventario</h2>
  
      <!-- 📥 Formulario para agregar producto -->
      <FormularioProducto />
  
      <!-- 📦 Tabla del inventario -->
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
          <tr v-for="(p, i) in productos" :key="i" class="hover:bg-gray-50">
            <td class="border p-2">{{ p.codigo }}</td>
            <td class="border p-2">{{ p.nombre }}</td>
            <td class="border p-2 text-right">{{ p.precio.toFixed(2) }}</td>
            <td class="border p-2 text-right">{{ p.stock }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import FormularioProducto from './FormularioProducto.vue'
  import { ref, onMounted } from 'vue'
  
  const productos = ref([])
  const mensaje = ref('')
  const mensajeColor = ref('')
  const nuevo = ref({
    codigo: '',
    nombre: '',
    precio: 0,
    stock: 0
  })
  
  onMounted(async () => {
    const local = localStorage.getItem('inventario')
    if (local) {
      productos.value = JSON.parse(local)
    } else {
      const res = await fetch('productos_base.json')
      const data = await res.json()
      productos.value = Object.values(data)
      localStorage.setItem('inventario', JSON.stringify(productos.value))
    }
  })
  
  function agregarProducto() {
    if (!nuevo.value.codigo || !nuevo.value.nombre) {
      mensaje.value = '⚠️ Código y nombre son obligatorios.'
      mensajeColor.value = 'text-red-600'
      return
    }
  
    const duplicado = productos.value.find(p => p.codigo === nuevo.value.codigo)
    if (duplicado) {
      mensaje.value = '⚠️ Ya existe un producto con ese código.'
      mensajeColor.value = 'text-yellow-600'
      return
    }
  
    productos.value.push({ ...nuevo.value })
    localStorage.setItem('inventario', JSON.stringify(productos.value))
  
    mensaje.value = '✅ Producto agregado exitosamente.'
    mensajeColor.value = 'text-green-600'
  
    // Limpiar formulario
    nuevo.value = { codigo: '', nombre: '', precio: 0, stock: 0 }
  }
  </script>
  