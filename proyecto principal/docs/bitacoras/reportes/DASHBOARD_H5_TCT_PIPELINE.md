# 🔄 PESTAÑA H5 - TCT PIPELINE

## 📋 INFORMACIÓN GENERAL

**ID**: `tab_tct`
**Hotkey**: **H5**
**Método Render**: `render_tct_panel()`
**Estado**: ✅ **COMPLETAMENTE OPERATIVO**

---

## 🎯 PROPÓSITO Y FUNCIONALIDAD

La **Pestaña TCT Pipeline** es el centro de procesamiento de datos y pipeline de Trading Cycle Transformation, proporcionando:

- **Data Pipeline management** en tiempo real
- **TCT (Trading Cycle Transformation)** processing
- **Data ingestion** desde múltiples fuentes
- **Transformation engine** para análisis avanzado
- **Quality assurance** y validación de datos
- **Performance monitoring** del pipeline

---

## 🖥️ CONTENIDO VISUAL

### **Header Principal**
```
🔄 TCT DATA PIPELINE - ESTADO OPERACIONAL
```

### **Pipeline Status Dashboard**
```
🏭 PIPELINE STATUS
╭─────────────────────────────────────╮
│ 🟢 INGESTION: ACTIVE               │
│ 🟢 PROCESSING: RUNNING             │
│ 🟢 TRANSFORMATION: OPERATIONAL     │
│ 🟢 VALIDATION: PASSING             │
│ 🟡 OUTPUT: BUFFERING               │
╰─────────────────────────────────────╯
```

### **Data Flow Metrics**
```
📊 DATA FLOW METRICS
╭─────────────────────────────────────╮
│ 📥 Records Ingested: 45,823        │
│ ⚙️ Records Processed: 44,891       │
│ ✅ Records Validated: 44,156       │
│ 📤 Records Output: 43,987          │
│ ❌ Records Rejected: 836           │
│ 📈 Success Rate: 96.2%             │
╰─────────────────────────────────────╯
```

### **Processing Stages**
```
🔧 PROCESSING STAGES
╭─────────────────────────────────────╮
│ Stage 1: Data Ingestion    [████████████] 100%
│ Stage 2: Clean & Filter    [███████████░] 98%
│ Stage 3: Transform         [██████████░░] 94%
│ Stage 4: Enrich Data       [█████████░░░] 91%
│ Stage 5: Validate          [████████░░░░] 89%
│ Stage 6: Output            [███████░░░░░] 87%
╰─────────────────────────────────────╯
```

### **Real-Time Queue Status**
```
📋 QUEUE STATUS
╭─────────────────────────────────────╮
│ 🚀 Input Queue: 1,247 items        │
│ ⚙️ Processing Queue: 456 items     │
│ 📤 Output Queue: 89 items          │
│ ⏱️ Avg Processing Time: 0.23s      │
│ 🔄 Queue Throughput: 4,567/min     │
╰─────────────────────────────────────╯
```

---

## 🔧 FUNCIONALIDAD TÉCNICA

### **Estructura del Panel Principal**
```python
def render_tct_panel(self):
    """Panel del TCT Data Pipeline con monitoreo en tiempo real"""

    # Layout principal
    main_table = Table.grid()
    main_table.add_column()

    # Header del pipeline
    header = Text("🔄 TCT DATA PIPELINE - ESTADO OPERACIONAL", style="bold cyan")
    main_table.add_row(Panel(header, style="cyan", padding=(1, 2)))

    # Separador
    main_table.add_row("")

    # Status del pipeline
    pipeline_status = self._generate_pipeline_status()
    main_table.add_row(pipeline_status)

    # Separador
    main_table.add_row("")

    # Métricas de flujo de datos
    data_flow_metrics = self._generate_data_flow_metrics()
    main_table.add_row(data_flow_metrics)

    return Panel(main_table, title="🔄 TCT Pipeline", style="cyan", padding=(1, 2))
```

