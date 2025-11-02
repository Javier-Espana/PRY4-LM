# Sistema de Control Difuso para Riego de Invernadero

**Proyecto:** PRY4-LM - Aplicación de Lógica Difusa con scikit-fuzzy  
**Fecha:** Noviembre 2025  
**Equipo:** [Nombres de los integrantes del equipo]

---

## Descripción del Proyecto

Este proyecto implementa un sistema de inferencia difusa (Fuzzy Inference System) tipo Mamdani para determinar la duración óptima del riego en un invernadero automatizado. El sistema utiliza lógica difusa para procesar tres variables ambientales críticas y calcular el tiempo necesario de riego, permitiendo una gestión eficiente del recurso hídrico en agricultura de precisión.

La lógica difusa permite manejar la incertidumbre inherente a las mediciones ambientales y simula el razonamiento de un experto agrónomo, proporcionando decisiones suaves y graduales que evitan cambios bruscos en el sistema de riego.

## Variables del Sistema

El sistema procesa tres variables de entrada (antecedentes) y produce una variable de salida (consecuente):

### Variables de Entrada (Antecedentes)

**1. Humedad del Suelo (0-100%)**
- Muy seca: 0-20%
- Seca: 10-50%
- Normal: 40-80%
- Húmeda: 70-100%

**2. Temperatura Ambiente (0-40°C)**
- Frío: 0-15°C
- Templado: 10-30°C
- Caliente: 25-40°C

**3. Radiación Solar (0-1000 W/m²)**
- Baja: 0-350 W/m²
- Media: 250-750 W/m²
- Alta: 650-1000 W/m²

### Variable de Salida (Consecuente)

**Duración del Riego (0-30 minutos)**
- Muy corta: 0-6 min
- Corta: 4-12 min
- Media: 10-24 min
- Larga: 20-30 min

---

## Características del Sistema

- Implementación de sistema de inferencia Mamdani con 12 reglas lingüísticas
- Funciones de pertenencia triangulares y trapezoidales para modelado preciso
- Menú interactivo con 8 opciones de operación
- Visualización gráfica de funciones de pertenencia en 4 gráficas integradas
- Generación de superficies de control 3D para análisis de comportamiento
- Sistema de registro automático de simulaciones en formato CSV y JSON
- Casos de prueba predefinidos y capacidad de entrada personalizada
- Defuzzificación mediante método del centroide
- Arquitectura modular y extensible

---

## Requisitos del Sistema

### Software Requerido

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Dependencias

```bash
pip install numpy>=1.21.0
pip install scikit-fuzzy>=0.4.2
pip install scipy>=1.7.0
pip install matplotlib>=3.5.0
pip install networkx>=2.6.0
```

O instalar todas las dependencias desde el archivo de requisitos:

```bash
pip install -r requirements.txt
```

---

## Estructura del Proyecto

```
PRY4-LM/
│
├── main.py                          # Script principal con menú interactivo
├── test_quick.py                    # Script de prueba rápida del sistema
├── requirements.txt                 # Dependencias del proyecto
├── README.md                        # Documentación del proyecto
├── GUIA_USO.md                      # Guía de uso rápido
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
└── logs/                            # Directorio de logs y resultados
    ├── session_*.csv                # Logs en formato CSV
    ├── session_*.json               # Resúmenes en formato JSON
    └── *.png                        # Gráficas generadas
```

---

## Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### Paso 1: Obtener el Código

```bash
# Clonar el repositorio
cd ~/Escritorio
git clone https://github.com/Javier-Espana/PRY4-LM.git
cd PRY4-LM
```

### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Verificar Instalación

```bash
python test_quick.py
```

Si la instalación es correcta, deberá ver la salida de 3 casos de prueba exitosos.

---

## Uso del Sistema

### Ejecución del Programa Principal

Para ejecutar el sistema completo con interfaz de menú interactivo:

```bash
python main.py
```

### Prueba Rápida

Para ejecutar una prueba rápida del sistema con 3 casos predefinidos:

```bash
python test_quick.py
```

### Opciones del Menú Interactivo

El programa principal presenta las siguientes opciones:

**Opción 1: Ejecutar casos de prueba predefinidos**  
Ejecuta 8 casos representativos que cubren diferentes escenarios de operación del invernadero.

**Opción 2: Ejecutar casos extremos**  
Prueba el sistema con valores en los límites de los rangos de operación.

