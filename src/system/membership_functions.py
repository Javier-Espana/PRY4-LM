"""
Definición de funciones de pertenencia (membership functions).
Define las funciones triangulares y trapezoidales para cada variable.
"""
import skfuzzy as fuzz


def define_memberships(universes):
    """
    Define todas las funciones de pertenencia para las variables de entrada y salida.
    
    Args:
        universes (dict): Diccionario con las variables Antecedent y Consequent
        
    Returns:
        dict: Diccionario con las variables configuradas con sus funciones de pertenencia:
            - 'soil_moisture': con membresías muy_seca, seca, normal, humeda
            - 'temperature': con membresías frio, templado, caliente
            - 'solar_radiation': con membresías baja, media, alta
            - 'irrigation_duration': con membresías muy_corta, corta, media, larga
    """
    soil_moisture = universes['soil_moisture']
    temperature = universes['temperature']
    solar_radiation = universes['solar_radiation']
    irrigation_duration = universes['irrigation_duration']
    
    # ============================================
    # HUMEDAD DEL SUELO (0-100%)
    # ============================================
    soil_moisture['muy_seca'] = fuzz.trapmf(soil_moisture.universe, [0, 0, 10, 20])
    soil_moisture['seca'] = fuzz.trimf(soil_moisture.universe, [10, 30, 50])
    soil_moisture['normal'] = fuzz.trimf(soil_moisture.universe, [40, 60, 80])
    soil_moisture['humeda'] = fuzz.trapmf(soil_moisture.universe, [70, 85, 100, 100])
    
    # ============================================
    # TEMPERATURA (0-40°C)
    # ============================================
    temperature['frio'] = fuzz.trapmf(temperature.universe, [0, 0, 10, 15])
    temperature['templado'] = fuzz.trimf(temperature.universe, [10, 22, 30])
    temperature['caliente'] = fuzz.trapmf(temperature.universe, [25, 32, 40, 40])
    
    # ============================================
    # RADIACIÓN SOLAR (0-1000 W/m²)
    # ============================================
    solar_radiation['baja'] = fuzz.trapmf(solar_radiation.universe, [0, 0, 200, 350])
    solar_radiation['media'] = fuzz.trimf(solar_radiation.universe, [250, 500, 750])
    solar_radiation['alta'] = fuzz.trapmf(solar_radiation.universe, [650, 800, 1000, 1000])
    
    # ============================================
    # DURACIÓN DEL RIEGO (0-30 min)
    # ============================================
    irrigation_duration['muy_corta'] = fuzz.trapmf(irrigation_duration.universe, [0, 0, 3, 6])
    irrigation_duration['corta'] = fuzz.trimf(irrigation_duration.universe, [4, 8, 12])
    irrigation_duration['media'] = fuzz.trimf(irrigation_duration.universe, [10, 17, 24])
    irrigation_duration['larga'] = fuzz.trapmf(irrigation_duration.universe, [20, 25, 30, 30])
    
    return {
        'soil_moisture': soil_moisture,
        'temperature': temperature,
        'solar_radiation': solar_radiation,
        'irrigation_duration': irrigation_duration
    }
