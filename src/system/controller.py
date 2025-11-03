"""
Construcción y ejecución del sistema de control difuso Mamdani.
Crea el sistema de inferencia y ejecuta simulaciones.
"""
from skfuzzy import control as ctrl


def build_system(rules):
    """
    Recibe la lista de reglas y crea el sistema difuso Mamdani.
    
    Args:
        rules (list): Lista de objetos control.Rule
        
    Returns:
        ctrl.ControlSystemSimulation: Sistema de control listo para simulación
    """
    # Crear el sistema de control con todas las reglas
    control_system = ctrl.ControlSystem(rules)
    
    # Crear la simulación del sistema
    simulation = ctrl.ControlSystemSimulation(control_system)
    
    return simulation


def simulate_irrigation(system, humedad, temperatura, radiacion):
    """
    Ejecuta la simulación con valores específicos de las variables de entrada.
    
    Args:
        system (ctrl.ControlSystemSimulation): Sistema de control difuso
        humedad (float): Valor de humedad del suelo (0-100%)
        temperatura (float): Valor de temperatura ambiente (0-40°C)
        radiacion (float): Valor de radiación solar (0-1000 W/m²)
        
    Returns:
        float: Valor defuzzificado de la duración del riego (minutos)
        
    Raises:
        ValueError: Si los valores de entrada están fuera de rango
    """
    # Validar rangos de entrada
    if not (0 <= humedad <= 100):
        raise ValueError(f"Humedad fuera de rango: {humedad}. Debe estar entre 0-100%")
    
    if not (0 <= temperatura <= 40):
        raise ValueError(f"Temperatura fuera de rango: {temperatura}. Debe estar entre 0-40°C")
    
    if not (0 <= radiacion <= 1000):
        raise ValueError(f"Radiación fuera de rango: {radiacion}. Debe estar entre 0-1000 W/m²")
    
    # Asignar valores de entrada al sistema
    system.input['soil_moisture'] = humedad
    system.input['temperature'] = temperatura
    system.input['solar_radiation'] = radiacion
    
    # Ejecutar el motor de inferencia
    try:
        system.compute()
    except Exception as e:
        raise RuntimeError(f"Error en la inferencia difusa: {str(e)}")
    # Obtener y retornar el valor defuzzificado
    try:
        duration = system.output['irrigation_duration']
    except KeyError:
        # Si por alguna razón la clave no existe, intentar obtener el primer
        # valor disponible en system.output y devolverlo (mejor mensaje para el
        # usuario que un KeyError crudo).
        try:
            # system.output es similar a un dict; tomar el primer valor
            first_val = next(iter(system.output.values()))
            return float(first_val)
        except Exception:
            raise RuntimeError("Salida de inferencia no disponible: 'irrigation_duration' no encontrada")

    return float(duration)


def get_system_info(system):
    """
    Obtiene información del sistema de control difuso.
    
    Args:
        system (ctrl.ControlSystemSimulation): Sistema de control difuso
        
    Returns:
        dict: Información sobre el sistema (número de reglas, variables, etc.)
    """
    ctrl_system = system.ctrl
    
    # Convertir generator a lista
    rules_list = list(ctrl_system.rules)
    
    # Mapeo de nombres internos a nombres legibles
    nombre_legible = {
        'soil_moisture': 'Humedad del Suelo (%)',
        'temperature': 'Temperatura Ambiente (°C)',
        'solar_radiation': 'Radiación Solar (W/m²)',
        'irrigation_duration': 'Duración del Riego (min)'
    }
    
    info = {
        'num_rules': len(rules_list),
        'antecedents': [nombre_legible.get(ant.label, ant.label) for ant in ctrl_system.antecedents],
        'consequents': [nombre_legible.get(cons.label, cons.label) for cons in ctrl_system.consequents],
        'rules_labels': [rule.label for rule in rules_list if rule.label]
    }
    
    return info
