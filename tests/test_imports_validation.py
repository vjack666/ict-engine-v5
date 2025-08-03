from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
TEST DE VALIDACIÓN DE IMPORTS - Advanced Candle Downloader
Verifica que todos los imports estén correctamente justificados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports_validation():
    """Valida que todos los imports del downloader funcionen correctamente"""

    enviar_senal_log("INFO", "🔍 === VALIDACIÓN DE IMPORTS ADVANCED CANDLE DOWNLOADER ===", "test_imports_validation", "migration")

    try:
        # Test pandas import y uso
        import pandas as pd
        df_test = pd.DataFrame({'test': [1, 2, 3]})
        enviar_senal_log("INFO", f"✅ pandas: OK - DataFrame creado con {len(df_test, "test_imports_validation", "migration")} filas")

        # Test numpy import y uso
        import numpy as np
        array_test = np.array([1, 2, 3])
        enviar_senal_log("INFO", f"✅ numpy: OK - Array creado con {len(array_test, "test_imports_validation", "migration")} elementos")

        # Test datetime y timedelta
        from datetime import datetime, timedelta
        now = datetime.now()
        delta = timedelta(hours=1)
        future = now + delta
        enviar_senal_log("INFO", f"✅ datetime/timedelta: OK - Delta calculado: {delta}", "test_imports_validation", "migration")

        # Test typing imports
        from typing import Optional, Dict, List, Tuple, Union
        test_dict: Dict[str, int] = {"test": 1}
        test_list: List[str] = ["test"]
        test_tuple: Tuple[str, int] = ("test", 1)
        test_optional: Optional[str] = None
        test_union: Union[str, int] = "test"
        enviar_senal_log("INFO", "✅ typing: OK - Todos los tipos importados correctamente", "test_imports_validation", "migration")

        # Test threading
        import threading
        thread_count = threading.active_count()
        enviar_senal_log("INFO", f"✅ threading: OK - Hilos activos: {thread_count}", "test_imports_validation", "migration")

        # Test concurrent.futures
        from concurrent.futures import ThreadPoolExecutor, as_completed
        enviar_senal_log("INFO", "✅ concurrent.futures: OK - ThreadPoolExecutor importado", "test_imports_validation", "migration")

        # Test completo del downloader
        from utils.advanced_candle_downloader import AdvancedCandleDownloader
        downloader = AdvancedCandleDownloader()
        enviar_senal_log("INFO", "✅ AdvancedCandleDownloader: OK - Instancia creada", "test_imports_validation", "migration")

        enviar_senal_log("INFO", "\n🎉 === TODOS LOS IMPORTS VALIDADOS EXITOSAMENTE ===", "test_imports_validation", "migration")
        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en validación: {e}", "test_imports_validation", "migration")
        return False

if __name__ == "__main__":
    success = test_imports_validation()
    sys.exit(0 if success else 1)
