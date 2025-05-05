#!/usr/bin/env python3
import streamlit as st
from providers.provider_manager import ProviderManager
from agent_modules.bodega_agent.agent import BodegaAgent

def main():
    st.title("🏬 Sistema de Gestión de Bodega")
    
    # Cargar configuración
    manager = ProviderManager("config/settings.yaml")
    bodega_agent = BodegaAgent(provider_manager=manager)
    
    # Interfaz de usuario
    st.sidebar.header("Operaciones")
    operation = st.sidebar.selectbox(
        "Selecciona una operación:",
        [
            "Ver inventario completo",
            "Buscar producto por código",
            "Registrar entrada de productos",
            "Registrar salida de productos",
            "Alertas de stock bajo",
            "Generar reporte de movimientos"
        ]
    )
    
    # Input personalizado según operación
    if operation == "Buscar producto por código":
        codigo = st.text_input("Código del producto:")
        if st.button("Buscar"):
            result = bodega_agent.run({"prompt": f"Buscar producto con código {codigo}"})
            st.write(result)
    
    elif operation == "Registrar entrada de productos":
        col1, col2 = st.columns(2)
        with col1:
            codigo = st.text_input("Código:")
            nombre = st.text_input("Nombre:")
            categoria = st.text_input("Categoría:")
            precio = st.number_input("Precio:", min_value=0.0)
        with col2:
            stock = st.number_input("Cantidad:", min_value=1)
            stock_min = st.number_input("Stock mínimo:", min_value=1)
            ubicacion = st.text_input("Ubicación:")
            motivo = st.text_input("Motivo de entrada:")
        
        if st.button("Registrar Entrada"):
            prompt = f"""
            Registrar entrada de producto: 
            Código: {codigo}
            Nombre: {nombre}
            Categoría: {categoria}
            Precio: {precio}
            Stock: {stock}
            Stock mínimo: {stock_min}
            Ubicación: {ubicacion}
            Motivo: {motivo}
            """
            result = bodega_agent.run({"prompt": prompt})
            st.success(f"Producto registrado: {result}")
    
    else:
        # Operaciones automáticas
        if st.button(f"Ejecutar: {operation}"):
            result = bodega_agent.run({"prompt": operation})
            st.write(result)
            
            # Mostrar alertas de stock bajo
            if result.get("results"):
                for item in result["results"]:
                    if isinstance(item, dict) and item.get("stock_actual", 0) < item.get("stock_minimo", 0):
                        st.warning(f"⚠️ Stock bajo: {item.get('nombre', 'N/A')} - Actual: {item.get('stock_actual', 0)}")

if __name__ == "__main__":
    main()
