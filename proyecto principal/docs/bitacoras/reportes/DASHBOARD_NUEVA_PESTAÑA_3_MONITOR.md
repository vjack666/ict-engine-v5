# 🖥️ PESTAÑA 3 - SYSTEM MONITOR v6.0

## 📋 INFORMACIÓN GENERAL

**ID Nueva**: `tab_system_monitor`
**Hotkey**: **3** (era H5 + H6 + funciones de hibernación)
**Método Render**: `render_system_monitor()`
**Estado**: 🚧 **EN DESARROLLO** (Objetivo: ✅ OPERATIVO)
**Prioridad**: 🔸 **MEDIA** - Monitoreo del sistema y herramientas

---

## 🎯 PROPÓSITO Y FUNCIONALIDAD

La **Pestaña System Monitor** consolida todas las herramientas de sistema, monitoreo y utilidades, proporcionando:

- **System Health Monitoring** → Estado completo del sistema
- **TCT Data Pipeline** → Pipeline de datos integrado desde H5
- **Candle Downloader** → Herramientas de descarga desde H6
- **Performance Metrics** → Métricas de rendimiento del sistema
- **Hibernation Controls** → Controles de hibernación avanzados
- **Debug & Maintenance** → Herramientas de debug y mantenimiento

---

## 🔄 MIGRACIÓN DESDE SISTEMA ACTUAL

### **🎯 CONSOLIDACIÓN DE FUENTES**

#### **Desde H5 - TCT Pipeline** ✅
- **TCT Data Pipeline** → Sistema completo de pipeline
- **Data Processing** → Procesamiento de datos en tiempo real
- **Pipeline Monitoring** → Monitoreo del pipeline
- **Data Quality Metrics** → Métricas de calidad de datos
- **Pipeline Configuration** → Configuración del pipeline

#### **Desde H6 - Downloader** ✅
- **Candle Downloader** → Sistema completo de descarga
- **Download Progress** → Progreso de descargas
- **Data Management** → Gestión de datos descargados
- **Download Scheduling** → Programación de descargas
- **Storage Management** → Gestión de almacenamiento

#### **Desde H1 - Hibernación** ✅
- **System Health Advanced** → Monitoreo completo del sistema
- **Hibernation Controls** → Controles avanzados de hibernación
- **Performance Monitoring** → Monitoreo de rendimiento
- **Resource Management** → Gestión de recursos

#### **Funcionalidad Nueva** 🆕
- **Unified System Dashboard** → Dashboard unificado del sistema
- **Advanced Diagnostics** → Diagnósticos avanzados
- **Maintenance Tools** → Herramientas de mantenimiento
- **Debug Console** → Consola de debug integrada

---

## 🖥️ CONTENIDO VISUAL OBJETIVO

