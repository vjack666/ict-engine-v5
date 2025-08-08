"""
🛡️ SISTEMA DE RESPALDO ROBUSTO - PRE-EJECUCIÓN
=============================================

Sistema inteligente de backup y recovery automático para garantizar
operaciones sin riesgo durante la ejecución del plan.

Autor: Sistema de Análisis Automático
Fecha: 06 Agosto 2025
"""

import os
import json
import shutil
import hashlib
import zipfile
import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, asdict

# Agregar el directorio padre al path para imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
import sys
sys.path.insert(0, str(project_root))

# MIGRACIÓN SIC v3.0 + SLUC v2.1
try:
    from sistema.sic import enviar_senal_log, log_info, log_warning
except ImportError:
    # Fallback si SIC no está disponible
    def enviar_senal_log(level, message, module, category):
        print(f"[{level}] {module}: {message}")
    log_info = log_warning = enviar_senal_log

@dataclass
class BackupManifest:
    timestamp: str
    backup_type: str
    total_files: int
    total_size_mb: float
    checksum_map: Dict[str, str]
    critical_files: List[str]
    recovery_instructions: str

class IntelligentBackupSystem:
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.backup_root = self.project_root / "backups"
        self.current_session = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")

        # Directorios críticos a respaldar
        self.critical_dirs = [
            "sistema", "dashboard", "core", "utils",
            "config", "scripts", "data"
        ]

        # Archivos críticos específicos
        self.critical_files = [
            "sistema/sic.py",
            "sistema/logging_interface.py",
            "dashboard/dashboard_definitivo.py",
            "main.py",
            "requirements.txt"
        ]

    def create_full_backup(self, backup_name: str = None) -> Path:
        """Crear backup completo del proyecto con manifest"""
        enviar_senal_log("INFO", "🛡️ Iniciando backup completo del proyecto", __name__, "backup")

        backup_name = backup_name or f"PRE_PLAN_{self.current_session}"
        backup_dir = self.backup_root / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)

        manifest = BackupManifest(
            timestamp=self.current_session,
            backup_type="FULL",
            total_files=0,
            total_size_mb=0.0,
            checksum_map={},
            critical_files=self.critical_files.copy(),
            recovery_instructions="Use emergency_recovery.py --restore-full"
        )

        total_size = 0
        file_count = 0

        # Respaldar directorios críticos
        for dir_name in self.critical_dirs:
            source_dir = self.project_root / dir_name
            if source_dir.exists():
                target_dir = backup_dir / dir_name
                enviar_senal_log("INFO", f"📂 Respaldando directorio: {dir_name}", __name__, "backup")

                shutil.copytree(source_dir, target_dir,
                              ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))

                # Calcular checksums
                for py_file in target_dir.rglob("*.py"):
                    rel_path = str(py_file.relative_to(backup_dir))
                    checksum = self._calculate_checksum(py_file)
                    manifest.checksum_map[rel_path] = checksum

                    file_size = py_file.stat().st_size
                    total_size += file_size
                    file_count += 1

        # Respaldar archivos individuales críticos
        for file_path in self.critical_files:
            source_file = self.project_root / file_path
            if source_file.exists():
                target_file = backup_dir / file_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, target_file)

        manifest.total_files = file_count
        manifest.total_size_mb = round(total_size / (1024 * 1024), 2)

        # Guardar manifest
        manifest_path = backup_dir / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(manifest), f, indent=2, ensure_ascii=False)

        # Crear archivo comprimido
        zip_path = self.backup_root / f"{backup_name}.zip"
        self._create_zip_backup(backup_dir, zip_path)

        enviar_senal_log("INFO", f"✅ Backup completo creado: {zip_path}", __name__, "backup")
        enviar_senal_log("INFO", f"📊 {file_count} archivos, {manifest.total_size_mb} MB", __name__, "backup")

        return backup_dir

    def create_incremental_backup(self, phase_name: str) -> Path:
        """Crear backup incremental para una fase específica"""
        enviar_senal_log("INFO", f"📦 Creando backup incremental: {phase_name}", __name__, "backup")

        backup_name = f"INCREMENTAL_{phase_name}_{self.current_session}"
        backup_dir = self.backup_root / "incremental" / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Solo respaldar archivos críticos modificados recientemente
        recent_files = self._find_recently_modified_files()

        manifest = BackupManifest(
            timestamp=self.current_session,
            backup_type="INCREMENTAL",
            total_files=len(recent_files),
            total_size_mb=0.0,
            checksum_map={},
            critical_files=recent_files,
            recovery_instructions=f"Use emergency_recovery.py --restore-incremental {phase_name}"
        )

        total_size = 0
        for file_path in recent_files:
            source_file = self.project_root / file_path
            if source_file.exists():
                target_file = backup_dir / file_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, target_file)

                checksum = self._calculate_checksum(source_file)
                manifest.checksum_map[file_path] = checksum
                total_size += source_file.stat().st_size

        manifest.total_size_mb = round(total_size / (1024 * 1024), 2)

        # Guardar manifest
        manifest_path = backup_dir / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(manifest), f, indent=2, ensure_ascii=False)

        enviar_senal_log("INFO", f"✅ Backup incremental creado: {backup_dir}", __name__, "backup")
        return backup_dir

    def verify_backup_integrity(self, backup_path: Path) -> bool:
        """Verificar integridad de un backup usando checksums"""
        enviar_senal_log("INFO", f"🔍 Verificando integridad: {backup_path}", __name__, "backup")

        manifest_path = backup_path / "manifest.json"
        if not manifest_path.exists():
            enviar_senal_log("ERROR", "❌ Manifest no encontrado", __name__, "backup")
            return False

        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)

        checksum_map = manifest_data.get('checksum_map', {})

        for file_path, expected_checksum in checksum_map.items():
            full_path = backup_path / file_path
            if not full_path.exists():
                enviar_senal_log("ERROR", f"❌ Archivo faltante: {file_path}", __name__, "backup")
                return False

            actual_checksum = self._calculate_checksum(full_path)
            if actual_checksum != expected_checksum:
                enviar_senal_log("ERROR", f"❌ Checksum inválido: {file_path}", __name__, "backup")
                return False

        enviar_senal_log("INFO", "✅ Integridad del backup verificada", __name__, "backup")
        return True

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calcular checksum SHA256 de un archivo"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def _create_zip_backup(self, source_dir: Path, zip_path: Path) -> None:
        """Crear archivo ZIP del backup"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(source_dir)
                    zipf.write(file_path, arcname)

    def _find_recently_modified_files(self, hours: int = 1) -> List[str]:
        """Encontrar archivos modificados recientemente"""
        cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
        recent_files = []

        for dir_name in self.critical_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                for py_file in dir_path.rglob("*.py"):
                    mod_time = datetime.datetime.fromtimestamp(py_file.stat().st_mtime)
                    if mod_time > cutoff_time:
                        rel_path = str(py_file.relative_to(self.project_root))
                        recent_files.append(rel_path)

        return recent_files

def main():
    """Función principal para crear backup completo"""
    print("🛡️ SISTEMA DE BACKUP ROBUSTO")
    print("=" * 40)

    project_root = Path.cwd()
    backup_system = IntelligentBackupSystem(project_root)

    # Crear backup completo pre-plan
    backup_dir = backup_system.create_full_backup("PRE_PLAN_OPTIMIZADO")

    # Verificar integridad
    if backup_system.verify_backup_integrity(backup_dir):
        print("✅ Backup completo creado y verificado exitosamente")
        print(f"📂 Ubicación: {backup_dir}")
    else:
        print("❌ Error en la verificación del backup")

    print("🏁 SISTEMA DE BACKUP LISTO")

if __name__ == "__main__":
    main()
