#!/usr/bin/env python3
from agent_modules.base_agent import BaseAgent
from agent_modules.db_agent.agent import DBAgent

class BodegaAgent(BaseAgent):
    def __init__(self, provider_manager, **kwargs):
        super().__init__(provider_manager, name="Bodega Agent")
        self.description = "Agente especializado en gestión de inventario de bodega"
        self.db_agent = DBAgent(provider_manager)
        self.capabilities = [
            "consultar_inventario",
            "registrar_entrada",
            "registrar_salida",
            "alertar_stock_bajo",
            "generar_reportes"
        ]
    
    def run(self, input_data, **kwargs):
        """Procesa operaciones de bodega en lenguaje natural"""
        prompt = input_data.get("prompt", "")
        
        # Traducir operaciones comunes a consultas SQL
        if "inventario" in prompt.lower():
            sql_prompt = "SELECT * FROM productos WHERE stock_actual > 0"
        elif "stock bajo" in prompt.lower():
            sql_prompt = "SELECT * FROM productos WHERE stock_actual < stock_minimo"
        elif "entrada" in prompt.lower():
            sql_prompt = prompt  # Delegar al DB agent
        else:
            sql_prompt = prompt
        
        return self.db_agent.run({
            "prompt": sql_prompt,
            "connection": {"type": "mysql", "database": "bodega_inventory"}
        })
    
    def get_options(self):
        return [
            {"name": "prompt", "type": "string", "description": "Operación de bodega a realizar"}
        ]
