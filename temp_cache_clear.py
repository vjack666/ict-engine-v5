# Temporary file to trigger Pylance refresh
from core.ict_engine.fractal_analyzer import FractalAnalyzer
analyzer = FractalAnalyzer()
levels = analyzer.get_fractal_levels()
print("Cache refresh triggered")