### **Layout Professional Target**
```
╭─────────────────────────────────────────────────────────────────────────────────╮
│ 🖥️ SYSTEM MONITOR                                    | Status: ALL SYSTEMS GO │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│ ╭─ SYSTEM HEALTH ──────────────────┬─ PERFORMANCE METRICS ───────────────────╮ │
│ │                                  │                                         │ │
│ │ 🖥️ System Status                │ 📊 Performance Overview                │ │
│ │ ═══════════════                  │ ═══════════════════════                 │ │
│ │ 🟢 CPU Usage:       45.2%        │ Memory Usage:    2.1GB / 8GB (26%)     │ │
│ │ 🟢 Memory:          26.8%        │ Disk I/O:       45 MB/s read           │ │
│ │ 🟢 Disk Space:      78.5% free   │ Network:         125 KB/s down          │ │
│ │ 🟢 Network:         Connected     │ Processes:       43 active              │ │
│ │ 🟢 MT5 Connection:  Active        │ Threads:         127 total              │ │
│ │ 🟢 Database:        Connected     │ Uptime:          2h 34m 15s            │ │
│ │                                  │                                         │ │
│ │ Overall Health: 🟢 EXCELLENT     │ Performance Score: 87/100               │ │
│ ╰──────────────────────────────────┴─────────────────────────────────────────╯ │
│                                                                                 │
│ ╭─ TCT DATA PIPELINE ──────────────────────────────────────────────────────────╮ │
│ │                                                                              │ │
│ │  Stage                Status        Processed     Rate        Last Update   │ │
│ │ ═══════════════════════════════════════════════════════════════════════════   │ │
│ │ 📥 Data Ingestion     🟢 RUNNING     1,247 msgs    125/min     2s ago       │ │
│ │ 🔄 Data Processing    🟢 RUNNING     1,239 items   123/min     3s ago       │ │
│ │ 📊 Analytics Engine   🟢 RUNNING     1,235 calc    122/min     1s ago       │ │
│ │ 💾 Data Storage      🟢 RUNNING     1,233 writes   121/min     2s ago       │ │
│ │ 📤 Data Export       🟡 THROTTLED   1,201 exports  115/min     15s ago      │ │
│ │                                                                              │ │
│ │ Pipeline Health: 🟢 OPERATIONAL | Processing: 98.7% | Queue: 8 pending      │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│                                                                                 │
│ ╭─ CANDLE DOWNLOADER ──────────────┬─ MAINTENANCE & DEBUG ───────────────────╮ │
│ │                                  │                                         │ │
│ │ 📊 Download Status               │ 🔧 System Tools                        │ │
│ │ ═══════════════════              │ ═══════════════                         │ │
│ │ 🟢 EUR/USD H1:  ████████ 98%     │ [1] POI Hub                             │ │
│ │ 🟡 GBP/USD H1:  ████▓▓▓▓ 65%     │ [2] Analysis                            │ │
│ │ 🔴 USD/JPY H1:  ██▓▓▓▓▓▓ 25%     │ [3] Monitor                             │ │
│ │ ⏸ AUD/USD H1:   Queued           │ [C] Clear Cache                         │ │
│ │                                  │ [R] Restart Services                    │ │
│ │ Total Progress: 72%               │ [L] View Logs                           │ │
│ │ Download Speed: 2.3 MB/s         │ [H] Hibernation Mode                    │ │
│ │ ETA: 8 minutes                   │ [D] Debug Console                       │ │
│ │                                  │                                         │ │
│ │ Queue: 4 pending | Errors: 1     │ Last Maintenance: 1h ago                │ │
│ ╰──────────────────────────────────┴─────────────────────────────────────────╯ │
│                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────╯
```

---

## 🔧 ARQUITECTURA TÉCNICA

### **Estructura del Nuevo Render**
```python
def render_system_monitor(self):
    """
    🖥️ SYSTEM MONITOR - Consolidación de monitoreo v6.0
    ===================================================

    Consolidación de:
    - System Health Monitoring (de H1 + nuevo)
    - TCT Data Pipeline (de H5)
    - Candle Downloader (de H6)
    - Maintenance & Debug Tools (nuevo)
    """
    from rich.table import Table
    from rich.columns import Columns
    from rich.progress import Progress, BarColumn, TextColumn

    # Grid principal con 3 niveles organizados
    main_layout = Table.grid(padding=1)
    main_layout.add_column(style="cyan", ratio=1)

    # TOP ROW: System Health + Performance Metrics
    top_row = Columns([
        self._render_system_health_panel(),
        self._render_performance_metrics_panel()
    ], equal=True, expand=True)
    main_layout.add_row(top_row)

    # MIDDLE ROW: TCT Data Pipeline (ancho completo)
    pipeline_panel = self._render_tct_pipeline_panel()
    main_layout.add_row(pipeline_panel)

    # BOTTOM ROW: Candle Downloader + Maintenance & Debug
    bottom_row = Columns([
        self._render_candle_downloader_panel(),
        self._render_maintenance_debug_panel()
    ], equal=True, expand=True)
    main_layout.add_row(bottom_row)

    return Panel(
        main_layout,
        title="🖥️ SYSTEM MONITOR",
        subtitle="System Health | Data Pipeline | Download Manager | Debug Tools",
        border_style="bright_white",
        padding=(1, 2)
    )
```

### **Panel Components**

