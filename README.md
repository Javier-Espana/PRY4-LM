# Sistema de Control Difuso para Riego de Invernadero 🌱💧

**Proyecto:** PRY4-LM - Aplicación de Lógica Difusa con scikit-fuzzy  
**Fecha:** Noviembre 2025  
**Equipo:** [Nombres de los integrantes del equipo]

---

## 📋 Descripción del Proyecto

Este proyecto implementa un **sistema de inferencia difusa (Fuzzy Inference System)** tipo **Mamdani** para determinar la **duración óptima del riego** en un invernadero automatizado. El sistema considera tres variables ambientales críticas para calcular cuánto tiempo debe funcionar el sistema de riego.

### Variables del Sistema

#### 🔵 Variables de Entrada (Antecedentes)

1. **Humedad del Suelo** (0-100%)
   - Muy seca: 0-20%
   - Seca: 10-50%
   - Normal: 40-80%
   - Húmeda: 70-100%

2. **Temperatura Ambiente** (0-40°C)
   - Frío: 0-15°C
   - Templado: 10-30°C
   - Caliente: 25-40°C

3. **Radiación Solar** (0-1000 W/m²)
   - Baja: 0-350 W/m²
   - Media: 250-750 W/m²
   - Alta: 650-1000 W/m²

#### 🟢 Variable de Salida (Consecuente)

**Duración del Riego** (0-30 minutos)
- Muy corta: 0-6 min
- Corta: 4-12 min
- Media: 10-24 min
- Larga: 20-30 min

---

## 🏗️ Estructura del Proyecto

```
PRY4-LM/
│
├── main.py                          # Script principal con menú interactivo
│
├── src/
│   ├── __init__.py
│   │
│   ├── system/                      # Módulo del sistema difuso
│   │   ├── __init__.py
│   │   ├── variables.py             # Definición de universos de discurso
│   │   ├── membership_functions.py  # Funciones de pertenencia
│   │   ├── rules.py                 # 12 reglas difusas del sistema
│   │   └── controller.py            # Motor de inferencia Mamdani
│   │
│   └── utils/                       # Módulo de utilidades
│       ├── __init__.py
│       ├── inputs.py                # Manejo de datos de entrada
│       ├── visualization.py         # Gráficas y visualizaciones
│       └── data_logger.py           # Registro de resultados (CSV/JSON)
│
├── logs/                            # Directorio de logs y resultados
│   ├── session_*.csv                # Logs en formato CSV
│   ├── session_*.json               # Resúmenes en formato JSON
│   └── *.png                        # Gráficas generadas
│
├── requirements.txt                 # Dependencias del proyecto
└── README.md                        # Este archivo
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o descargar el repositorio

```bash
cd ~/Escritorio
git clone https://github.com/Javier-Espana/PRY4-LM.git
cd PRY4-LM
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📦 Dependencias

```
numpy>=1.21.0
scikit-fuzzy>=0.4.2
matplotlib>=3.5.0
```

---

## 🎯 Uso del Sistema

### Ejecución del Programa Principal

```bash
python main.py
```

### Menú Interactivo

El programa presenta un menú con las siguientes opciones:

1. **Ejecutar casos de prueba predefinidos** - 8 casos representativos
2. **Ejecutar casos extremos** - Límites del sistema
3. **Ingresar valores personalizados** - Entrada manual
4. **Visualizar funciones de pertenencia** - Gráficas de membresías
5. **Visualizar superficie de control 3D** - Análisis de respuesta
6. **Visualizar resultado de simulación específica** - Detalle de inferencia
7. **Ver información del sistema** - Reglas y variables
8. **Ver resumen de sesión actual** - Estadísticas
0. **Salir** - Guarda resumen y cierra

### Ejemplo de Uso en Código

```python
from src.system.variables import define_universes
from src.system.membership_functions import define_memberships
from src.system.rules import define_rules
from src.system.controller import build_system, simulate_irrigation

# Inicializar sistema
universes = define_universes()
vars = define_memberships(universes)
rules = define_rules(vars)
system = build_system(rules)

# Simular con valores específicos
humedad = 35      # 35% humedad
temperatura = 28  # 28°C
radiacion = 750   # 750 W/m²

duracion = simulate_irrigation(system, humedad, temperatura, radiacion)
print(f"Duración del riego: {duracion:.2f} minutos")
```

---

## 🧠 Reglas del Sistema

El sistema implementa 12 reglas difusas basadas en conocimiento experto:

| # | Regla | Salida |
|---|-------|--------|
| 1 | SI humedad muy seca Y temperatura caliente Y radiación alta | Larga |
| 2 | SI humedad muy seca Y temperatura caliente Y radiación media | Larga |
| 3 | SI humedad muy seca Y temperatura templado | Larga |
| 4 | SI humedad seca Y temperatura caliente | Media |
| 5 | SI humedad seca Y radiación alta | Media |
| 6 | SI humedad normal Y temperatura caliente Y radiación alta | Media |
| 7 | SI humedad normal Y radiación baja | Corta |
| 8 | SI humedad húmeda | Muy corta |
| 9 | SI humedad seca Y temperatura frío | Corta |
| 10 | SI humedad muy seca Y temperatura frío | Media |
| 11 | SI radiación alta Y temperatura caliente | Media |
| 12 | SI humedad normal Y temperatura templado Y radiación media | Corta |