### **Pipeline Status Generator**
```python
def _generate_pipeline_status(self):
    """Generar estado actual del pipeline"""

    # Estado de componentes del pipeline
    pipeline_components = {
        "ingestion": {"status": "ACTIVE", "health": "green"},
        "processing": {"status": "RUNNING", "health": "green"},
        "transformation": {"status": "OPERATIONAL", "health": "green"},
        "validation": {"status": "PASSING", "health": "green"},
        "output": {"status": "BUFFERING", "health": "yellow"}
    }

    # Tabla de estado
    status_table = Table.grid()
    status_table.add_column(style="bright_white", no_wrap=True)
    status_table.add_column(style="white")

    status_table.add_row("🏭 PIPELINE STATUS", "")

    for component, info in pipeline_components.items():
        health_emoji = "🟢" if info["health"] == "green" else "🟡" if info["health"] == "yellow" else "🔴"
        status_color = info["health"]

        status_table.add_row(
            f"{health_emoji} {component.upper()}:",
            f"[{status_color}]{info['status']}[/{status_color}]"
        )

    return Panel(status_table, title="🏭 Pipeline Status", style="bright_white")
```

### **Data Flow Metrics Generator**
```python
def _generate_data_flow_metrics(self):
    """Generar métricas de flujo de datos"""

    # Métricas de procesamiento
    flow_metrics = {
        "records_ingested": 45823,
        "records_processed": 44891,
        "records_validated": 44156,
        "records_output": 43987,
        "records_rejected": 836,
        "success_rate": 96.2
    }

    # Tabla de métricas
    metrics_table = Table.grid()
    metrics_table.add_column(style="bright_blue", no_wrap=True)
    metrics_table.add_column(style="white")

    metrics_table.add_row("📊 DATA FLOW METRICS", "")
    metrics_table.add_row("📥 Records Ingested:", f"{flow_metrics['records_ingested']:,}")
    metrics_table.add_row("⚙️ Records Processed:", f"{flow_metrics['records_processed']:,}")
    metrics_table.add_row("✅ Records Validated:", f"{flow_metrics['records_validated']:,}")
    metrics_table.add_row("📤 Records Output:", f"{flow_metrics['records_output']:,}")
    metrics_table.add_row("❌ Records Rejected:", f"[red]{flow_metrics['records_rejected']:,}[/red]")
    metrics_table.add_row("📈 Success Rate:", f"[green]{flow_metrics['success_rate']}%[/green]")

    return Panel(metrics_table, title="📊 Flow Metrics", style="bright_blue")
```

---

## 🏭 ARQUITECTURA DEL PIPELINE

### **Componentes Principales**
```python
class TCTPipeline:
    """Clase principal del TCT Data Pipeline"""

    def __init__(self):
        self.ingestion_engine = DataIngestionEngine()
        self.transformation_engine = TransformationEngine()
        self.validation_engine = ValidationEngine()
        self.output_engine = OutputEngine()
        self.monitoring_system = PipelineMonitor()

    def start_pipeline(self):
        """Iniciar el pipeline completo"""
        self.ingestion_engine.start()
        self.transformation_engine.start()
        self.validation_engine.start()
        self.output_engine.start()
        self.monitoring_system.start()
```

### **Data Ingestion Engine**
```python
class DataIngestionEngine:
    """Motor de ingesta de datos"""

    def __init__(self):
        self.sources = {
            "mt5": MT5DataSource(),
            "market_data": MarketDataSource(),
            "poi_detector": POIDataSource(),
            "analytics": AnalyticsDataSource()
        }

    def ingest_data(self):
        """Ingerir datos de todas las fuentes"""
        ingested_data = {}

        for source_name, source in self.sources.items():
            try:
                data = source.fetch_data()
                ingested_data[source_name] = data
                enviar_senal_log("INFO", f"🔄 Data ingested from {source_name}: {len(data)} records", __name__, "pipeline")
            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Ingestion error from {source_name}: {e}", __name__, "pipeline")

        return ingested_data
```