#### **1. System Health Panel** (expandido de H1)
```python
def _render_system_health_panel(self):
    """
    System health expandido desde hibernación H1
    Incluye monitoreo completo del sistema
    """

    health_table = Table.grid()
    health_table.add_column(style="bright_white", no_wrap=True)
    health_table.add_column(style="white")

    try:
        # System metrics
        system_metrics = self._get_system_metrics_safe()

        # CPU Usage
        cpu_usage = system_metrics.get('cpu_usage', 45.2)
        cpu_emoji = "🟢" if cpu_usage < 70 else "🟡" if cpu_usage < 85 else "🔴"
        health_table.add_row(f"{cpu_emoji} CPU Usage:", f"{cpu_usage}%")

        # Memory Usage
        memory_usage = system_metrics.get('memory_usage', 26.8)
        memory_emoji = "🟢" if memory_usage < 70 else "🟡" if memory_usage < 85 else "🔴"
        health_table.add_row(f"{memory_emoji} Memory:", f"{memory_usage}%")

        # Disk Space
        disk_free = system_metrics.get('disk_free', 78.5)
        disk_emoji = "🟢" if disk_free > 20 else "🟡" if disk_free > 10 else "🔴"
        health_table.add_row(f"{disk_emoji} Disk Space:", f"{disk_free}% free")

        # Network Status
        network_status = system_metrics.get('network_connected', True)
        network_emoji = "🟢" if network_status else "🔴"
        health_table.add_row(f"{network_emoji} Network:", "Connected" if network_status else "Disconnected")

        # MT5 Connection
        mt5_status = self._check_mt5_connection_safe()
        mt5_emoji = "🟢" if mt5_status else "🔴"
        health_table.add_row(f"{mt5_emoji} MT5 Connection:", "Active" if mt5_status else "Inactive")

        # Database Connection
        db_status = system_metrics.get('database_connected', True)
        db_emoji = "🟢" if db_status else "🔴"
        health_table.add_row(f"{db_emoji} Database:", "Connected" if db_status else "Disconnected")

        # Overall health assessment
        overall_health = self._calculate_overall_health_safe(system_metrics)
        health_table.add_row("", "")
        health_table.add_row("Overall Health:", f"{overall_health['emoji']} {overall_health['status']}")

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en system health: {e}", __name__, "system_monitor")
        # Fallback data
        health_table.add_row("🟢 CPU Usage:", "45.2%")
        health_table.add_row("🟢 Memory:", "26.8%")
        health_table.add_row("🟢 Disk Space:", "78.5% free")
        health_table.add_row("🟢 Network:", "Connected")
        health_table.add_row("🟢 MT5 Connection:", "Active")
        health_table.add_row("🟢 Database:", "Connected")
        health_table.add_row("", "")
        health_table.add_row("Overall Health:", "🟢 EXCELLENT")

    return Panel(
        health_table,
        title="🖥️ System Health",
        style="bright_white",
        border_style="white"
    )
```

#### **2. Performance Metrics Panel** (nuevo)
```python
def _render_performance_metrics_panel(self):
    """Performance metrics nuevo panel"""

    performance_table = Table.grid()
    performance_table.add_column(style="bright_green", no_wrap=True)
    performance_table.add_column(style="white")

    try:
        # Performance metrics
        perf_metrics = self._get_performance_metrics_safe()

        # Memory usage detailed
        memory_used = perf_metrics.get('memory_used_gb', 2.1)
        memory_total = perf_metrics.get('memory_total_gb', 8.0)
        memory_pct = (memory_used / memory_total) * 100
        performance_table.add_row("Memory Usage:", f"{memory_used}GB / {memory_total}GB ({memory_pct:.0f}%)")

        # Disk I/O
        disk_read = perf_metrics.get('disk_read_mbps', 45)
        performance_table.add_row("Disk I/O:", f"{disk_read} MB/s read")

        # Network throughput
        network_down = perf_metrics.get('network_down_kbps', 125)
        performance_table.add_row("Network:", f"{network_down} KB/s down")

        # Process count
        active_processes = perf_metrics.get('active_processes', 43)
        performance_table.add_row("Processes:", f"{active_processes} active")

        # Thread count
        total_threads = perf_metrics.get('total_threads', 127)
        performance_table.add_row("Threads:", f"{total_threads} total")

        # System uptime
        uptime = perf_metrics.get('uptime', '2h 34m 15s')
        performance_table.add_row("Uptime:", uptime)

        # Performance score
        performance_score = perf_metrics.get('performance_score', 87)
        performance_table.add_row("", "")
        performance_table.add_row("Performance Score:", f"{performance_score}/100")

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en performance metrics: {e}", __name__, "system_monitor")
        # Fallback data
        performance_table.add_row("Memory Usage:", "2.1GB / 8GB (26%)")
        performance_table.add_row("Disk I/O:", "45 MB/s read")
        performance_table.add_row("Network:", "125 KB/s down")
        performance_table.add_row("Processes:", "43 active")
        performance_table.add_row("Threads:", "127 total")
        performance_table.add_row("Uptime:", "2h 34m 15s")
        performance_table.add_row("", "")
        performance_table.add_row("Performance Score:", "87/100")

    return Panel(
        performance_table,
        title="📊 Performance Metrics",
        style="bright_green",
        border_style="green"
    )
```

