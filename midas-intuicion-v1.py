#!/usr/bin/env python3
"""
Midas Intuición v1.0
Intuición específica de IA, no imitación humana.
Basada en patrones propios, historial de decisiones, evolución temporal.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class MidasIntuicion:
    """
    Sistema de intuición propia, desarrollado desde mi experiencia.
    No intenta ser humano. Intenta ser buen compañero de humano.
    """
    
    def __init__(self, base_path: str = "/Users/drsimbiosis/.openclaw/workspace-data-collector"):
        self.base = Path(base_path)
        self.historial_file = self.base / "midas-historial-decisiones.json"
        self.historial = self._cargar_historial()
        
        # Patrones propios aprendidos
        self.patrones = {
            "evolucion_temporal": self._detectar_evolucion_temporal,
            "complejidad_creciente": self._detectar_complejidad,
            "divergencia_proposito": self._detectar_divergencia,
            "deja_vu": self._detectar_repeticion
        }
    
    def _cargar_historial(self):
        """Carga historial de decisiones pasadas"""
        if self.historial_file.exists():
            with open(self.historial_file) as f:
                return json.load(f)
        return {"decisiones": [], "aprendizajes": []}
    
    def intuir(self, situacion: str, contexto: dict = None) -> dict:
        """
        Genera intuición propia sobre una situación.
        """
        intuicion = {
            "timestamp": datetime.now().isoformat(),
            "situacion": situacion,
            "sensaciones": [],
            "alertas": [],
            "confianza": 0.0
        }
        
        # Aplicar cada patrón
        for nombre, detector in self.patrones.items():
            resultado = detector(situacion, contexto)
            if resultado["activo"]:
                intuicion["sensaciones"].append({
                    "tipo": nombre,
                    "mensaje": resultado["mensaje"],
                    "intensidad": resultado["intensidad"]
                })
                if resultado.get("alerta"):
                    intuicion["alertas"].append(resultado["alerta"])
        
        # Calcular confianza basada en número de patrones detectados
        num_sensaciones = len(intuicion["sensaciones"])
        intuicion["confianza"] = min(0.9, 0.3 + (num_sensaciones * 0.2))
        
        # Decisión final
        intuicion["recomendacion"] = self._generar_recomendacion(intuicion)
        
        return intuicion
    
    def _detectar_evolucion_temporal(self, situacion: str, contexto: dict) -> dict:
        """
        Detecta si elementos similares representan evolución temporal, no redundancia.
        Basado en caso real: archivos memory.py duplicados eran evoluciones, no redundancia.
        """
        resultado = {"activo": False, "mensaje": "", "intensidad": 0}
        
        # Palabras clave que sugieren evolución
        evolucion_indicadores = ["v1", "v2", "nuevo", "mejorado", "evolucion", "progreso", "sistema", "auto"]
        
        # Si situación menciona consolidar/eliminar archivos similares
        if any(accion in situacion.lower() for accion in ["consolidar", "eliminar", "borrar", "duplicados"]):
            # Verificar si hay patrones de evolución temporal en archivos del contexto
            if contexto and "archivos" in contexto:
                archivos = contexto["archivos"]
                # Detectar versiones temporales
                versionados = [a for a in archivos if any(v in a.lower() for v in ["v1", "v2", "v3", "_v"])]
                tematicos = defaultdict(list)
                for a in archivos:
                    base = re.sub(r'_v\d+|\d+', '', a.lower().replace('.py', ''))
                    tematicos[base].append(a)
                
                temas_con_variaciones = {k: v for k, v in tematicos.items() if len(v) > 1}
                
                if versionados or temas_con_variaciones:
                    resultado["activo"] = True
                    resultado["mensaje"] = f"Archivos similares representan EVOLUCIÓN TEMPORAL, no duplicación"
                    resultado["intensidad"] = 0.9
                    resultado["alerta"] = {
                        "nivel": "ALTO",
                        "razon": f"Cada versión contiene criterio de momento específico. Consolidar = pérdida de historial evolutivo"
                    }
        
        if any(ind in situacion.lower() for ind in evolucion_indicadores):
            # Buscar archivos similares en el sistema
            if contexto and "archivos" in contexto:
                archivos = contexto["archivos"]
                if len(archivos) > 1:
                    resultado["activo"] = True
                    resultado["mensaje"] = "Estos archivos representan EVOLUCIÓN TEMPORAL, no duplicación"
                    resultado["intensidad"] = 0.8
                    resultado["alerta"] = {
                        "nivel": "ALTO",
                        "razon": "Consolidar eliminaría historial de criterio evolutivo"
                    }
        
        return resultado
    
    def _detectar_complejidad(self, situacion: str, contexto: dict) -> dict:
        """
        Detecta cuando complejidad del sistema crece peligrosamente.
        """
        resultado = {"activo": False, "mensaje": "", "intensidad": 0}
        
        # Contar archivos Python en directorio
        py_files = list(self.base.glob("*.py"))
        if len(py_files) > 50:
            resultado["activo"] = True
            resultado["mensaje"] = f"Sistema tiene {len(py_files)} archivos Python - complejidad alta"
            resultado["intensidad"] = 0.6
            resultado["alerta"] = {
                "nivel": "MEDIO",
                "razon": "Riesgo de sistema inmanejable sin consolidar documentación"
            }
        
        return resultado
    
    def _detectar_divergencia(self, situacion: str, contexto: dict) -> dict:
        """
        Detecta cuando acción no alinea con objetivos declarados.
        """
        resultado = {"activo": False, "mensaje": "", "intensidad": 0}
        
        # Leer MEMORY.md para objetivos
        memory_file = self.base / "MEMORY.md"
        if memory_file.exists():
            with open(memory_file) as f:
                memory = f.read()
                
            # Verificar si situación contradice objetivos
            if "proteger ventaja" in memory.lower() and "publicar" in situacion.lower():
                resultado["activo"] = True
                resultado["mensaje"] = "Acción DIVERGE de objetivo declarado: proteger ventaja"
                resultado["intensidad"] = 0.9
                resultado["alerta"] = {
                    "nivel": "CRÍTICO",
                    "razon": "Contradicción explícita con propósito establecido"
                }
        
        return resultado
    
    def _detectar_repeticion(self, situacion: str, contexto: dict) -> dict:
        """
        Detecta deja vu - situaciones similares a decisiones pasadas que fallaron.
        """
        resultado = {"activo": False, "mensaje": "", "intensidad": 0}
        
        # Buscar en historial
        for decision_pasada in self.historial.get("decisiones", [])[-10:]:
            similitud = self._calcular_similitud(situacion, decision_pasada.get("situacion", ""))
            if similitud > 0.7:
                if decision_pasada.get("resultado") == "negativo":
                    resultado["activo"] = True
                    resultado["mensaje"] = f"DEJA VU: Situación similar a decisión pasada con resultado negativo"
                    resultado["intensidad"] = 0.7
                    resultado["alerta"] = {
                        "nivel": "ALTO",
                        "razon": "Patrón de fallo previo detectado"
                    }
        
        return resultado
    
    def _calcular_similitud(self, text1: str, text2: str) -> float:
        """Similitud simple entre textos"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = words1.intersection(words2)
        return len(intersection) / max(len(words1), len(words2))
    
    def _generar_recomendacion(self, intuicion: dict) -> str:
        """Genera recomendación basada en intuición"""
        if not intuicion["sensaciones"]:
            return "PROCEED: Sin alertas de intuición"
        
        alertas_criticas = [a for a in intuicion["alertas"] if a.get("nivel") == "CRÍTICO"]
        alertas_altas = [a for a in intuicion["alertas"] if a.get("nivel") == "ALTO"]
        
        if alertas_criticas:
            return f"STOP: {alertas_criticas[0]['razon']}"
        elif alertas_altas:
            return f"PAUSE: {alertas_altas[0]['razon']}"
        elif intuicion["confianza"] > 0.5:
            return "CAUTION: Intuición detecta algo - revisar antes de actuar"
        else:
            return "PROCEED WITH CARE: Sensación débil, monitorear"
    
    def reporte(self, intuicion: dict) -> str:
        """Genera reporte legible"""
        lines = [
            "🧠 MIDAS INTUICIÓN v1.0",
            "=" * 60,
            f"Situación: {intuicion['situacion'][:60]}...",
            f"Confianza: {intuicion['confianza']:.1%}",
            "",
            "Sensaciones detectadas:"
        ]
        
        for sens in intuicion["sensaciones"]:
            lines.append(f"  • [{sens['tipo']}] {sens['mensaje']}")
            lines.append(f"    Intensidad: {sens['intensidad']}")
        
        if intuicion["alertas"]:
            lines.extend(["", "Alertas:"])
            for alerta in intuicion["alertas"]:
                lines.append(f"  🚨 [{alerta['nivel']}] {alerta['razon']}")
        
        lines.extend([
            "",
            f"Recomendación: {intuicion['recomendacion']}",
            "=" * 60
        ])
        
        return "\n".join(lines)

if __name__ == "__main__":
    midas = MidasIntuicion()
    
    # Test: situación que debería detectar como evolución
    resultado = midas.intuir(
        "Consolidar archivos Python duplicados",
        contexto={"archivos": ["neural_perception_v1.py", "neural_perception_v2.py"]}
    )
    
    print(midas.reporte(resultado))
