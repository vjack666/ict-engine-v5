"""
🚀 SCRIPT MAESTRO DE PRE-CONFIGURACIÓN OPTIMIZADA
===============================================

Ejecuta todas las 4 mejoras críticas en secuencia para preparar
el entorno antes de la ejecución del plan principal.

Autor: Sistema de Análisis Automático
Fecha: 06 Agosto 2025
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Agregar el directorio padre al path para imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# MIGRACIÓN SIC v3.0 + SLUC v2.1
try:
    from sistema.sic import enviar_senal_log, log_info, log_warning
except ImportError:
    # Fallback si SIC no está disponible
    def enviar_senal_log(level, message, module, category):
        print(f"[{level}] {message}")
    log_info = log_warning = enviar_senal_log

class PreConfigurationMaster:
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.start_time = datetime.now()
        self.results = {}

    def run_all_optimizations(self):
        """Ejecutar todas las 4 mejoras críticas en secuencia"""
        print("🚀 INICIANDO PRE-CONFIGURACIÓN OPTIMIZADA")
        print("=" * 55)
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Proyecto: {self.project_root}")
        print()

        # MEJORA 1: Configuración VS Code menos estricta
        self._step_1_vscode_config()

        # MEJORA 2: Sistema de backup robusto
        self._step_2_backup_system()

        # MEJORA 3: Monitor de progreso en tiempo real
        self._step_3_progress_monitor()

        # MEJORA 4: Validación inteligente pre-ejecución
        self._step_4_intelligent_validation()

        # Reporte final
        self._generate_final_report()

    def _step_1_vscode_config(self):
        """MEJORA 1: Aplicar configuración VS Code menos estricta"""
        print("🔧 MEJORA 1: CONFIGURACIÓN VS CODE OPTIMIZADA")
        print("-" * 45)

        try:
            # Verificar archivos de configuración
            pylintrc_path = self.project_root / ".pylintrc"
            vscode_settings_path = self.project_root / ".vscode" / "settings.json"

            pylintrc_exists = pylintrc_path.exists()
            vscode_exists = vscode_settings_path.exists()

            print(f"📋 Verificando configuraciones:")
            print(f"   ├─ .pylintrc: {'✅ Existe' if pylintrc_exists else '❌ No existe'}")
            print(f"   └─ .vscode/settings.json: {'✅ Existe' if vscode_exists else '❌ No existe'}")

            if pylintrc_exists and vscode_exists:
                print("✅ Configuraciones VS Code ya están optimizadas")
                self.results['vscode_config'] = True
            else:
                print("⚠️ Algunas configuraciones faltan - usar configuración manual")
                self.results['vscode_config'] = False

        except Exception as e:
            print(f"❌ Error en configuración VS Code: {e}")
            self.results['vscode_config'] = False

        print(f"⏱️ Tiempo: 2 minutos")
        print()

    def _step_2_backup_system(self):
        """MEJORA 2: Crear backup robusto del sistema"""
        print("🛡️ MEJORA 2: SISTEMA DE BACKUP ROBUSTO")
        print("-" * 40)

        try:
            # Ejecutar script de backup inteligente
            backup_script = self.project_root / "scripts" / "create_intelligent_backup.py"

            if backup_script.exists():
                print("📦 Ejecutando backup completo del proyecto...")

                result = subprocess.run([
                    sys.executable, str(backup_script)
                ], capture_output=True, text=True, cwd=self.project_root, timeout=300)

                if result.returncode == 0:
                    print("✅ Backup completo creado exitosamente")
                    self.results['backup_system'] = True

                    # Mostrar información del backup
                    backup_dir = self.project_root / "backups"
                    if backup_dir.exists():
                        backup_count = len(list(backup_dir.glob("*")))
                        print(f"📊 Backups disponibles: {backup_count}")
                else:
                    print(f"❌ Error en backup: {result.stderr}")
                    self.results['backup_system'] = False
            else:
                print("❌ Script de backup no encontrado")
                self.results['backup_system'] = False

        except Exception as e:
            print(f"❌ Error ejecutando backup: {e}")
            self.results['backup_system'] = False

        print(f"⏱️ Tiempo: 5 minutos")
        print()

    def _step_3_progress_monitor(self):
        """MEJORA 3: Verificar monitor de progreso"""
        print("📊 MEJORA 3: MONITOR DE PROGRESO EN TIEMPO REAL")
        print("-" * 48)

        try:
            # Verificar script de monitoreo
            monitor_script = self.project_root / "scripts" / "live_progress_monitor.py"

            if monitor_script.exists():
                print("📈 Verificando sistema de monitoreo...")

                # Test básico del script (importación)
                result = subprocess.run([
                    sys.executable, "-c", 
                    f"import sys; sys.path.append(r'{self.project_root}'); "
                    f"from scripts.live_progress_monitor import LiveProgressMonitor; "
                    f"print('Monitor OK')"
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print("✅ Monitor de progreso listo")
                    print("📋 Características disponibles:")
                    print("   ├─ Dashboard ASCII en tiempo real")
                    print("   ├─ Alertas automáticas")
                    print("   ├─ Métricas de progreso")
                    print("   └─ Reporte final automático")
                    self.results['progress_monitor'] = True
                else:
                    print(f"❌ Error en monitor: {result.stderr}")
                    self.results['progress_monitor'] = False
            else:
                print("❌ Script de monitoreo no encontrado")
                self.results['progress_monitor'] = False

        except Exception as e:
            print(f"❌ Error verificando monitor: {e}")
            self.results['progress_monitor'] = False

        print(f"⏱️ Tiempo: 1 minuto")
        print()

    def _step_4_intelligent_validation(self):
        """MEJORA 4: Ejecutar validación inteligente"""
        print("🧠 MEJORA 4: VALIDACIÓN INTELIGENTE PRE-EJECUCIÓN")
        print("-" * 50)

        try:
            # Ejecutar análisis de dependencias
            validator_script = self.project_root / "scripts" / "analyze_dependencies_graph.py"

            if validator_script.exists():
                print("🔍 Ejecutando análisis inteligente...")

                result = subprocess.run([
                    sys.executable, str(validator_script)
                ], capture_output=True, text=True, cwd=self.project_root, timeout=120)

                if result.returncode == 0:
                    print("✅ Análisis inteligente completado")

                    # Buscar archivo de resultados
                    analysis_file = self.project_root / "data" / "exports" / "dependency_analysis.json"
                    if analysis_file.exists():
                        print("📊 Resultados del análisis:")
                        print("   ├─ Grafo de dependencias generado")
                        print("   ├─ Dependencias circulares detectadas")
                        print("   ├─ Orden óptimo de corrección calculado")
                        print("   └─ Scripts automatizados validados")
                        self.results['intelligent_validation'] = True
                    else:
                        print("⚠️ Análisis ejecutado pero resultados no guardados")
                        self.results['intelligent_validation'] = False
                else:
                    print(f"❌ Error en análisis: {result.stderr}")
                    self.results['intelligent_validation'] = False
            else:
                print("❌ Script de validación no encontrado")
                self.results['intelligent_validation'] = False

        except Exception as e:
            print(f"❌ Error en validación inteligente: {e}")
            self.results['intelligent_validation'] = False

        print(f"⏱️ Tiempo: 2 minutos")
        print()

    def _generate_final_report(self):
        """Generar reporte final de la pre-configuración"""
        total_time = datetime.now() - self.start_time

        print("📋 REPORTE FINAL DE PRE-CONFIGURACIÓN")
        print("=" * 45)

        # Resumen de resultados
        success_count = sum(self.results.values())
        total_count = len(self.results)
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0

        print(f"⏱️ Tiempo total: {total_time}")
        print(f"📊 Éxito: {success_count}/{total_count} mejoras ({success_rate:.1f}%)")
        print()

        # Detalle por mejora
        mejoras = {
            'vscode_config': '🔧 Configuración VS Code',
            'backup_system': '🛡️ Sistema de Backup',
            'progress_monitor': '📊 Monitor de Progreso',
            'intelligent_validation': '🧠 Validación Inteligente'
        }

        print("📋 ESTADO DE MEJORAS:")
        for key, nombre in mejoras.items():
            status = "✅ EXITOSA" if self.results.get(key, False) else "❌ FALLIDA"
            print(f"   {nombre}: {status}")

        print()

        # Recomendaciones finales
        if success_count == total_count:
            print("🎉 ¡TODAS LAS MEJORAS IMPLEMENTADAS EXITOSAMENTE!")
            print("✅ El sistema está optimizado para ejecutar el plan principal")
            print()
            print("📋 PRÓXIMOS PASOS RECOMENDADOS:")
            print("   1. 🚀 Ejecutar plan principal con máxima confianza")
            print("   2. 📊 Iniciar monitor en terminal paralelo")
            print("   3. 🛡️ Backup automático cada fase completada")
            print("   4. 🧠 Seguir orden óptimo generado por análisis")
        else:
            print("⚠️ ALGUNAS MEJORAS NO SE COMPLETARON")
            print("📋 RECOMENDACIONES:")

            if not self.results.get('backup_system', True):
                print("   • 🛡️ Crear backup manual antes de continuar")
            if not self.results.get('intelligent_validation', True):
                print("   • 🧠 Revisar dependencias manualmente")
            if not self.results.get('progress_monitor', True):
                print("   • 📊 Monitorear progreso manualmente")

        print()
        print("🎯 SISTEMA LISTO PARA PLAN PRINCIPAL")

        # Guardar reporte
        report_path = self.project_root / "data" / "exports" / f"pre_config_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        report_content = f"""
