#!/usr/bin/env python3
import os
import sys
from utils.db_system_detector import run as detect_system
from agent_modules.db_agent.agent import DBAgent
from providers.provider_manager import ProviderManager

def init_bodega_db():
    """Inicializa la base de datos para la bodega"""
    
    # Detectar sistema
    system_info = detect_system()
    
    # Cargar proveedor
    manager = ProviderManager("config/settings.yaml")
    db_agent = DBAgent(provider_manager=manager)
    
    # Crear estructura de base de datos
    create_tables_sql = """
    CREATE DATABASE IF NOT EXISTS bodega_inventory;
    USE bodega_inventory;
    
    CREATE TABLE IF NOT EXISTS productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        codigo VARCHAR(50) UNIQUE,
        nombre VARCHAR(255),
        descripcion TEXT,
        categoria VARCHAR(100),
        precio DECIMAL(10,2),
        stock_actual INT,
        stock_minimo INT,
        ubicacion VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS movimientos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        producto_id INT,
        tipo_movimiento ENUM('entrada', 'salida'),
        cantidad INT,
        motivo VARCHAR(255),
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    );
    """
    
    print("Creando estructura de base de datos...")
    # Ejecutar SQL
    results = db_agent.run({
        "prompt": create_tables_sql,
        "connection": {"type": "mysql"}
    })
    
    print("Base de datos inicializada!")

if __name__ == "__main__":
    init_bodega_db()