**Opción 3: Ingresar valores personalizados**  
Permite al usuario introducir valores específicos de humedad, temperatura y radiación solar.

**Opción 4: Visualizar funciones de pertenencia**  
Genera y muestra gráficas de las funciones de pertenencia para todas las variables del sistema.

**Opción 5: Visualizar superficie de control 3D**  
Crea una superficie tridimensional que muestra la relación entre dos variables de entrada y la salida.

**Opción 6: Visualizar resultado de simulación específica**  
Muestra el detalle de una simulación incluyendo los grados de activación de cada función de pertenencia.

**Opción 7: Ver información del sistema**  
Presenta información técnica sobre el sistema, incluyendo número de reglas y variables.

**Opción 8: Ver resumen de sesión actual**  
Muestra estadísticas de todas las simulaciones ejecutadas en la sesión actual.

**Opción 0: Salir**  
Guarda el resumen de la sesión y cierra el programa.

---

## Ejemplo de Uso Programático

El sistema puede ser utilizado directamente desde código Python:

```python
import sys
sys.path.insert(0, 'src')

from system.variables import define_universes
from system.membership_functions import define_memberships
from system.rules import define_rules
from system.controller import build_system, simulate_irrigation

# Inicializar el sistema de control difuso
universes = define_universes()
vars = define_memberships(universes)
rules = define_rules(vars)
system = build_system(rules)

# Simular con valores específicos
humedad = 35          # 35% de humedad del suelo
temperatura = 28      # 28°C de temperatura ambiente
radiacion = 750       # 750 W/m² de radiación solar

# Ejecutar inferencia
duracion = simulate_irrigation(system, humedad, temperatura, radiacion)
print(f"Duración del riego: {duracion:.2f} minutos")
```

---

## Reglas del Sistema de Inferencia

El sistema implementa 12 reglas difusas basadas en conocimiento experto de gestión de riego en invernaderos. Estas reglas relacionan las condiciones ambientales con la duración óptima del riego:

| Número | Condiciones de Entrada | Salida |
|--------|------------------------|--------|
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

Las reglas están diseñadas para maximizar la eficiencia del riego considerando:
- La evapotranspiración aumenta con temperatura y radiación solar
- El suelo húmedo requiere menos riego independientemente de otras condiciones
- Las condiciones extremas (muy seco + caliente + alta radiación) requieren riego prolongado
- Las temperaturas bajas reducen la necesidad de riego incluso con humedad baja

---

## Formato de Resultados y Registro de Datos

### Archivo CSV

El sistema genera automáticamente archivos CSV con los resultados de cada simulación en el directorio `logs/`. El formato es:

```csv
timestamp,caso,humedad_suelo_%,temperatura_C,radiacion_W_m2,duracion_riego_min,notas
2025-11-02 10:30:15,Condiciones extremas,15,35,900,20.21,
2025-11-02 10:30:16,Condiciones normales,60,22,500,8.00,
2025-11-02 10:30:17,Suelo húmedo,85,18,300,2.33,
```

### Archivo JSON

Además del CSV, se genera un archivo JSON con un resumen completo de la sesión:

```json
{
  "session_id": "riego_invernadero_20251102_103015",
  "timestamp_inicio": "2025-11-02 10:30:15",
  "timestamp_fin": "2025-11-02 10:35:22",
  "num_simulaciones": 8,
  "estadisticas": {
    "duracion_min": 2.33,
    "duracion_max": 20.21,
    "duracion_promedio": 11.45
  },
  "informacion_adicional": {
    "descripcion": "Sistema de Control Difuso para Riego de Invernadero",
    "tipo_sistema": "Mamdani",
    "num_reglas": 12
  },
  "resultados": [...]
}
```

---

## Visualizaciones Disponibles

El sistema proporciona cuatro tipos de visualizaciones para analizar el comportamiento del sistema difuso:

### 1. Funciones de Pertenencia

Genera una figura con 4 subgráficas que muestra todas las funciones de pertenencia del sistema:
- Humedad del Suelo: muy_seca, seca, normal, húmeda
- Temperatura Ambiente: frío, templado, caliente
- Radiación Solar: baja, media, alta
- Duración del Riego: muy_corta, corta, media, larga

Cada gráfica incluye el universo de discurso completo y los grados de pertenencia de 0 a 1.

### 2. Superficie de Control 3D