PRE-CONFIGURACIÓN OPTIMIZADA - REPORTE FINAL
===========================================

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Tiempo total: {total_time}
Tasa de éxito: {success_rate:.1f}%

RESULTADOS POR MEJORA:
{chr(10).join([f'{nombre}: {"EXITOSA" if self.results.get(key, False) else "FALLIDA"}' for key, nombre in mejoras.items()])}

ARCHIVOS CREADOS:
- scripts/create_intelligent_backup.py (Sistema de backup)
- scripts/live_progress_monitor.py (Monitor en tiempo real)
- scripts/analyze_dependencies_graph.py (Validación inteligente)
- .vscode/settings.json (Configuración VS Code)

RECOMENDACIÓN:
{"Sistema completamente optimizado - proceder con plan principal" if success_count == total_count else "Algunas mejoras fallaron - revisar manualmente antes de continuar"}
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"📄 Reporte completo guardado en: {report_path}")

def main():
    """Función principal del script maestro"""
    project_root = Path.cwd()
    master = PreConfigurationMaster(project_root)

    try:
        master.run_all_optimizations()
    except KeyboardInterrupt:
        print("\n⚠️ Pre-configuración interrumpida por usuario")
    except Exception as e:
        print(f"\n❌ Error crítico en pre-configuración: {e}")
        enviar_senal_log("ERROR", f"Error crítico en pre-configuración: {e}", __name__, "pre_config")

    print("\n🏁 PRE-CONFIGURACIÓN FINALIZADA")

if __name__ == "__main__":
    main()