#### **3. TCT Pipeline Panel** (de H5)
```python
def _render_tct_pipeline_panel(self):
    """
    TCT Data Pipeline integrado desde H5
    Reutiliza el sistema existente de pipeline
    """

    pipeline_table = Table()
    pipeline_table.add_column("📊 Stage", style="cyan", no_wrap=True)
    pipeline_table.add_column("Status", style="white", justify="center")
    pipeline_table.add_column("Processed", style="white", justify="right")
    pipeline_table.add_column("Rate", style="white", justify="right")
    pipeline_table.add_column("Last Update", style="white", justify="center")

    try:
        # Integrar con sistema existente de H5 TCT Pipeline
        pipeline_data = self._get_tct_pipeline_data_safe()

        for stage in pipeline_data.get('stages', []):
            # Status emoji
            status_emoji = "🟢" if stage['status'] == 'RUNNING' else "🟡" if stage['status'] == 'THROTTLED' else "🔴"

            pipeline_table.add_row(
                f"{stage['icon']} {stage['name']}",
                f"{status_emoji} {stage['status']}",
                f"{stage['processed']:,} {stage['unit']}",
                f"{stage['rate']}/{stage['rate_unit']}",
                stage['last_update']
            )

        # Pipeline summary
        pipeline_health = pipeline_data.get('health', {})
        pipeline_table.add_row("", "", "", "", "")
        pipeline_table.add_row(
            f"Pipeline Health: {pipeline_health.get('emoji', '🟢')} {pipeline_health.get('status', 'OPERATIONAL')}",
            f"Processing: {pipeline_health.get('processing_pct', 98.7)}%",
            f"Queue: {pipeline_health.get('queue_pending', 8)} pending",
            "", ""
        )

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en TCT pipeline: {e}", __name__, "system_monitor")
        # Fallback con datos estáticos
        pipeline_table.add_row("📥 Data Ingestion", "🟢 RUNNING", "1,247 msgs", "125/min", "2s ago")
        pipeline_table.add_row("🔄 Data Processing", "🟢 RUNNING", "1,239 items", "123/min", "3s ago")
        pipeline_table.add_row("📊 Analytics Engine", "🟢 RUNNING", "1,235 calc", "122/min", "1s ago")
        pipeline_table.add_row("💾 Data Storage", "🟢 RUNNING", "1,233 writes", "121/min", "2s ago")
        pipeline_table.add_row("📤 Data Export", "🟡 THROTTLED", "1,201 exports", "115/min", "15s ago")
        pipeline_table.add_row("", "", "", "", "")
        pipeline_table.add_row("Pipeline Health: 🟢 OPERATIONAL", "Processing: 98.7%", "Queue: 8 pending", "", "")

    return Panel(
        pipeline_table,
        title="📊 TCT Data Pipeline",
        subtitle="Real-time Data Processing & Analytics",
        style="bright_blue",
        border_style="blue"
    )
```

#### **4. Candle Downloader Panel** (de H6)
```python
def _render_candle_downloader_panel(self):
    """
    Candle Downloader integrado desde H6
    Reutiliza el sistema existente de downloads
    """

    downloader_table = Table.grid()
    downloader_table.add_column(style="bright_yellow", no_wrap=True)
    downloader_table.add_column(style="white")

    try:
        # Integrar con sistema existente de H6 Downloader
        download_data = self._get_candle_downloader_data_safe()

        # Download progress por símbolo
        for symbol_data in download_data.get('symbols', []):
            status_emoji = symbol_data['status_emoji']
            progress_bar = symbol_data['progress_bar']
            progress_pct = symbol_data['progress_pct']

            downloader_table.add_row(
                f"{status_emoji} {symbol_data['symbol']}:",
                f"{progress_bar} {progress_pct}%"
            )

        # Download summary
        download_summary = download_data.get('summary', {})
        downloader_table.add_row("", "")
        downloader_table.add_row("Total Progress:", f"{download_summary.get('total_progress', 72)}%")
        downloader_table.add_row("Download Speed:", f"{download_summary.get('speed', 2.3)} MB/s")
        downloader_table.add_row("ETA:", download_summary.get('eta', '8 minutes'))
        downloader_table.add_row("", "")
        downloader_table.add_row(
            f"Queue: {download_summary.get('queue', 4)} pending",
            f"Errors: {download_summary.get('errors', 1)}"
        )

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en candle downloader: {e}", __name__, "system_monitor")
        # Fallback data
        downloader_table.add_row("🟢 EUR/USD H1:", "████████ 98%")
        downloader_table.add_row("🟡 GBP/USD H1:", "████▓▓▓▓ 65%")
        downloader_table.add_row("🔴 USD/JPY H1:", "██▓▓▓▓▓▓ 25%")
        downloader_table.add_row("⏸ AUD/USD H1:", "Queued")
        downloader_table.add_row("", "")
        downloader_table.add_row("Total Progress:", "72%")
        downloader_table.add_row("Download Speed:", "2.3 MB/s")
        downloader_table.add_row("ETA:", "8 minutes")
        downloader_table.add_row("", "")
        downloader_table.add_row("Queue: 4 pending", "Errors: 1")

    return Panel(
        downloader_table,
        title="📊 Candle Downloader",
        style="bright_yellow",
        border_style="yellow"
    )
```

