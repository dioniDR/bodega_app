 Ficha informativa: Sistema de Codificación de Productos XXX-XXX-XXX
Este sistema organiza los productos del inventario de forma jerárquica y flexible para facilitar el control, búsqueda, categorización y escalabilidad.

📐 Estructura del código
Formato:

Copy
Edit
AAA-BBB-CCC

Bloque	Significado	Ejemplo
AAA	Área o categoría principal	001 → Viveres secos
BBB	Subcategoría o grupo interno	002 → Azúcar y derivados
CCC	Número único del producto	005 → Azúcar morena 1kg
Ejemplo completo:

Copy
Edit
001-002-005 → Viveres secos > Azúcar > Azúcar morena 1kg
🧾 Estructura mínima esperada por producto
json
Copy
Edit
{
  "codigo": "001-002-005",
  "nombre": "Azúcar morena 1kg",
  "precio": 1.60,
  "stock": 20
}
🧱 Campos adicionales sugeridos (opcional)
json
Copy
Edit
{
  "unidad": "kg",
  "iva": true,
  "categoria": "Viveres secos",
  "subcategoria": "Azúcar",
  "proveedor": "Distribuidora DulceSol",
  "fechaIngreso": "2025-04-21"
}
🎯 Ventajas del sistema
🔍 Búsqueda rápida por categoría o grupo

🧩 Escalable a múltiples tipos de bodega o comercio

📦 Compatible con códigos QR u otras codificaciones físicas

🔄 Automatizable en backend y frontend

📚 Fáciles de mantener y auditar

🔐 Consideraciones
Todos los códigos deben ser únicos y no repetirse

El sistema debe permitir agregar nuevos códigos sin colapsar la estructura

Puede ser utilizado como clave primaria en bases de datos o como identificador QR

¿Deseas que esta ficha se guarde automáticamente como archivo CODIFICACION.md dentro del proyecto library?

