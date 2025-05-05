# Bodega App - Sistema de Gestión de Inventario

## 🎯 Descripción

Bodega App es un sistema de gestión de inventario inteligente que utiliza el framework t-p para integrar modelos de lenguaje (LLMs) con bases de datos, permitiendo consultas en lenguaje natural y automatización de tareas.

## 🚀 Características

- **Consultas en Lenguaje Natural**: Habla con tu inventario usando preguntas comunes
- **Agentes Inteligentes**: Procesamiento automático de comandos de inventario
- **Testing Dinámico**: Análisis automático de estructura de base de datos
- **Integración Multi-LLM**: Soporta OpenAI, Claude y modelos locales
- **Base de Datos Flexible**: Trabaja con MySQL, PostgreSQL y SQLite

## 🔧 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/bodega_app.git
cd bodega_app

# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env-example .env
# Editar .env con tus credenciales