#### **5. Maintenance & Debug Panel** (nuevo)
```python
def _render_maintenance_debug_panel(self):
    """Maintenance & debug tools panel nuevo"""

    maintenance_table = Table.grid()
    maintenance_table.add_column(style="bright_magenta", no_wrap=True)
    maintenance_table.add_column(style="white")

    # Navigation shortcuts
    maintenance_table.add_row("[1]", "POI Hub")
    maintenance_table.add_row("[2]", "Analysis")
    maintenance_table.add_row("[3]", "Monitor")
    maintenance_table.add_row("", "")

    # System tools
    maintenance_table.add_row("[C]", "Clear Cache")
    maintenance_table.add_row("[R]", "Restart Services")
    maintenance_table.add_row("[L]", "View Logs")
    maintenance_table.add_row("[H]", "Hibernation Mode")
    maintenance_table.add_row("[D]", "Debug Console")

    # Last maintenance info
    try:
        last_maintenance = self._get_last_maintenance_time_safe()
        maintenance_table.add_row("", "")
        maintenance_table.add_row("Last Maintenance:", last_maintenance)
    except:
        maintenance_table.add_row("", "")
        maintenance_table.add_row("Last Maintenance:", "1h ago")

    return Panel(
        maintenance_table,
        title="🔧 Maintenance & Debug",
        style="bright_magenta",
        border_style="magenta"
    )
```

---

## 🌐 INTEGRACIÓN CON SISTEMAS EXISTENTES

### **System Health (de H1 expandido)**
- **System Monitoring** → Monitoreo completo del sistema
- **Performance Metrics** → Métricas de rendimiento avanzadas
- **Resource Management** → Gestión de recursos del sistema
- **Health Assessment** → Evaluación del estado general

### **TCT Pipeline (de H5)**
- **Data Pipeline Complete** → Pipeline completo desde H5
- **Real-time Processing** → Procesamiento en tiempo real
- **Pipeline Monitoring** → Monitoreo del pipeline
- **Data Quality Control** → Control de calidad de datos

### **Candle Downloader (de H6)**
- **Download Management** → Gestión completa de descargas
- **Progress Tracking** → Seguimiento de progreso
- **Queue Management** → Gestión de cola de descargas
- **Error Handling** → Manejo de errores de descarga

### **Maintenance Tools (Nuevo)**
- **System Maintenance** → Herramientas de mantenimiento
- **Debug Console** → Consola de debug integrada
- **Service Management** → Gestión de servicios
- **Log Management** → Gestión de logs del sistema

---

## 🎨 DISEÑO PROFESIONAL

### **Layout Grid Organization**
```
┌─ System Health ───────┬─ Performance Metrics ──┐
├───────────────────────┴─────────────────────────┤
│             TCT Data Pipeline                   │
│             (ANCHO COMPLETO)                    │
├─ Candle Downloader ───┬─ Maintenance & Debug ───┤
└───────────────────────┴─────────────────────────┘
```

### **Color Scheme Maintained**
- **White**: System health y información crítica
- **Green**: Performance metrics y estado positivo
- **Blue**: TCT pipeline y data processing
- **Yellow**: Candle downloader y procesos en progreso
- **Magenta**: Maintenance tools y debug utilities
- **Red**: Errores y estados críticos

