"""
Sistema de Control Difuso para Riego de Invernadero
====================================================

Este sistema utiliza lógica difusa (fuzzy logic) para determinar la duración
óptima del riego en un invernadero considerando:
- Humedad del suelo (0-100%)
- Temperatura ambiente (0-40°C)
- Radiación solar (0-1000 W/m²)

Salida: Duración del riego en minutos (0-30 min)

Autor: Equipo PRY4-LM
Fecha: Noviembre 2025
"""

import sys
import os

# Añadir el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from system.variables import define_universes
from system.membership_functions import define_memberships
from system.rules import define_rules
from system.controller import build_system, simulate_irrigation, get_system_info
from utils.inputs import get_sample_inputs, get_extreme_cases, get_custom_input
from utils.visualization import (plot_memberships, plot_surface, 
                                  plot_simulation_result, plot_multiple_simulations)
from utils.data_logger import DataLogger


def print_header():
    """Imprime el encabezado del programa."""
    print("\n" + "="*70)
    print(" "*10 + "SISTEMA DE CONTROL DIFUSO PARA RIEGO DE INVERNADERO")
    print("="*70)
    print("Variables de Entrada:")
    print("  • Humedad del Suelo: 0-100%")
    print("  • Temperatura Ambiente: 0-40°C")
    print("  • Radiación Solar: 0-1000 W/m²")
    print("\nVariable de Salida:")
    print("  • Duración del Riego: 0-30 minutos")
    print("="*70 + "\n")


def print_menu():
    """Imprime el menú de opciones."""
    print("\n" + "─"*70)
    print("MENÚ DE OPCIONES")
    print("─"*70)
    print("1. Ejecutar casos de prueba predefinidos")
    print("2. Ejecutar casos extremos")
    print("3. Ingresar valores personalizados")
    print("4. Visualizar funciones de pertenencia")
    print("5. Visualizar superficie de control 3D")
    print("6. Visualizar resultado de simulación específica")
    print("7. Ver información del sistema")
    print("8. Ver resumen de sesión actual")
    print("0. Salir")
    print("─"*70)


def execute_simulations(system, samples, logger, show_details=True):
    """
    Ejecuta múltiples simulaciones y registra los resultados.
    
    Args:
        system: Sistema de control difuso
        samples: Lista de casos de prueba
        logger: DataLogger para registrar resultados
        show_details: Si True, muestra detalles de cada simulación
    
    Returns:
        list: Lista de resultados
    """
    results = []
    
    print("\n" + "="*70)
    print("EJECUTANDO SIMULACIONES")
    print("="*70)
    
    for i, sample in enumerate(samples, 1):
        nombre = sample['nombre']
        humedad = sample['humedad']
        temperatura = sample['temperatura']
        radiacion = sample['radiacion']
        
        if show_details:
            print(f"\n[{i}/{len(samples)}] {nombre}")
            print(f"  └─ Entradas: H={humedad}%, T={temperatura}°C, R={radiacion} W/m²")
        
        try:
            # Ejecutar simulación
            duracion = simulate_irrigation(system, humedad, temperatura, radiacion)
            
            if show_details:
                print(f"  └─ Salida: Duración del riego = {duracion:.2f} minutos")
            
            # Registrar resultado
            logger.log_simulation(sample, duracion)
            
            # Guardar para comparación
            result = {
                'nombre': nombre,
                'humedad': humedad,
                'temperatura': temperatura,
                'radiacion': radiacion,
                'duracion': duracion
            }
            results.append(result)
            
        except Exception as e:
            print(f"  └─ Error: {str(e)}")
    
    print("\n" + "="*70)
    print(f"✓ Simulaciones completadas: {len(results)}/{len(samples)}")
    print("="*70)
    
    return results


