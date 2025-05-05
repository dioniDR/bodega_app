# 📚 Guía de Comandos - Bodega App

## 🗺️ Diccionario de Comandos

### 1. Agentes

#### DB Agent (Base de Datos)
```bash
# Modo interactivo - Para consultas en lenguaje natural
python -m agent_modules.db_agent.agent --interactive

# Consulta única
python -m agent_modules.db_agent.agent \
  --prompt "¿Cuántos productos hay en cada categoría?" \
  --type mysql

# Con parámetros específicos de conexión
python -m agent_modules.db_agent.agent \
  --prompt "Mostrar todos los productos" \
  --host 127.0.0.1 \
  --port 3307 \
  --user root \
  --database bodega_inventory

# Explorar bases de datos disponibles
python -m agent_modules.db_agent.agent --explore

# Reiniciar caché de conexiones
python -m agent_modules.db_agent.agent --reset-cache
```

#### Bodega Agent (Inventario Especializado)
```bash
# Modo interactivo
python -m agent_modules.bodega_agent.agent --interactive

# Consultas especializadas
# Ver inventario completo
# Productos con stock bajo
# Registrar entrada de productos
# Registrar salida de productos
# Alertas de stock bajo
# Generar reportes
```

#### Command Agent (Procesamiento de Comandos)
```bash
# Modo ejemplo
python -m agent_modules.command_agent.command_agent_example

# Test del procesador de comandos
python agent_modules/command_agent/test_command_processor.py "comando a ejecutar"

# Modo interactivo
python agent_modules/command_agent/test_command_processor.py
```

### 2. Scripts Principales

#### Script de Inicialización
```bash
# Crear estructura de base de datos
python -m scripts.init_bodega_db
```

#### Agente Simplificado
```bash
# Modo interactivo simple
python simple_db_agent.py --interactive

# Consulta única
python simple_db_agent.py --prompt "Tu consulta en lenguaje natural"
```

#### Sistema Principal
```bash
# Ejecución principal
python main.py --help

# Listar proveedores disponibles
python main.py --list-providers

# Información del sistema
python main.py --info

# Generar texto con proveedor específico
python main.py --provider openai --prompt "Texto a generar"

# Interfaz Streamlit para bodega
python main_bodega.py
```

### 3. Scripts de Prueba y Diagnóstico

#### Tests de Conexión
```bash
# Test de conexión MySQL
python agent_modules/db_agent/db_connection_test.py

# Detector de sistema
python -m utils.db_system_detector
```

#### CrewAI y Orquestación
```bash
# Análisis con CrewAI
python scripts/run_crew_analysis.py --detect-only

# Análisis con prompt específico
python scripts/run_crew_analysis.py --prompt "Analiza el inventario"

# Guardar resultado
python scripts/run_crew_analysis.py --prompt "Tu consulta" --output resultado.txt

# Adaptador CrewAI para DB
python scripts/db_agent_crew_adapter.py --prompt "Tu consulta" --provider claude
```

### 4. Frontend

#### Comandos NPM
```bash
# Instalar dependencias
cd frontend
npm install

# Ejecutar en desarrollo
npm run dev

# Construir para producción
npm build

# Preview de la build
npm preview
```

### 5. Notebooks y VS Code

#### Ejecutar notebooks
```bash
# Navegar al directorio de notebooks
cd notebooks/bodega_test

# Abrir notebook directamente en VS Code
code bodega_test.ipynb

# Alternativamente, abrir VS Code en el directorio de notebooks
code .
```

## 🔧 Configuraciones y Modos

### Variables de Entorno (.env)

```env
# MySQL
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
MYSQL_DATABASE=bodega_inventory

# API Keys
OPENAI_API_KEY=tu_clave_openai
ANTHROPIC_API_KEY=tu_clave_claude
GOOGLE_CLOUD_API_KEY=tu_clave_google

# Red (opcional)
WIFI_SSID=tu_red
WIFI_PASSWORD=tu_password
```

