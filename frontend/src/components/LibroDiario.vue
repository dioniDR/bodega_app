<template>
  <div>
    <table class="w-full border text-sm">
      <thead class="bg-gray-200">
        <tr>
          <th class="p-2 border">Fecha</th>
          <th class="p-2 border">Descripción</th>
          <th class="p-2 border">Cuenta</th>
          <th class="p-2 border text-right">Debe (Bs)</th>
          <th class="p-2 border text-right">Haber (Bs)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(a, i) in asientos" :key="i" class="hover:bg-gray-50">
          <td class="p-2 border">{{ a.fecha }}</td>
          <td class="p-2 border">{{ a.descripcion }}</td>
          <td class="p-2 border">{{ a.cuenta }}</td>
          <td class="p-2 border text-right">{{ a.debe.toFixed(2) }}</td>
          <td class="p-2 border text-right">{{ a.haber.toFixed(2) }}</td>
        </tr>
      </tbody>
      <tfoot>
        <tr class="font-semibold bg-gray-100">
          <td colspan="3" class="p-2 border text-right">Totales:</td>
          <td class="p-2 border text-right">{{ totalDebe.toFixed(2) }}</td>
          <td class="p-2 border text-right">{{ totalHaber.toFixed(2) }}</td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'

const asientos = ref([])

function cargarAsientos() {
  const guardados = localStorage.getItem('asientos')
  if (guardados) {
    asientos.value = JSON.parse(guardados)
  }
}

onMounted(() => {
  cargarAsientos()
})

const totalDebe = computed(() =>
  asientos.value.reduce((s, a) => s + a.debe, 0)
)
const totalHaber = computed(() =>
  asientos.value.reduce((s, a) => s + a.haber, 0)
)
</script>

