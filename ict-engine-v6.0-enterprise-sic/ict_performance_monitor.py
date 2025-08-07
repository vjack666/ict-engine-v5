#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 ICT PERFORMANCE MONITOR v6.0
Monitor en tiempo real del rendimiento del sistema ICT
"""

import psutil
import time
import json
from datetime import datetime
from pathlib import Path

class ICTPerformanceMonitor:
    def __init__(self):
        self.monitoring = False
        self.stats = []
    
    def start_monitoring(self, interval_seconds=5):
        """Iniciar monitoreo continuo"""
        print("📊 Iniciando monitoreo de rendimiento ICT...")
        self.monitoring = True
        
        while self.monitoring:
            stats = self.collect_stats()
            self.stats.append(stats)
            
            # Mostrar stats en tiempo real
            self.display_stats(stats)
            
            # Guardar cada 60 segundos
            if len(self.stats) % 12 == 0:  # Cada 60 segundos aprox
                self.save_stats()
            
            time.sleep(interval_seconds)
    
    def collect_stats(self):
        """Recopilar estadísticas del sistema"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_used_gb': psutil.virtual_memory().used / (1024**3),
            'disk_percent': psutil.disk_usage('.').percent,
            'disk_free_gb': psutil.disk_usage('.').free / (1024**3),
            'process_count': len(psutil.pids()),
            'network_io': dict(psutil.net_io_counters()._asdict()) if psutil.net_io_counters() else {}
        }
    
    def display_stats(self, stats):
        """Mostrar estadísticas en tiempo real"""
        print(f"\r📊 CPU: {stats['cpu_percent']:.1f}% | "
              f"RAM: {stats['memory_percent']:.1f}% ({stats['memory_used_gb']:.1f}GB) | "
              f"Disk: {stats['disk_percent']:.1f}% ({stats['disk_free_gb']:.0f}GB free)", end="")
    
    def save_stats(self):
        """Guardar estadísticas a archivo"""
        logs_dir = Path("logs/performance")
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"performance_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = logs_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.stats, f, indent=2, default=str)
    
    def stop_monitoring(self):
        """Detener monitoreo"""
        self.monitoring = False
        self.save_stats()
        print("\n📊 Monitoreo detenido y stats guardadas")

if __name__ == "__main__":
    monitor = ICTPerformanceMonitor()
    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        monitor.stop_monitoring()