def main():
    """Función principal del programa."""
    
    print_header()
    
    print("Inicializando sistema de control difuso...")
    
    # 1. Definir universos de discurso
    print("  [1/5] Definiendo universos de variables...")
    universes = define_universes()
    
    # 2. Definir funciones de pertenencia
    print("  [2/5] Configurando funciones de pertenencia...")
    vars = define_memberships(universes)
    
    # 3. Definir reglas difusas
    print("  [3/5] Estableciendo reglas del sistema...")
    rules = define_rules(vars)
    
    # 4. Construir sistema de control
    print("  [4/5] Construyendo sistema de inferencia Mamdani...")
    system = build_system(rules)
    
    # 5. Inicializar logger
    print("  [5/5] Inicializando registro de datos...")
    logger = DataLogger(log_dir='logs')
    logger.start_session('riego_invernadero')
    
    print("\nSistema inicializado correctamente")
    
    # Bucle principal del menú
    while True:
        print_menu()
        
        try:
            opcion = input("\nSeleccione una opción (0-8): ").strip()
            
            if opcion == '0':
                # Salir
                print("\nGuardando resumen de la sesión...")
                logger.save_summary({
                    'descripcion': 'Sistema de Control Difuso para Riego de Invernadero',
                    'variables_entrada': ['Humedad del suelo', 'Temperatura', 'Radiación solar'],
                    'variable_salida': 'Duración del riego',
                    'tipo_sistema': 'Mamdani',
                    'num_reglas': len(rules)
                })
                print("\nGracias por usar el sistema. ¡Hasta pronto!")
                break
            
            elif opcion == '1':
                # Casos predefinidos
                samples = get_sample_inputs()
                results = execute_simulations(system, samples, logger)
                
                # Mostrar comparación gráfica
                respuesta = input("\n¿Desea ver la comparación gráfica? (s/n): ").strip().lower()
                if respuesta == 's':
                    plot_multiple_simulations(results)
            
            elif opcion == '2':
                # Casos extremos
                samples = get_extreme_cases()
                results = execute_simulations(system, samples, logger)
                
                respuesta = input("\n¿Desea ver la comparación gráfica? (s/n): ").strip().lower()
                if respuesta == 's':
                    plot_multiple_simulations(results)
            
            elif opcion == '3':
                # Entrada personalizada
                sample = get_custom_input()
                if sample:
                    results = execute_simulations(system, [sample], logger)
                    
                    if results:
                        respuesta = input("\n¿Desea ver el resultado gráfico? (s/n): ").strip().lower()
                        if respuesta == 's':
                            plot_simulation_result(system, sample, results[0]['duracion'], vars)
            
            elif opcion == '4':
                # Visualizar funciones de pertenencia
                print("\nGenerando gráficas de funciones de pertenencia...")
                plot_memberships(vars, save_path='logs/funciones_pertenencia.png')
            
            elif opcion == '5':
                # Superficie 3D
                print("\nSeleccione las variables para la superficie 3D:")
                print("1. Humedad vs Temperatura (Radiación fija)")
                print("2. Humedad vs Radiación (Temperatura fija)")
                print("3. Temperatura vs Radiación (Humedad fija)")
                
                sub_opcion = input("\nSeleccione (1-3): ").strip()
                
                if sub_opcion == '1':
                    rad_fija = float(input("Valor de radiación fija (0-1000): "))
                    plot_surface(system, vars, 'soil_moisture', 'temperature',
                               'solar_radiation', rad_fija,
                               save_path='logs/superficie_humedad_temp.png')
                elif sub_opcion == '2':
                    temp_fija = float(input("Valor de temperatura fija (0-40): "))
                    plot_surface(system, vars, 'soil_moisture', 'solar_radiation',
                               'temperature', temp_fija,
                               save_path='logs/superficie_humedad_rad.png')
                elif sub_opcion == '3':
                    hum_fija = float(input("Valor de humedad fija (0-100): "))
                    plot_surface(system, vars, 'temperature', 'solar_radiation',
                               'soil_moisture', hum_fija,
                               save_path='logs/superficie_temp_rad.png')
                else:
                    print("Opción no válida")
            
            elif opcion == '6':
                # Visualizar simulación específica
                sample = get_custom_input()
                if sample:
                    duracion = simulate_irrigation(system, sample['humedad'],
                                                  sample['temperatura'], sample['radiacion'])
                    print(f"\nDuración calculada: {duracion:.2f} minutos")
                    plot_simulation_result(system, sample, duracion, vars)
            
            elif opcion == '7':
                # Información del sistema
                info = get_system_info(system)
                print("\n" + "="*70)
                print("INFORMACIÓN DEL SISTEMA DE CONTROL DIFUSO")
                print("="*70)
                print(f"Número de reglas: {info['num_rules']}")
                print(f"\nVariables de entrada (Antecedentes):")
                for ant in info['antecedents']:
                    print(f"  • {ant}")
                print(f"\nVariables de salida (Consecuentes):")
                for cons in info['consequents']:
                    print(f"  • {cons}")
                print(f"\nReglas definidas:")
                for i, label in enumerate(info['rules_labels'], 1):
                    print(f"  {i:2d}. {label}")
                print("="*70)
            
            elif opcion == '8':
                # Resumen de sesión
                logger.print_summary()
            
            else:
                print("\nOpción no válida. Por favor, seleccione un número del 0 al 8.")
        
        except KeyboardInterrupt:
            print("\n\nProceso interrumpido por el usuario.")
            print("Guardando resumen...")
            logger.save_summary()
            break
        except Exception as e:
            print(f"\nError inesperado: {str(e)}")
            print("Por favor, intente de nuevo.")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\nError crítico: {str(e)}")
        print("El programa se cerrará.")
        sys.exit(1)