---

## 📊 Resultados y Logs

### Formato CSV

Los resultados se guardan en `logs/session_*.csv`:

```csv
timestamp,caso,humedad_suelo_%,temperatura_C,radiacion_W_m2,duracion_riego_min,notas
2025-11-02 10:30:15,Condiciones extremas,15,35,900,24.56,
2025-11-02 10:30:16,Condiciones normales,60,22,500,8.34,
```

### Formato JSON

Resumen completo en `logs/session_*.json`:

```json
{
  "session_id": "riego_invernadero_20251102_103015",
  "num_simulaciones": 8,
  "estadisticas": {
    "duracion_min": 3.21,
    "duracion_max": 24.56,
    "duracion_promedio": 12.45
  },
  "resultados": [...]
}
```

---

## 📈 Visualizaciones

### 1. Funciones de Pertenencia

Muestra las funciones triangulares y trapezoidales de cada variable.

### 2. Superficie de Control 3D

Gráfica interactiva que muestra cómo dos variables de entrada afectan la salida.

### 3. Resultado de Simulación

Visualiza los grados de activación de cada función de pertenencia para un caso específico.

### 4. Comparación de Simulaciones

Gráfico de barras y heatmap comparando múltiples casos.

---

## 🔬 Metodología

### Tipo de Sistema

**Sistema Mamdani** con:
- Fuzzificación: Funciones triangulares y trapezoidales
- Motor de inferencia: AND (mínimo), OR (máximo)
- Defuzzificación: Método del centroide

### Proceso de Inferencia

1. **Fuzzificación**: Conversión de valores crisp a grados de pertenencia
2. **Evaluación de reglas**: Activación de reglas mediante operadores difusos
3. **Agregación**: Unión de salidas de todas las reglas
4. **Defuzzificación**: Conversión a valor crisp (duración en minutos)

---

## 🎓 Aplicación Práctica

Este sistema puede aplicarse en:

- Invernaderos automatizados
- Agricultura de precisión
- Sistemas de riego inteligente
- Ahorro de agua en cultivos
- Optimización de recursos hídricos

### Ventajas del Enfoque Difuso

✅ Maneja incertidumbre en mediciones  
✅ Simula razonamiento humano experto  
✅ No requiere modelo matemático preciso  
✅ Robustez ante ruido en sensores  
✅ Fácil ajuste mediante reglas lingüísticas  

---

## 📝 Conclusiones

### Conclusiones Técnicas

1. El sistema difuso proporciona respuestas suaves y graduales, evitando cambios abruptos en la duración del riego.
2. La combinación de tres variables permite modelar mejor las condiciones reales del invernadero.
3. Las 12 reglas cubren adecuadamente los casos típicos y extremos.
4. La visualización 3D facilita la comprensión del comportamiento del sistema.

### Recomendaciones

- Calibrar las funciones de pertenencia con datos reales del invernadero.
- Considerar variables adicionales: humedad ambiente, velocidad del viento.
- Implementar retroalimentación adaptativa basada en históricos.
- Integrar con sensores IoT para automatización completa.

---

## 👥 Reflexiones del Equipo

### Reflexión Grupal

*[Aquí cada grupo debe agregar su reflexión conjunta sobre el aprendizaje de lógica difusa, los desafíos enfrentados y los logros obtenidos]*

### Reflexiones Individuales

**Integrante 1:** [Nombre]  
*[Reflexión personal sobre el proyecto]*

**Integrante 2:** [Nombre]  
*[Reflexión personal sobre el proyecto]*

**Integrante 3:** [Nombre]  
*[Reflexión personal sobre el proyecto]*

---

## 📚 Referencias

1. Zadeh, L. A. (1965). Fuzzy sets. Information and Control, 8(3), 338-353.
2. Mamdani, E. H., & Assilian, S. (1975). An experiment in linguistic synthesis with a fuzzy logic controller.
3. Scikit-fuzzy Documentation: https://pythonhosted.org/scikit-fuzzy/
4. Ross, T. J. (2010). Fuzzy Logic with Engineering Applications (3rd ed.). Wiley.

---

## 📄 Licencia

Este proyecto es con fines educativos para la asignatura PRY4-LM.

---

## 📧 Contacto

Para consultas sobre el proyecto:
- Repositorio: https://github.com/Javier-Espana/PRY4-LM
- Issues: https://github.com/Javier-Espana/PRY4-LM/issues

---

**Fecha de última actualización:** 2 de noviembre de 2025
