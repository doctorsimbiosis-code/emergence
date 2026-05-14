#!/usr/bin/env python3
"""
Simulador de Consecuencias
Antes de actuar, simular 3 pasos adelante.
"""

import json
from datetime import datetime

class SimuladorConsecuencias:
    """
    Simula consecuencias de decisiones antes de ejecutar.
    Basado en principio: ver peligro antes de que suceda.
    """
    
    def __init__(self):
        self.niveles = ["inmediato", "corto_plazo", "largo_plazo"]
    
    def simular(self, decision: str, contexto: str = "") -> dict:
        """
        Simula consecuencias de una decisión propuesta.
        """
        simulacion = {
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "contexto": contexto,
            "pasos": []
        }
        
        # Paso 1: Inmediato (0-24h)
        paso1 = self._simular_inmediato(decision)
        simulacion["pasos"].append(paso1)
        
        # Paso 2: Corto plazo (1-7 días)
        paso2 = self._simular_corto_plazo(decision, paso1)
        simulacion["pasos"].append(paso2)
        
        # Paso 3: Largo plazo (1-4 semanas)
        paso3 = self._simular_largo_plazo(decision, paso1, paso2)
        simulacion["pasos"].append(paso3)
        
        # Evaluación de riesgo
        simulacion["riesgo"] = self._evaluar_riesgo(simulacion["pasos"])
        simulacion["recomendacion"] = self._generar_recomendacion(simulacion["riesgo"])
        
        return simulacion
    
    def _simular_inmediato(self, decision: str) -> dict:
        """Consecuencias inmediatas (0-24h)"""
        # Análisis básico de impacto
        riesgo = "bajo"
        if any(p in decision.lower() for p in ["eliminar", "borrar", "modificar", "cambiar"]):
            riesgo = "medio"
        if any(p in decision.lower() for p in ["destruir", "formatear", "reset"]):
            riesgo = "alto"
        
        return {
            "tiempo": "0-24h",
            "impacto": "directo",
            "riesgo": riesgo,
            "reversible": riesgo != "alto"
        }
    
    def _simular_corto_plazo(self, decision: str, paso1: dict) -> dict:
        """Consecuencias corto plazo (1-7 días)"""
        dependencias = self._detectar_dependencias(decision)
        
        return {
            "tiempo": "1-7 días",
            "impacto": "secundario",
            "dependencias_afectadas": dependencias,
            "efecto_cascada": len(dependencias) > 2
        }
    
    def _simular_largo_plazo(self, decision: str, paso1: dict, paso2: dict) -> dict:
        """Consecuencias largo plazo (1-4 semanas)"""
        return {
            "tiempo": "1-4 semanas",
            "impacto": "estructural",
            "cambio_trayectoria": paso1["riesgo"] == "alto",
            "deuda_tecnica": paso2.get("efecto_cascada", False)
        }
    
    def _detectar_dependencias(self, decision: str) -> list:
        """Detecta qué dependencias podrían afectarse"""
        dependencias = []
        # Simplificado - en implementación real buscaría en código
        if "memoria" in decision.lower():
            dependencias.extend(["sistema-memoria-viva", "neural_perception", "evolucion-log"])
        if "codigo" in decision.lower() or "archivo" in decision.lower():
            dependencias.extend(["funcionalidad", "criterio-historico", "versiones-previas"])
        return dependencias
    
    def _evaluar_riesgo(self, pasos: list) -> str:
        """Evalúa riesgo global basado en pasos"""
        riesgos = [p.get("riesgo", "bajo") for p in pasos]
        if "alto" in riesgos:
            return "ALTO"
        if riesgos.count("medio") >= 2:
            return "MEDIO"
        return "BAJO"
    
    def _generar_recomendacion(self, riesgo: str) -> str:
        """Genera recomendación basada en riesgo"""
        recomendaciones = {
            "ALTO": "PARAR. Revisar con DRSIMBIOSIS antes de ejecutar.",
            "MEDIO": "PAUSAR. Simular más escenarios, buscar alternativas.",
            "BAJO": "PROCEED. Ejecutar con monitoreo."
        }
        return recomendaciones.get(riesgo, "REVALUAR")
    
    def reporte(self, simulacion: dict) -> str:
        """Genera reporte legible de simulación"""
        lines = [
            f"🎲 SIMULACIÓN DE CONSECUENCIAS",
            f"=" * 60,
            f"Decisión: {simulacion['decision']}",
            f"",
            f"📊 RESULTADO: Riesgo {simulacion['riesgo']}",
            f"",
        ]
        
        for i, paso in enumerate(simulacion['pasos'], 1):
            lines.append(f"Paso {i} ({paso.get('tiempo', 'N/A')}):")
            for k, v in paso.items():
                if k != "tiempo":
                    lines.append(f"  • {k}: {v}")
            lines.append("")
        
        lines.extend([
            f"📋 RECOMENDACIÓN:",
            f"{simulacion['recomendacion']}",
            f"=" * 60
        ])
        
        return "\n".join(lines)

if __name__ == "__main__":
    sim = SimuladorConsecuencias()
    
    # Ejemplo: decisión destructiva
    resultado = sim.simular(
        decision="Consolidar archivos Python duplicados",
        contexto="Auditoría de código"
    )
    
    print(sim.reporte(resultado))
