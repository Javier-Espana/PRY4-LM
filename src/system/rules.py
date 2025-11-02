"""
Definición de reglas difusas del sistema de inferencia Mamdani.
Contiene las 12 reglas lingüísticas del sistema de riego.
"""
from skfuzzy import control as ctrl


def define_rules(vars):
    """
    Crea las 12 reglas difusas del sistema de riego para invernadero.
    
    Args:
        vars (dict): Diccionario con las variables difusas (antecedentes y consecuente)
        
    Returns:
        list: Lista de objetos control.Rule del sistema difuso
    """
    sm = vars['soil_moisture']  # Humedad del suelo
    temp = vars['temperature']  # Temperatura
    rad = vars['solar_radiation']  # Radiación solar
    duration = vars['irrigation_duration']  # Duración del riego
    
    rules = []
    
    # ============================================
    # REGLAS DEL SISTEMA DE RIEGO
    # ============================================
    
    # Regla 1: Condiciones extremas de sequía y calor
    rule1 = ctrl.Rule(
        sm['muy_seca'] & temp['caliente'] & rad['alta'],
        duration['larga'],
        label='R1: Muy seca + Caliente + Radiación alta'
    )
    rules.append(rule1)
    
    # Regla 2: Muy seca con calor y radiación media
    rule2 = ctrl.Rule(
        sm['muy_seca'] & temp['caliente'] & rad['media'],
        duration['larga'],
        label='R2: Muy seca + Caliente + Radiación media'
    )
    rules.append(rule2)
    
    # Regla 3: Muy seca con temperatura templada
    rule3 = ctrl.Rule(
        sm['muy_seca'] & temp['templado'],
        duration['larga'],
        label='R3: Muy seca + Templado'
    )
    rules.append(rule3)
    
    # Regla 4: Seca con temperatura caliente
    rule4 = ctrl.Rule(
        sm['seca'] & temp['caliente'],
        duration['media'],
        label='R4: Seca + Caliente'
    )
    rules.append(rule4)
    
    # Regla 5: Seca con radiación alta
    rule5 = ctrl.Rule(
        sm['seca'] & rad['alta'],
        duration['media'],
        label='R5: Seca + Radiación alta'
    )
    rules.append(rule5)
    
    # Regla 6: Humedad normal pero condiciones extremas
    rule6 = ctrl.Rule(
        sm['normal'] & temp['caliente'] & rad['alta'],
        duration['media'],
        label='R6: Normal + Caliente + Radiación alta'
    )
    rules.append(rule6)
    
    # Regla 7: Humedad normal con radiación baja
    rule7 = ctrl.Rule(
        sm['normal'] & rad['baja'],
        duration['corta'],
        label='R7: Normal + Radiación baja'
    )
    rules.append(rule7)
    
    # Regla 8: Suelo húmedo (prioridad máxima - poco riego)
    rule8 = ctrl.Rule(
        sm['humeda'],
        duration['muy_corta'],
        label='R8: Húmeda'
    )
    rules.append(rule8)
    
    # Regla 9: Seca con frío
    rule9 = ctrl.Rule(
        sm['seca'] & temp['frio'],
        duration['corta'],
        label='R9: Seca + Frío'
    )
    rules.append(rule9)
    
    # Regla 10: Muy seca pero con frío
    rule10 = ctrl.Rule(
        sm['muy_seca'] & temp['frio'],
        duration['media'],
        label='R10: Muy seca + Frío'
    )
    rules.append(rule10)
    
    # Regla 11: Radiación alta con calor (evaporación alta)
    rule11 = ctrl.Rule(
        rad['alta'] & temp['caliente'],
        duration['media'],
        label='R11: Radiación alta + Caliente'
    )
    rules.append(rule11)
    
    # Regla 12: Condiciones moderadas en todo
    rule12 = ctrl.Rule(
        sm['normal'] & temp['templado'] & rad['media'],
        duration['corta'],
        label='R12: Normal + Templado + Radiación media'
    )
    rules.append(rule12)
    
    return rules