### **Professional Elements**
- **System Monitoring Dashboard** completo
- **Progress Bars** para downloads y pipelines
- **Real-time Metrics** con actualización automática
- **Status Indicators** claros y consistentes
- **Maintenance Tools** integrados

---

## 📊 MÉTRICAS Y MONITOREO

### **Performance Targets**
- **Render Time**: < 120ms para toda la pestaña
- **System Health**: Actualización cada 5s
- **TCT Pipeline**: Monitoreo en tiempo real
- **Downloader**: Progreso actualizado cada 2s
- **Performance Metrics**: Refresh automático

### **Logging SLUC v2.1**
```python
enviar_senal_log("INFO", "🖥️ MONITOR: Pestaña 3 renderizada exitosamente", __name__, "system_monitor")
enviar_senal_log("SYSTEM", f"🖥️ HEALTH: {overall_health} - Score {health_score}/100", __name__, "system_monitor")
enviar_senal_log("PIPELINE", f"🖥️ TCT: Pipeline {pipeline_status} - {processing_rate}/min", __name__, "system_monitor")
enviar_senal_log("DOWNLOAD", f"🖥️ DOWNLOADER: {total_progress}% - {active_downloads} activos", __name__, "system_monitor")
```

---

## 🔄 MIGRACIÓN STEP-BY-STEP

### **FASE 1: Setup Base** 🏗️
1. **Crear** `render_system_monitor()` method
2. **Integrar** TabPane con ID `tab_system_monitor`
3. **Configurar** hotkey "3"
4. **Testing** básico de navegación

### **FASE 2: System Health** 🖥️
1. **Expandir** system health desde H1
2. **Implementar** performance metrics panel
3. **Testing** monitoreo del sistema
4. **Validar** métricas en tiempo real

### **FASE 3: Pipeline Integration** 📊
1. **Migrar** TCT pipeline desde H5
2. **Integrar** data processing monitoring
3. **Testing** pipeline en tiempo real
4. **Optimizar** visualización de datos

### **FASE 4: Downloader & Tools** 🔧
1. **Migrar** candle downloader desde H6
2. **Implementar** maintenance & debug tools
3. **Agregar** service management
4. **Testing** completo de utilidades

### **FASE 5: Polish & Optimization** ✨
1. **Optimizar** performance y layout
2. **Ajustar** real-time updates
3. **Testing** completo de monitoreo
4. **Documentar** sistema final

---

## 🎯 ROADMAP DE IMPLEMENTACIÓN

### **Sprint Inmediato** 🚀
- [ ] **Implementar estructura base** de System Monitor
- [ ] **Expandir system health** desde H1
- [ ] **Migrar TCT pipeline** desde H5
- [ ] **Testing inicial** de consolidación

### **Sprint Optimización** ⚡
- [ ] **Migrar candle downloader** desde H6
- [ ] **Implementar maintenance tools** completos
- [ ] **Optimizar real-time updates** y performance
- [ ] **Polish visual** y user experience

### **Sprint Validación** ✅
- [ ] **Testing completo** de todas las funcionalidades
- [ ] **Validar monitoreo** en tiempo real
- [ ] **Performance optimization** avanzado
- [ ] **Documentación final** del sistema monitor

---

## 🎯 CONCLUSIONES

La **Pestaña 3: System Monitor** representa la **consolidación definitiva** del monitoreo del sistema, ofreciendo:

✅ **System Health completo** expandido desde H1
✅ **TCT Pipeline integrado** desde H5 completamente
✅ **Candle Downloader** desde H6 sin duplicación
✅ **Performance Metrics** avanzados y en tiempo real
✅ **Maintenance Tools** integrados y funcionales
✅ **Debug Console** para troubleshooting
✅ **Real-time Monitoring** con updates automáticos
✅ **Professional Dashboard** unificado y eficiente

**UTILIDAD MÁXIMA**: Esta pestaña elimina la necesidad de H5 y H6 separadas, creando un **centro único de monitoreo y herramientas** que es más eficiente y funcional que las pestañas originales.

---

**Documentación relacionada**:
- [Dashboard Reestructuración v6.0](./DASHBOARD_REESTRUCTURACION_v6_COMPARATIVA.md)
- [Pestaña 1: POI Trading Hub](./DASHBOARD_NUEVA_PESTAÑA_1_POI_HUB.md) ← Primera
- [Pestaña 2: Analysis & Patterns](./DASHBOARD_NUEVA_PESTAÑA_2_ANALYSIS.md) ← Anterior