Genera una superficie tridimensional que muestra cómo dos variables de entrada afectan la variable de salida, manteniendo la tercera variable fija. Permite visualizar:
- Humedad vs Temperatura (con Radiación fija)
- Humedad vs Radiación (con Temperatura fija)
- Temperatura vs Radiación (con Humedad fija)

La superficie utiliza un mapa de colores para indicar la duración del riego resultante.

### 3. Resultado de Simulación Individual

Visualiza el detalle completo de una simulación específica, mostrando:
- Grados de activación de cada función de pertenencia para las entradas
- Valor de entrada marcado en cada gráfica
- Valor de salida resultante de la defuzzificación
- Funciones de pertenencia de la variable de salida

### 4. Comparación de Múltiples Simulaciones

Presenta dos visualizaciones complementarias:
- Gráfico de barras con las duraciones de riego para cada caso
- Heatmap con los valores normalizados de las variables de entrada

Permite comparar fácilmente el comportamiento del sistema ante diferentes condiciones.

---

## Metodología y Fundamento Teórico

### Sistema de Inferencia Mamdani

El sistema implementado utiliza el método de inferencia Mamdani, que se caracteriza por:

**Fuzzificación:**  
Conversión de valores numéricos crisp (precisos) en grados de pertenencia a conjuntos difusos mediante funciones de pertenencia triangulares y trapezoidales.

**Base de Reglas:**  
12 reglas lingüísticas del tipo "SI-ENTONCES" que relacionan las variables de entrada con la salida.

**Motor de Inferencia:**  
- Operador AND: Función mínimo (fmin)
- Operador OR: Función máximo (fmax)
- Agregación de reglas: Unión de todas las salidas activadas

**Defuzzificación:**  
Método del centroide (center of gravity) para convertir el conjunto difuso resultante en un valor numérico crisp que representa la duración del riego en minutos.

### Proceso de Inferencia Completo

1. **Entrada de Datos:** El sistema recibe tres valores numéricos (humedad, temperatura, radiación)

2. **Fuzzificación:** Cada valor de entrada se convierte en grados de pertenencia para cada conjunto difuso de su variable

3. **Evaluación de Reglas:** Cada regla se evalúa calculando el mínimo de los grados de pertenencia de sus antecedentes

4. **Agregación:** Las salidas de todas las reglas se combinan mediante la función máximo

5. **Defuzzificación:** El conjunto difuso agregado se convierte en un valor numérico usando el método del centroide

6. **Salida:** El sistema produce la duración óptima del riego en minutos

Este proceso permite al sistema manejar la incertidumbre y proporcionar transiciones suaves entre diferentes estados de operación.

---

## Aplicaciones Prácticas

Este sistema de control difuso puede aplicarse en diversos contextos de agricultura de precisión:

### Invernaderos Automatizados
Integración con sistemas de riego automático para ajustar la duración del riego en tiempo real según las condiciones ambientales medidas por sensores.

### Agricultura de Precisión
Optimización del uso de agua en cultivos mediante decisiones inteligentes basadas en múltiples variables ambientales simultáneas.

### Sistemas de Riego Inteligente
Implementación en sistemas IoT para gestión remota y automatizada de recursos hídricos en instalaciones agrícolas.

### Ahorro de Agua en Cultivos
Reducción del consumo de agua mediante riego ajustado a las necesidades reales de las plantas según las condiciones ambientales.

### Optimización de Recursos Hídricos
Gestión eficiente del recurso hídrico en zonas con escasez de agua o altos costos de bombeo.

### Ventajas del Enfoque de Lógica Difusa

**Manejo de Incertidumbre:**  
La lógica difusa permite trabajar con mediciones imprecisas o ruidosas de sensores sin requerir calibración exacta.

**Razonamiento Experto:**  
El sistema simula el proceso de toma de decisiones de un agrónomo experto mediante reglas lingüísticas comprensibles.

**Sin Modelo Matemático Exacto:**  
No requiere ecuaciones diferenciales complejas ni modelos físicos precisos de evapotranspiración.

**Robustez ante Ruido:**  
El sistema mantiene un comportamiento estable incluso con variaciones y ruido en las lecturas de los sensores.

**Ajuste Intuitivo:**  
Las reglas y funciones de pertenencia pueden ajustarse fácilmente mediante conocimiento experto sin necesidad de re-entrenar modelos complejos.