### Configuración de Proveedores (config/settings.yaml)

```yaml
default_provider: openai

providers:
  ollama:
    base_url: http://localhost:11434
    default_model: gemma3:1b
  
  openai:
    api_key: ${OPENAI_API_KEY}
    base_url: https://api.openai.com/v1
    default_model: gpt-3.5-turbo
  
  claude:
    api_key: ${ANTHROPIC_API_KEY}
    base_url: https://api.anthropic.com/v1
    default_model: claude-3-haiku-20240307
```

## 🚀 Modos de Operación

### 1. Modo Interactivo

#### DB Agent
```bash
python -m agent_modules.db_agent.agent --interactive

# Consultas disponibles:
🔍 Consulta: ¿Cuántos productos hay?
🔍 Consulta: SHOW TABLES
🔍 Consulta: reset  # Limpia caché
🔍 Consulta: salir  # Termina sesión
```

#### Command Processor
```bash
python agent_modules/command_agent/test_command_processor.py

# Comandos disponibles:
🧠 > ayuda
🧠 > usar claude
🧠 > generar Explica qué es Python
🧠 > listar proveedores
🧠 > resumen [texto]
🧠 > traducir [texto]
🧠 > salir
```

### 2. Modo Línea de Comandos

```bash
# Consulta directa
python simple_db_agent.py --prompt "¿Qué productos hay?"

# Con configuración específica
python -m agent_modules.db_agent.agent \
  --prompt "Tu consulta" \
  --type mysql \
  --host 127.0.0.1 \
  --port 3307
```

### 3. Modo Interface Web

```bash
# Frontend Vue
cd frontend
npm run dev
# Abre http://localhost:5173

# Streamlit
python main_bodega.py
# Abre http://localhost:8501
```

## 📦 Flujo de Trabajo Típico

### 1. Inicialización
```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar .env
cp .env-example .env

# 4. Inicializar DB
python -m scripts.init_bodega_db
```

### 2. Operaciones Comunes

#### Consultar Inventario
```bash
# Interactivo
python -m agent_modules.bodega_agent.agent --interactive

# Consultas rápidas
"ver inventario completo"
"productos con stock bajo"
"alertas de stock crítico"
```

#### Registrar Movimientos
```bash
# A través del frontend
cd frontend && npm run dev

# O con el agente
"registrar entrada de productos"
"registrar salida de productos"
```

#### Analizar Datos
```bash
# CrewAI para análisis profundo
python scripts/run_crew_analysis.py --prompt "Analiza patrones de venta"

# Consultas SQL directas
python simple_db_agent.py --interactive
```

### 3. Monitoreo y Reportes

```bash
# Verificar estado del sistema
python -m utils.db_system_detector

# Generar reportes
"generar reporte de ventas del mes"
"reporte de productos más vendidos"
"análisis de stock crítico"
```

## ⚠️ Solución de Problemas

### Error de Módulo No Encontrado
```bash
# Error: ModuleNotFoundError
# Solución: Ejecutar desde raíz del proyecto
cd /path/to/bodega_app
python -m module.path

# O agregar al script:
import sys
sys.path.insert(0, "/path/to/bodega_app")
```

### Error de Conexión MySQL
```bash
# Verificar conexión
python agent_modules/db_agent/db_connection_test.py

# Verificar variables de entorno
cat .env | grep MYSQL
```

### Error de API Key
```bash
# Verificar claves
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY'))"
```

## 📚 Referencias Rápidas

### Frontend
- Libro de Ventas: Registro de transacciones
- Libro Diario: Asientos contables
- Inventario: Gestión de productos
- Lista de Productos: Visualización de stock

### Agentes
- DBAgent: Consultas SQL en lenguaje natural
- BodegaAgent: Operaciones específicas de inventario
- CommandAgent: Procesamiento de comandos

### Base de Datos
- bodega_inventory: BD principal
- productos: Tabla de productos
- movimientos: Historial de movimientos
- ventas: Registro de ventas