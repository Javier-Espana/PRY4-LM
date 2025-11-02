"""
Manejo de datos de entrada para el sistema de riego.
Proporciona funciones para obtener datos de prueba y validación.
"""


def get_sample_inputs():
    """
    Devuelve un conjunto de valores de prueba representativos para el sistema.
    
    Returns:
        list: Lista de diccionarios con casos de prueba:
            - humedad: 0-100%
            - temperatura: 0-40°C
            - radiacion: 0-1000 W/m²
    """
    samples = [
        # Caso 1: Condiciones extremas - muy seco, muy caliente, alta radiación
        {
            'nombre': 'Condiciones extremas',
            'humedad': 15,
            'temperatura': 35,
            'radiacion': 900
        },
        # Caso 2: Suelo seco, temperatura media, radiación alta
        {
            'nombre': 'Seco con radiación alta',
            'humedad': 30,
            'temperatura': 25,
            'radiacion': 750
        },
        # Caso 3: Condiciones normales
        {
            'nombre': 'Condiciones normales',
            'humedad': 60,
            'temperatura': 22,
            'radiacion': 500
        },
        # Caso 4: Suelo húmedo - poco riego necesario
        {
            'nombre': 'Suelo húmedo',
            'humedad': 80,
            'temperatura': 20,
            'radiacion': 400
        },
        # Caso 5: Frío con humedad baja
        {
            'nombre': 'Frío y seco',
            'humedad': 25,
            'temperatura': 12,
            'radiacion': 300
        },
        # Caso 6: Muy seco pero frío
        {
            'nombre': 'Muy seco pero frío',
            'humedad': 10,
            'temperatura': 8,
            'radiacion': 200
        },
        # Caso 7: Normal con poca radiación
        {
            'nombre': 'Normal con poca luz',
            'humedad': 65,
            'temperatura': 18,
            'radiacion': 150
        },
        # Caso 8: Calor moderado, seco
        {
            'nombre': 'Calor moderado y seco',
            'humedad': 35,
            'temperatura': 28,
            'radiacion': 600
        }
    ]
    
    return samples


def validate_input(humedad, temperatura, radiacion):
    """
    Valida que los valores de entrada estén dentro de los rangos permitidos.
    
    Args:
        humedad (float): Humedad del suelo (0-100%)
        temperatura (float): Temperatura ambiente (0-40°C)
        radiacion (float): Radiación solar (0-1000 W/m²)
        
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
    """
    if not (0 <= humedad <= 100):
        return False, f"Humedad ({humedad}%) fuera de rango válido: 0-100%"
    
    if not (0 <= temperatura <= 40):
        return False, f"Temperatura ({temperatura}°C) fuera de rango válido: 0-40°C"
    
    if not (0 <= radiacion <= 1000):
        return False, f"Radiación ({radiacion} W/m²) fuera de rango válido: 0-1000 W/m²"
    
    return True, "Valores válidos"


def get_custom_input():
    """
    Solicita valores personalizados al usuario vía consola.
    
    Returns:
        dict: Diccionario con los valores ingresados
    """
    print("\n" + "="*50)
    print("INGRESO DE VALORES PERSONALIZADOS")
    print("="*50)
    
    while True:
        try:
            humedad = float(input("\nHumedad del suelo (0-100%): "))
            temperatura = float(input("Temperatura ambiente (0-40°C): "))
            radiacion = float(input("Radiación solar (0-1000 W/m²): "))
            
            es_valido, mensaje = validate_input(humedad, temperatura, radiacion)
            
            if es_valido:
                return {
                    'nombre': 'Entrada personalizada',
                    'humedad': humedad,
                    'temperatura': temperatura,
                    'radiacion': radiacion
                }
            else:
                print(f"\nError: {mensaje}")
                print("Por favor, ingrese valores dentro de los rangos válidos.\n")
                
        except ValueError:
            print("\n❌ Error: Debe ingresar valores numéricos válidos.\n")
        except KeyboardInterrupt:
            print("\n\nEntrada cancelada por el usuario.")
            return None


def get_extreme_cases():
    """
    Devuelve casos extremos para probar los límites del sistema.
    
    Returns:
        list: Lista de casos extremos
    """
    extreme_cases = [
        {
            'nombre': 'Mínimo absoluto',
            'humedad': 0,
            'temperatura': 0,
            'radiacion': 0
        },
        {
            'nombre': 'Máximo absoluto',
            'humedad': 100,
            'temperatura': 40,
            'radiacion': 1000
        },
        {
            'nombre': 'Desierto diurno',
            'humedad': 5,
            'temperatura': 40,
            'radiacion': 1000
        },
        {
            'nombre': 'Invernadero saturado',
            'humedad': 95,
            'temperatura': 15,
            'radiacion': 100
        }
    ]
    
    return extreme_cases