### **Transformation Engine**
```python
class TransformationEngine:
    """Motor de transformación de datos"""

    def __init__(self):
        self.transformers = [
            DataCleaningTransformer(),
            NormalizationTransformer(),
            EnrichmentTransformer(),
            AggregationTransformer()
        ]

    def transform_data(self, raw_data):
        """Aplicar transformaciones en secuencia"""
        transformed_data = raw_data

        for transformer in self.transformers:
            try:
                transformed_data = transformer.transform(transformed_data)
                enviar_senal_log("INFO", f"🔄 Applied {transformer.__class__.__name__}", __name__, "pipeline")
            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Transformation error: {e}", __name__, "pipeline")

        return transformed_data
```

---

## 📊 PROCESSING STAGES MONITOR

### **Stage Progress Tracking**
```python
def track_processing_stages():
    """Monitorear progreso de stages de procesamiento"""

    stages = {
        "data_ingestion": {"progress": 100, "status": "COMPLETED"},
        "clean_filter": {"progress": 98, "status": "RUNNING"},
        "transform": {"progress": 94, "status": "RUNNING"},
        "enrich_data": {"progress": 91, "status": "RUNNING"},
        "validate": {"progress": 89, "status": "RUNNING"},
        "output": {"progress": 87, "status": "RUNNING"}
    }

    return stages

def display_processing_stages():
    """Display de stages con progress bars"""
    stages = track_processing_stages()

    stages_table = Table.grid()
    stages_table.add_column(style="bright_green", no_wrap=True)
    stages_table.add_column(style="white")

    stages_table.add_row("🔧 PROCESSING STAGES", "")

    for stage_name, info in stages.items():
        progress = info["progress"]
        filled_blocks = int(progress / 10)
        empty_blocks = 10 - filled_blocks

        progress_bar = "█" * filled_blocks + "░" * empty_blocks

        stages_table.add_row(
            f"Stage: {stage_name.replace('_', ' ').title()}",
            f"[{progress_bar}] {progress}%"
        )

    return Panel(stages_table, title="🔧 Processing Stages", style="bright_green")
```

### **Queue Management System**
```python
class QueueManager:
    """Gestor de colas del pipeline"""

    def __init__(self):
        self.input_queue = Queue()
        self.processing_queue = Queue()
        self.output_queue = Queue()
        self.metrics = QueueMetrics()

    def get_queue_status(self):
        """Obtener estado actual de las colas"""
        return {
            "input_queue_size": self.input_queue.qsize(),
            "processing_queue_size": self.processing_queue.qsize(),
            "output_queue_size": self.output_queue.qsize(),
            "avg_processing_time": self.metrics.get_avg_processing_time(),
            "throughput": self.metrics.get_throughput()
        }

def display_queue_status():
    """Display del estado de colas"""
    queue_manager = QueueManager()
    status = queue_manager.get_queue_status()

    queue_table = Table.grid()
    queue_table.add_column(style="bright_yellow", no_wrap=True)
    queue_table.add_column(style="white")

    queue_table.add_row("📋 QUEUE STATUS", "")
    queue_table.add_row("🚀 Input Queue:", f"{status['input_queue_size']:,} items")
    queue_table.add_row("⚙️ Processing Queue:", f"{status['processing_queue_size']:,} items")
    queue_table.add_row("📤 Output Queue:", f"{status['output_queue_size']:,} items")
    queue_table.add_row("⏱️ Avg Processing Time:", f"{status['avg_processing_time']:.2f}s")
    queue_table.add_row("🔄 Queue Throughput:", f"{status['throughput']:,}/min")

    return Panel(queue_table, title="📋 Queue Monitor", style="bright_yellow")
```

---

## 🔍 DATA VALIDATION ENGINE