**Transiciones Suaves:**  
Evita cambios abruptos en la duración del riego, proporcionando una operación más estable del sistema físico.

---

## Conclusiones

### Conclusiones Técnicas

**Efectividad del Sistema Difuso:**  
El sistema de inferencia difusa proporciona respuestas suaves y graduales, evitando cambios abruptos en la duración del riego que podrían causar estrés en las plantas o ineficiencia en el uso del agua.

**Modelado Multivariable:**  
La combinación de tres variables ambientales (humedad, temperatura y radiación solar) permite modelar de manera más precisa las condiciones reales del invernadero y las necesidades hídricas de los cultivos.

**Cobertura de Casos:**  
Las 12 reglas difusas implementadas cubren adecuadamente tanto los casos típicos de operación como los escenarios extremos, proporcionando respuestas coherentes en todo el rango de operación.

**Visualización y Comprensión:**  
Las herramientas de visualización 3D y las gráficas de funciones de pertenencia facilitan significativamente la comprensión del comportamiento del sistema y permiten identificar áreas de mejora.

**Arquitectura Modular:**  
La estructura modular del código facilita el mantenimiento, la extensión del sistema y la reutilización de componentes en otros proyectos de control difuso.

### Recomendaciones

**Calibración con Datos Reales:**  
Se recomienda ajustar las funciones de pertenencia y las reglas utilizando datos históricos del invernadero específico donde se implementará el sistema.

**Variables Adicionales:**  
Considerar la inclusión de variables adicionales como humedad relativa del aire, velocidad del viento y tipo de cultivo para mejorar la precisión del sistema.

**Retroalimentación Adaptativa:**  
Implementar un sistema de aprendizaje que ajuste automáticamente las funciones de pertenencia basándose en el histórico de operación y resultados obtenidos.

**Integración IoT:**  
Desarrollar una interfaz con sensores IoT (Internet of Things) para automatización completa del sistema y monitoreo remoto en tiempo real.

**Validación Experimental:**  
Realizar pruebas de campo comparando el consumo de agua y el estado de los cultivos entre el sistema difuso y métodos tradicionales de riego.

---

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

## Reflexiones del Equipo

### Reflexión Grupal

[Espacio para que el equipo agregue su reflexión conjunta sobre el aprendizaje de lógica difusa, los desafíos enfrentados durante el desarrollo del proyecto, los logros obtenidos y la aplicabilidad de los conocimientos adquiridos.]

### Reflexiones Individuales

**Integrante 1:** [Nombre]  
[Reflexión personal sobre el proyecto, el aprendizaje de lógica difusa y la experiencia de trabajo en equipo.]

**Integrante 2:** [Nombre]  
[Reflexión personal sobre el proyecto, el aprendizaje de lógica difusa y la experiencia de trabajo en equipo.]

**Integrante 3:** [Nombre]  
[Reflexión personal sobre el proyecto, el aprendizaje de lógica difusa y la experiencia de trabajo en equipo.]

---

## Referencias

1. Zadeh, L. A. (1965). Fuzzy sets. *Information and Control*, 8(3), 338-353.

2. Mamdani, E. H., & Assilian, S. (1975). An experiment in linguistic synthesis with a fuzzy logic controller. *International Journal of Man-Machine Studies*, 7(1), 1-13.

3. Warner, J., et al. (2019). Scikit-fuzzy: Fuzzy logic toolbox for Python. *SciPy*. Disponible en: https://pythonhosted.org/scikit-fuzzy/

4. Ross, T. J. (2010). *Fuzzy Logic with Engineering Applications* (3rd ed.). John Wiley & Sons.

5. Klir, G. J., & Yuan, B. (1995). *Fuzzy Sets and Fuzzy Logic: Theory and Applications*. Prentice Hall.

---

## Licencia

Este proyecto ha sido desarrollado con fines educativos para la asignatura PRY4-LM. El código está disponible para uso académico y de aprendizaje.

---

## Información de Contacto

Para consultas, sugerencias o reporte de problemas relacionados con este proyecto:

**Repositorio del Proyecto:**  
https://github.com/Javier-Espana/PRY4-LM

**Reporte de Problemas (Issues):**  
https://github.com/Javier-Espana/PRY4-LM/issues

---

**Fecha de última actualización:** 2 de noviembre de 2025  
**Versión del Sistema:** 1.0.0  
**Estado del Proyecto:** Completo y Funcional
