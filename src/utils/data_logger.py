"""
Registro y almacenamiento de resultados de simulaciones.
Guarda datos en formato CSV y JSON para análisis posterior.
"""
import csv
import json
import os
from datetime import datetime


class DataLogger:
    """
    Clase para registrar y almacenar resultados de simulaciones del sistema de riego.
    """
    
    def __init__(self, log_dir='logs'):
        """
        Inicializa el logger de datos.
        
        Args:
            log_dir (str): Directorio donde se guardarán los logs
        """
        self.log_dir = log_dir
        self.csv_file = None
        self.json_file = None
        self.session_id = None
        self.results = []
        
        # Crear directorio de logs si no existe
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"✓ Directorio de logs creado: {log_dir}")
    
    def start_session(self, session_name=None):
        """
        Inicia una nueva sesión de registro.
        
        Args:
            session_name (str, optional): Nombre personalizado para la sesión
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if session_name:
            self.session_id = f"{session_name}_{timestamp}"
        else:
            self.session_id = f"session_{timestamp}"
        
        # Configurar nombres de archivos
        self.csv_file = os.path.join(self.log_dir, f"{self.session_id}.csv")
        self.json_file = os.path.join(self.log_dir, f"{self.session_id}.json")
        
        # Crear archivo CSV con encabezados
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'caso', 'humedad_suelo_%', 'temperatura_C',
                'radiacion_W_m2', 'duracion_riego_min', 'notas'
            ])
        
        print(f"\n✓ Sesión iniciada: {self.session_id}")
        print(f"  - CSV: {self.csv_file}")
        print(f"  - JSON: {self.json_file}")
        
        self.results = []
    
    def log_simulation(self, input_values, output_value, notes=''):
        """
        Registra el resultado de una simulación.
        
        Args:
            input_values (dict): Valores de entrada {'humedad', 'temperatura', 'radiacion'}
            output_value (float): Valor de salida (duración del riego)
            notes (str, optional): Notas adicionales sobre la simulación
        """
        if not self.session_id:
            print("Advertencia: No hay sesión activa. Iniciando sesión automática...")
            self.start_session()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Crear registro
        record = {
            'timestamp': timestamp,
            'caso': input_values.get('nombre', 'Sin nombre'),
            'humedad': input_values.get('humedad', 0),
            'temperatura': input_values.get('temperatura', 0),
            'radiacion': input_values.get('radiacion', 0),
            'duracion': round(output_value, 2),
            'notas': notes
        }
        
        # Guardar en lista
        self.results.append(record)
        
        # Escribir en CSV
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                record['timestamp'],
                record['caso'],
                record['humedad'],
                record['temperatura'],
                record['radiacion'],
                record['duracion'],
                record['notas']
            ])
        
        return record
    
    def save_summary(self, additional_info=None):
        """
        Guarda un resumen completo de la sesión en formato JSON.
        
        Args:
            additional_info (dict, optional): Información adicional a incluir
        """
        if not self.session_id:
            print("No hay sesión activa para guardar.")
            return
        
        # Calcular estadísticas
        duraciones = [r['duracion'] for r in self.results]
        
        summary = {
            'session_id': self.session_id,
            'timestamp_inicio': self.results[0]['timestamp'] if self.results else None,
            'timestamp_fin': self.results[-1]['timestamp'] if self.results else None,
            'num_simulaciones': len(self.results),
            'estadisticas': {
                'duracion_min': min(duraciones) if duraciones else 0,
                'duracion_max': max(duraciones) if duraciones else 0,
                'duracion_promedio': sum(duraciones) / len(duraciones) if duraciones else 0
            },
            'resultados': self.results
        }
        
        if additional_info:
            summary['informacion_adicional'] = additional_info
        
        # Guardar en JSON
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Resumen guardado en: {self.json_file}")
        print(f"  - Total de simulaciones: {len(self.results)}")
        print(f"  - Duración mín/máx/prom: {summary['estadisticas']['duracion_min']:.2f} / "
              f"{summary['estadisticas']['duracion_max']:.2f} / "
              f"{summary['estadisticas']['duracion_promedio']:.2f} min")
        
        return summary
    
    def get_results(self):
        """
        Obtiene todos los resultados registrados en la sesión actual.
        
        Returns:
            list: Lista de diccionarios con los resultados
        """
        return self.results
    
    def print_summary(self):
        """
        Imprime un resumen de la sesión actual en consola.
        """
        if not self.results:
            print("\nNo hay resultados registrados.")
            return
        
        print("\n" + "="*70)
        print(f"RESUMEN DE LA SESIÓN: {self.session_id}")
        print("="*70)
        print(f"Total de simulaciones: {len(self.results)}")
        print("\nResultados:")
        print("-"*70)
        print(f"{'#':<4} {'Caso':<25} {'H%':<6} {'T°C':<6} {'R W/m²':<8} {'Dur.(min)':<10}")
        print("-"*70)
        
        for i, r in enumerate(self.results, 1):
            print(f"{i:<4} {r['caso']:<25} {r['humedad']:<6.1f} {r['temperatura']:<6.1f} "
                  f"{r['radiacion']:<8.0f} {r['duracion']:<10.2f}")
        
        print("-"*70)
        
        # Estadísticas
        duraciones = [r['duracion'] for r in self.results]
        print(f"\nEstadísticas de Duración:")
        print(f"  - Mínima:   {min(duraciones):.2f} min")
        print(f"  - Máxima:   {max(duraciones):.2f} min")
        print(f"  - Promedio: {sum(duraciones)/len(duraciones):.2f} min")
        print("="*70)


def load_session(json_file):
    """
    Carga una sesión guardada desde un archivo JSON.
    
    Args:
        json_file (str): Ruta al archivo JSON
        
    Returns:
        dict: Datos de la sesión
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Sesión cargada: {data['session_id']}")
        return data
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {json_file}")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo {json_file} no es un JSON válido")
        return None


def compare_sessions(json_files):
    """
    Compara múltiples sesiones guardadas.
    
    Args:
        json_files (list): Lista de rutas a archivos JSON
        
    Returns:
        dict: Comparación de sesiones
    """
    sessions = []
    
    for file in json_files:
        data = load_session(file)
        if data:
            sessions.append(data)
    
    if not sessions:
        print("No se pudieron cargar sesiones para comparar.")
        return None
    
    print("\n" + "="*70)
    print("COMPARACIÓN DE SESIONES")
    print("="*70)
    
    for session in sessions:
        print(f"\nSesión: {session['session_id']}")
        print(f"  - Simulaciones: {session['num_simulaciones']}")
        print(f"  - Duración promedio: {session['estadisticas']['duracion_promedio']:.2f} min")
        print(f"  - Rango: [{session['estadisticas']['duracion_min']:.2f}, "
              f"{session['estadisticas']['duracion_max']:.2f}] min")
    
    print("="*70)
    
    return sessions