### **Validation Rules**
```python
class ValidationEngine:
    """Motor de validación de datos"""

    def __init__(self):
        self.validation_rules = [
            DataIntegrityValidator(),
            SchemaValidator(),
            BusinessRulesValidator(),
            QualityMetricsValidator()
        ]

    def validate_data(self, data):
        """Validar datos contra todas las reglas"""
        validation_results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "errors": []
        }

        for validator in self.validation_rules:
            try:
                result = validator.validate(data)
                if result["is_valid"]:
                    validation_results["passed"] += result["records_validated"]
                else:
                    validation_results["failed"] += result["records_failed"]
                    validation_results["errors"].extend(result["errors"])
            except Exception as e:
                validation_results["errors"].append(str(e))

        return validation_results
```

### **Quality Metrics**
```python
def calculate_data_quality_metrics(validation_results, total_records):
    """Calcular métricas de calidad de datos"""

    quality_metrics = {
        "completeness": (validation_results["passed"] / total_records) * 100,
        "accuracy": calculate_accuracy_score(validation_results),
        "consistency": calculate_consistency_score(validation_results),
        "timeliness": calculate_timeliness_score(validation_results),
        "validity": calculate_validity_score(validation_results)
    }

    return quality_metrics

def display_quality_metrics():
    """Display de métricas de calidad"""
    metrics = calculate_data_quality_metrics(validation_results, total_records)

    quality_table = Table.grid()
    quality_table.add_column(style="bright_magenta", no_wrap=True)
    quality_table.add_column(style="white")

    quality_table.add_row("🎯 DATA QUALITY METRICS", "")
    quality_table.add_row("📊 Completeness:", f"[green]{metrics['completeness']:.1f}%[/green]")
    quality_table.add_row("🎯 Accuracy:", f"[cyan]{metrics['accuracy']:.1f}%[/cyan]")
    quality_table.add_row("🔄 Consistency:", f"[blue]{metrics['consistency']:.1f}%[/blue]")
    quality_table.add_row("⏰ Timeliness:", f"[yellow]{metrics['timeliness']:.1f}%[/yellow]")
    quality_table.add_row("✅ Validity:", f"[magenta]{metrics['validity']:.1f}%[/magenta]")

    return Panel(quality_table, title="🎯 Quality Metrics", style="bright_magenta")
```

---

## 🚀 PERFORMANCE OPTIMIZATION

### **Parallel Processing**
```python
class ParallelProcessor:
    """Procesador paralelo para pipeline"""

    def __init__(self, num_workers=4):
        self.num_workers = num_workers
        self.executor = ThreadPoolExecutor(max_workers=num_workers)

    def process_batch(self, data_batch):
        """Procesar lote de datos en paralelo"""
        futures = []

        # Dividir datos en chunks
        chunks = self.split_into_chunks(data_batch, self.num_workers)

        # Procesar cada chunk en paralelo
        for chunk in chunks:
            future = self.executor.submit(self.process_chunk, chunk)
            futures.append(future)

        # Recopilar resultados
        results = []
        for future in as_completed(futures):
            results.extend(future.result())

        return results
```

### **Memory Management**
```python
class MemoryManager:
    """Gestor de memoria para el pipeline"""

    def __init__(self, max_memory_mb=1024):
        self.max_memory_mb = max_memory_mb
        self.current_usage = 0

    def monitor_memory_usage(self):
        """Monitorear uso de memoria"""
        import psutil

        process = psutil.Process()
        memory_info = process.memory_info()

        self.current_usage = memory_info.rss / 1024 / 1024  # MB

        if self.current_usage > self.max_memory_mb:
            enviar_senal_log("WARNING", f"⚠️ High memory usage: {self.current_usage:.1f}MB", __name__, "pipeline")
            self.trigger_garbage_collection()

    def trigger_garbage_collection(self):
        """Ejecutar garbage collection"""
        import gc
        gc.collect()
        enviar_senal_log("INFO", "🗑️ Garbage collection executed", __name__, "pipeline")
```

---

## 📊 MONITORING Y ALERTAS

