"""
Definición de variables difusas (universes of discourse).
Define los rangos numéricos para cada variable de entrada y salida.
"""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def define_universes():
    """
    Crea y devuelve los universos (rangos numéricos) para cada variable difusa.
    
    Returns:
        dict: Diccionario con las variables de entrada y salida:
            - 'soil_moisture': Antecedent para humedad del suelo [0-100]%
            - 'temperature': Antecedent para temperatura ambiente [0-40]°C
            - 'solar_radiation': Antecedent para radiación solar [0-1000] W/m²
            - 'irrigation_duration': Consequent para duración del riego [0-30] min
    """
    # Variables de entrada (Antecedents)
    soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_moisture')
    temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
    solar_radiation = ctrl.Antecedent(np.arange(0, 1001, 10), 'solar_radiation')
    
    # Variable de salida (Consequent)
    irrigation_duration = ctrl.Consequent(np.arange(0, 31, 1), 'irrigation_duration')
    
    return {
        'soil_moisture': soil_moisture,
        'temperature': temperature,
        'solar_radiation': solar_radiation,
        'irrigation_duration': irrigation_duration
    }
