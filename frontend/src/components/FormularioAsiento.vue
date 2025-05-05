<template>
  <div class="bg-white p-4 rounded shadow mb-6">
    <h2 class="text-lg font-semibold mb-4">Registrar nuevo asiento</h2>

    <div class="mb-2">
      <label class="block text-sm mb-1">Fecha</label>
      <input v-model="fecha" type="date" class="w-full border px-2 py-1 rounded" />
    </div>

    <div class="mb-2">
      <label class="block text-sm mb-1">Descripción</label>
      <input v-model="descripcion" type="text" class="w-full border px-2 py-1 rounded" placeholder="Ej: Compra al contado" />
    </div>

    <div class="mb-3">
      <table class="w-full border text-sm">
        <thead class="bg-gray-100">
          <tr>
            <th class="p-2 border">Cuenta</th>
            <th class="p-2 border">Tipo</th>
            <th class="p-2 border">Monto</th>
            <th class="p-2 border"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(linea, index) in lineas" :key="index">
            <td class="p-2 border">
              <input v-model="linea.cuenta" type="text" class="w-full border rounded px-2 py-1" placeholder="Ej: 1101 - Caja" />
            </td>
            <td class="p-2 border">
              <select v-model="linea.tipo" class="border rounded px-2 py-1 w-full">
                <option value="debe">Debe</option>
                <option value="haber">Haber</option>
              </select>
            </td>
            <td class="p-2 border">
              <input v-model.number="linea.monto" type="number" min="0" class="w-full border rounded px-2 py-1" />
            </td>
            <td class="p-2 border text-center">
              <button @click="eliminarLinea(index)" class="text-red-500 hover:underline">✕</button>
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="agregarLinea" class="mt-2 text-blue-600 hover:underline">➕ Agregar línea</button>
    </div>

    <div class="flex justify-between items-center">
      <div class="text-sm text-gray-700">
        Total Debe: {{ totalDebe }} Bs | Total Haber: {{ totalHaber }} Bs
      </div>
      <button
        @click="registrarAsiento"
        :disabled="totalDebe !== totalHaber || totalDebe === 0"
        class="px-4 py-2 bg-green-600 text-white rounded disabled:bg-gray-400"
      >
        Registrar Asiento
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
const emit = defineEmits(['agregar'])

const fecha = new Date().toISOString().substr(0, 10)
const descripcion = reactive({ text: '' })

const lineas = reactive([
  { cuenta: '', tipo: 'debe', monto: 0 }
])

const agregarLinea = () => {
  lineas.push({ cuenta: '', tipo: 'debe', monto: 0 })
}

const eliminarLinea = (index) => {
  lineas.splice(index, 1)
}

const totalDebe = computed(() =>
  lineas.filter(l => l.tipo === 'debe').reduce((s, l) => s + l.monto, 0)
)

const totalHaber = computed(() =>
  lineas.filter(l => l.tipo === 'haber').reduce((s, l) => s + l.monto, 0)
)

const registrarAsiento = () => {
  const nuevosAsientos = lineas.map(l => ({
    fecha,
    descripcion: descripcion.text,
    cuenta: l.cuenta,
    debe: l.tipo === 'debe' ? l.monto : 0,
    haber: l.tipo === 'haber' ? l.monto : 0
  }))
  emit('agregar', nuevosAsientos)

  // Limpiar
  descripcion.text = ''
  lineas.splice(0, lineas.length, { cuenta: '', tipo: 'debe', monto: 0 })
}
</script>