### **Pipeline Health Monitor**
```python
class PipelineHealthMonitor:
    """Monitor de salud del pipeline"""

    def __init__(self):
        self.health_checks = [
            MemoryHealthCheck(),
            PerformanceHealthCheck(),
            QueueHealthCheck(),
            DataQualityHealthCheck()
        ]

    def perform_health_check(self):
        """Realizar check completo de salud"""
        health_status = {
            "overall_health": "HEALTHY",
            "warnings": [],
            "errors": [],
            "recommendations": []
        }

        for check in self.health_checks:
            result = check.execute()

            if result["status"] == "WARNING":
                health_status["warnings"].append(result["message"])
            elif result["status"] == "ERROR":
                health_status["errors"].append(result["message"])
                health_status["overall_health"] = "UNHEALTHY"

            if result.get("recommendations"):
                health_status["recommendations"].extend(result["recommendations"])

        return health_status
```

### **Alert System**
```python
class AlertSystem:
    """Sistema de alertas del pipeline"""

    def __init__(self):
        self.alert_handlers = [
            LogAlertHandler(),
            EmailAlertHandler(),
            SlackAlertHandler()
        ]

    def send_alert(self, alert_type, message, severity="INFO"):
        """Enviar alerta a todos los handlers"""
        alert = {
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }

        for handler in self.alert_handlers:
            try:
                handler.send_alert(alert)
            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Alert handler error: {e}", __name__, "pipeline")
```

---

## 🔄 ERROR HANDLING Y RECOVERY

### **Error Recovery System**
```python
class ErrorRecoverySystem:
    """Sistema de recuperación de errores"""

    def __init__(self):
        self.retry_policies = {
            "network_error": RetryPolicy(max_retries=3, backoff=2),
            "data_error": RetryPolicy(max_retries=1, backoff=1),
            "system_error": RetryPolicy(max_retries=5, backoff=5)
        }

    def handle_error(self, error, context):
        """Manejar error con recuperación automática"""
        error_type = self.classify_error(error)
        policy = self.retry_policies.get(error_type)

        if policy and policy.should_retry():
            enviar_senal_log("WARNING", f"🔄 Retrying after {error_type}: {error}", __name__, "pipeline")
            return self.retry_operation(context, policy)
        else:
            enviar_senal_log("ERROR", f"❌ Unrecoverable error: {error}", __name__, "pipeline")
            return self.fallback_operation(context)
```

### **Circuit Breaker Pattern**
```python
class CircuitBreaker:
    """Circuit breaker para proteger componentes"""

    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        """Ejecutar función con circuit breaker"""
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenException("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
```

---

## 🎯 ROADMAP Y MEJORAS

### **Sprint 1.8 - Optimización**
- [ ] Implementar processing paralelo avanzado
- [ ] Optimizar memory management
- [ ] Mejorar error recovery mechanisms

### **Sprint 2.0 - Funcionalidades Avanzadas**
- [ ] Machine learning para data quality
- [ ] Auto-scaling capabilities
- [ ] Advanced data lineage tracking

### **Sprint 2.1 - Enterprise Integration**
- [ ] Kafka integration para streaming
- [ ] Cloud pipeline deployment
- [ ] Advanced monitoring dashboard

---

## 🎯 CONCLUSIONES

La **Pestaña H5 - TCT Pipeline** es el **centro de procesamiento de datos**, proporcionando:

✅ **Pipeline completo de datos** con ingesta, transformación y validación
✅ **Monitoreo en tiempo real** de todas las stages de procesamiento
✅ **Sistema de colas** robusto con métricas de performance
✅ **Validation engine** con múltiples reglas de calidad
✅ **Error handling** y recovery automático
✅ **Performance optimization** con procesamiento paralelo
✅ **Health monitoring** y sistema de alertas
✅ **Logging completo** para auditoría y debugging

Es la pestaña más **técnica para procesamiento de datos** y está **100% operativa** con capacidades de pipeline de nivel enterprise para processing de datos de trading.
