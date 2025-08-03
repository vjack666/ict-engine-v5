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

    print("🔍 === VALIDACIÓN DE IMPORTS ADVANCED CANDLE DOWNLOADER ===")

    try:
        # Test pandas import y uso
        import pandas as pd
        df_test = pd.DataFrame({'test': [1, 2, 3]})
        print(f"✅ pandas: OK - DataFrame creado con {len(df_test)} filas")

        # Test numpy import y uso
        import numpy as np
        array_test = np.array([1, 2, 3])
        print(f"✅ numpy: OK - Array creado con {len(array_test)} elementos")

        # Test datetime y timedelta
        from datetime import datetime, timedelta
        now = datetime.now()
        delta = timedelta(hours=1)
        future = now + delta
        print(f"✅ datetime/timedelta: OK - Delta calculado: {delta}")

        # Test typing imports
        from typing import Optional, Dict, List, Tuple, Union
        test_dict: Dict[str, int] = {"test": 1}
        test_list: List[str] = ["test"]
        test_tuple: Tuple[str, int] = ("test", 1)
        test_optional: Optional[str] = None
        test_union: Union[str, int] = "test"
        print("✅ typing: OK - Todos los tipos importados correctamente")

        # Test threading
        import threading
        thread_count = threading.active_count()
        print(f"✅ threading: OK - Hilos activos: {thread_count}")

        # Test concurrent.futures
        from concurrent.futures import ThreadPoolExecutor, as_completed
        print("✅ concurrent.futures: OK - ThreadPoolExecutor importado")

        # Test completo del downloader
        from utils.advanced_candle_downloader import AdvancedCandleDownloader
        downloader = AdvancedCandleDownloader()
        print("✅ AdvancedCandleDownloader: OK - Instancia creada")

        print("\n🎉 === TODOS LOS IMPORTS VALIDADOS EXITOSAMENTE ===")
        return True

    except Exception as e:
        print(f"❌ Error en validación: {e}")
        return False

if __name__ == "__main__":
    success = test_imports_validation()
    sys.exit(0 if success else 1)
