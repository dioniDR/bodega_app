<template>
    <div class="bg-white rounded shadow p-4 mb-6">
      <h3 class="font-semibold mb-3">➕ Agregar nuevo producto</h3>
  
      <!-- Categoría -->
      <label class="block mb-1 text-sm">Categoría</label>
      <select v-model="categoriaSeleccionada" @change="sugerirCodigo" class="mb-3 px-2 py-1 border rounded w-full">
        <option disabled value="">-- Selecciona categoría --</option>
        <option v-for="cat in categorias" :key="cat.codigo" :value="cat.codigo">
          {{ cat.codigo }} - {{ cat.nombre }}
        </option>
      </select>
  
      <!-- Código sugerido -->
      <label class="block mb-1 text-sm">Código sugerido</label>
      <input v-model="producto.codigo" class="mb-3 px-2 py-1 border rounded w-full" placeholder="001-001-001" />
  
      <!-- Nombre -->
      <label class="block mb-1 text-sm">Nombre</label>
      <input v-model="producto.nombre" class="mb-3 px-2 py-1 border rounded w-full" placeholder="Nombre del producto" />
  
      <!-- Precio -->
      <label class="block mb-1 text-sm">Precio</label>
      <input v-model.number="producto.precio" type="number" class="mb-3 px-2 py-1 border rounded w-full" placeholder="0.00" />
  
      <!-- Stock -->
      <label class="block mb-1 text-sm">Stock inicial</label>
      <input v-model.number="producto.stock" type="number" class="mb-3 px-2 py-1 border rounded w-full" placeholder="0" />
  
      <!-- Botón guardar -->
      <button @click="agregarProducto" class="mt-2 px-4 py-1 bg-green-600 text-white rounded">
        Guardar producto
      </button>
  
      <p v-if="mensaje" class="text-sm mt-2" :class="mensajeColor">{{ mensaje }}</p>
  
      <!-- Vista previa productos existentes -->
      <div v-if="productosCategoria.length" class="mt-4 text-sm">
        <strong class="block mb-1">Ejemplos en esta categoría:</strong>
        <ul class="list-disc ml-5">
          <li v-for="p in productosCategoria.slice(0, 5)" :key="p.codigo">{{ p.codigo }} – {{ p.nombre }}</li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, computed, onMounted } from 'vue'
  
  const categorias = [
    { codigo: "001", nombre: "Viveres secos" },
    { codigo: "002", nombre: "Refrescos" },
    { codigo: "003", nombre: "Dulces" },
    { codigo: "004", nombre: "Higiene personal" },
    { codigo: "005", nombre: "Limpieza" },
    { codigo: "006", nombre: "Repuestos de moto" },
    { codigo: "007", nombre: "Quincalla" },
    { codigo: "008", nombre: "Papelería" },
    { codigo: "009", nombre: "Misceláneos" },
    { codigo: "010", nombre: "Temporada" }
  ]
  
  const categoriaSeleccionada = ref("")
  const producto = ref({ codigo: "", nombre: "", precio: 0, stock: 0 })
  const mensaje = ref("")
  const mensajeColor = ref("")
  const productos = ref([])
  
  onMounted(() => {
    const data = localStorage.getItem('inventario')
    productos.value = data ? JSON.parse(data) : []
  })
  
  const productosCategoria = computed(() =>
    productos.value.filter(p => p.codigo.startsWith(`${categoriaSeleccionada.value}-`))
  )
  
  function sugerirCodigo() {
    const codigos = productosCategoria.value.map(p => p.codigo)
    let maxId = 0
  
    for (const c of codigos) {
      const partes = c.split("-")
      const id = parseInt(partes[2])
      if (!isNaN(id) && id > maxId) {
        maxId = id
      }
    }
  
    const siguiente = String(maxId + 1).padStart(3, "0")
    producto.value.codigo = `${categoriaSeleccionada.value}-001-${siguiente}`
  }
  
  function agregarProducto() {
    const existe = productos.value.find(p => p.codigo === producto.value.codigo)
  
    if (existe) {
      mensaje.value = "⚠️ Ese código ya existe."
      mensajeColor.value = "text-yellow-600"
      return
    }
  
    if (!producto.value.codigo || !producto.value.nombre) {
      mensaje.value = "⚠️ Código y nombre son obligatorios."
      mensajeColor.value = "text-red-600"
      return
    }
  
    productos.value.push({ ...producto.value })
    localStorage.setItem('inventario', JSON.stringify(productos.value))
  
    mensaje.value = "✅ Producto agregado."
    mensajeColor.value = "text-green-600"
  
    producto.value = { codigo: "", nombre: "", precio: 0, stock: 0 }
  }
  </script>
  