"""
Funciones de visualización para el sistema de control difuso.
Genera gráficas de funciones de pertenencia y superficies de decisión.
"""
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def plot_memberships(vars, save_path=None):
    """
    Genera y muestra gráficas de las funciones de pertenencia para cada variable.
    
    Args:
        vars (dict): Diccionario con las variables difusas
        save_path (str, optional): Ruta para guardar la figura. Si es None, solo muestra.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Funciones de Pertenencia del Sistema de Riego', 
                 fontsize=16, fontweight='bold')
    
    # ============================================
    # 1. HUMEDAD DEL SUELO
    # ============================================
    ax = axes[0, 0]
    sm = vars['soil_moisture']
    
    for term in sm.terms:
        ax.plot(sm.universe, sm[term].mf, linewidth=2, label=term.replace('_', ' ').title())
    
    ax.set_title('Humedad del Suelo', fontsize=12, fontweight='bold')
    ax.set_xlabel('Humedad (%)', fontsize=10)
    ax.set_ylabel('Grado de Pertenencia', fontsize=10)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 100])
    ax.set_ylim([-0.05, 1.05])
    
    # ============================================
    # 2. TEMPERATURA
    # ============================================
    ax = axes[0, 1]
    temp = vars['temperature']
    
    for term in temp.terms:
        ax.plot(temp.universe, temp[term].mf, linewidth=2, label=term.replace('_', ' ').title())
    
    ax.set_title('Temperatura Ambiente', fontsize=12, fontweight='bold')
    ax.set_xlabel('Temperatura (°C)', fontsize=10)
    ax.set_ylabel('Grado de Pertenencia', fontsize=10)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 40])
    ax.set_ylim([-0.05, 1.05])
    
    # ============================================
    # 3. RADIACIÓN SOLAR
    # ============================================
    ax = axes[1, 0]
    rad = vars['solar_radiation']
    
    for term in rad.terms:
        ax.plot(rad.universe, rad[term].mf, linewidth=2, label=term.replace('_', ' ').title())
    
    ax.set_title('Radiación Solar', fontsize=12, fontweight='bold')
    ax.set_xlabel('Radiación (W/m²)', fontsize=10)
    ax.set_ylabel('Grado de Pertenencia', fontsize=10)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1000])
    ax.set_ylim([-0.05, 1.05])
    
    # ============================================
    # 4. DURACIÓN DEL RIEGO
    # ============================================
    ax = axes[1, 1]
    duration = vars['irrigation_duration']
    
    for term in duration.terms:
        ax.plot(duration.universe, duration[term].mf, linewidth=2, 
                label=term.replace('_', ' ').title())
    
    ax.set_title('Duración del Riego (Salida)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Duración (minutos)', fontsize=10)
    ax.set_ylabel('Grado de Pertenencia', fontsize=10)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 30])
    ax.set_ylim([-0.05, 1.05])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfica guardada en: {save_path}")
    
    plt.show()


def plot_surface(system, vars, var_x='soil_moisture', var_y='temperature', 
                 fixed_var=None, fixed_value=500, save_path=None):
    """
    Genera una superficie 3D mostrando la relación entre dos variables de entrada
    y la duración del riego.
    
    Args:
        system: Sistema de control difuso (ControlSystemSimulation)
        vars (dict): Diccionario con las variables difusas
        var_x (str): Nombre de la primera variable ('soil_moisture', 'temperature', 'solar_radiation')
        var_y (str): Nombre de la segunda variable
        fixed_var (str): Variable a mantener fija (si hay tres variables)
        fixed_value (float): Valor fijo de la tercera variable
        save_path (str, optional): Ruta para guardar la figura
    """
    # Configuración de variables y rangos
    var_configs = {
        'soil_moisture': {
            'range': np.arange(0, 101, 5),
            'label': 'Humedad del Suelo (%)',
            'default': 50
        },
        'temperature': {
            'range': np.arange(0, 41, 2),
            'label': 'Temperatura (°C)',
            'default': 20
        },
        'solar_radiation': {
            'range': np.arange(0, 1001, 50),
            'label': 'Radiación Solar (W/m²)',
            'default': 500
        }
    }
    
    # Obtener rangos y configuraciones
    x_range = var_configs[var_x]['range']
    y_range = var_configs[var_y]['range']
    x_label = var_configs[var_x]['label']
    y_label = var_configs[var_y]['label']
    
    # Determinar la variable fija
    all_vars = ['soil_moisture', 'temperature', 'solar_radiation']
    if fixed_var is None:
        remaining = [v for v in all_vars if v not in [var_x, var_y]]
        fixed_var = remaining[0] if remaining else 'solar_radiation'
    
    fixed_label = var_configs[fixed_var]['label']
    
    # Crear malla de valores
    x_mesh, y_mesh = np.meshgrid(x_range, y_range)
    z_output = np.zeros_like(x_mesh, dtype=float)
    
    # Calcular la salida para cada combinación
    print(f"\nGenerando superficie 3D ({x_label} vs {y_label})...")
    print(f"Variable fija: {fixed_label} = {fixed_value}")
    
    for i in range(x_mesh.shape[0]):
        for j in range(x_mesh.shape[1]):
            inputs = {
                'soil_moisture': 50,
                'temperature': 20,
                'solar_radiation': 500
            }
            
            inputs[var_x] = x_mesh[i, j]
            inputs[var_y] = y_mesh[i, j]
            inputs[fixed_var] = fixed_value
            
            try:
                system.input['soil_moisture'] = inputs['soil_moisture']
                system.input['temperature'] = inputs['temperature']
                system.input['solar_radiation'] = inputs['solar_radiation']
                system.compute()
                z_output[i, j] = system.output['irrigation_duration']
            except:
                z_output[i, j] = np.nan
    
    # Crear figura 3D
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Superficie con mapa de colores
    surf = ax.plot_surface(x_mesh, y_mesh, z_output, cmap='viridis',
                           alpha=0.9, edgecolor='none', antialiased=True)
    
    # Etiquetas y título
    ax.set_xlabel(x_label, fontsize=11, labelpad=10)
    ax.set_ylabel(y_label, fontsize=11, labelpad=10)
    ax.set_zlabel('Duración del Riego (min)', fontsize=11, labelpad=10)
    ax.set_title(f'Superficie de Control Difuso\n{fixed_label} = {fixed_value}',
                 fontsize=13, fontweight='bold', pad=20)
    
    # Barra de colores
    cbar = fig.colorbar(surf, ax=ax, shrink=0.6, aspect=10)
    cbar.set_label('Duración (min)', fontsize=10)
    
    # Configuración de vista
    ax.view_init(elev=25, azim=45)
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Superficie 3D guardada en: {save_path}")
    
    plt.show()


def plot_simulation_result(system, input_values, output_value, vars):
    """
    Visualiza el resultado de una simulación específica mostrando los grados de
    activación de cada función de pertenencia.
    
    Args:
        system: Sistema de control difuso
        input_values (dict): Valores de entrada usados
        output_value (float): Valor de salida calculado
        vars (dict): Diccionario con las variables difusas
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'Resultado de Simulación - Duración: {output_value:.2f} min',
                 fontsize=14, fontweight='bold')
    
    # Humedad del suelo (mostrar grado de activación de cada término)
    ax = axes[0, 0]
    sm = vars['soil_moisture']
    hum_val = input_values.get('humedad', input_values.get('soil_moisture', 0))

    for term in sm.terms:
        mf = sm[term].mf
        ax.plot(sm.universe, mf, linewidth=2, label=term.replace('_', ' ').title())

        # grado de activación (interpolación de la mf en el valor de entrada)
        try:
            degree = float(np.interp(hum_val, sm.universe, mf))
        except Exception:
            degree = 0.0

        # sombrear la porción activada (clipping de la mf al grado)
        ax.fill_between(sm.universe, 0, np.minimum(mf, degree), alpha=0.25)

    ax.axvline(hum_val, color='red', linestyle='--', linewidth=2,
               label=f"Valor: {hum_val:.1f}%")
    ax.set_title('Humedad del Suelo', fontweight='bold')
    ax.set_xlabel('Humedad (%)')
    ax.set_ylabel('Grado de Pertenencia')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # Temperatura (mostrar grado de activación)
    ax = axes[0, 1]
    temp = vars['temperature']
    temp_val = input_values.get('temperatura', input_values.get('temperature', 0))

    for term in temp.terms:
        mf = temp[term].mf
        ax.plot(temp.universe, mf, linewidth=2, label=term.replace('_', ' ').title())
        try:
            degree = float(np.interp(temp_val, temp.universe, mf))
        except Exception:
            degree = 0.0
        ax.fill_between(temp.universe, 0, np.minimum(mf, degree), alpha=0.25)

    ax.axvline(temp_val, color='red', linestyle='--', linewidth=2,
               label=f"Valor: {temp_val:.1f}°C")
    ax.set_title('Temperatura', fontweight='bold')
    ax.set_xlabel('Temperatura (°C)')
    ax.set_ylabel('Grado de Pertenencia')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # Radiación solar (mostrar grado de activación)
    ax = axes[1, 0]
    rad = vars['solar_radiation']
    rad_val = input_values.get('radiacion', input_values.get('solar_radiation', 0))

    for term in rad.terms:
        mf = rad[term].mf
        ax.plot(rad.universe, mf, linewidth=2, label=term.replace('_', ' ').title())
        try:
            degree = float(np.interp(rad_val, rad.universe, mf))
        except Exception:
            degree = 0.0
        ax.fill_between(rad.universe, 0, np.minimum(mf, degree), alpha=0.25)

    ax.axvline(rad_val, color='red', linestyle='--', linewidth=2,
               label=f"Valor: {rad_val:.1f} W/m²")
    ax.set_title('Radiación Solar', fontweight='bold')
    ax.set_xlabel('Radiación (W/m²)')
    ax.set_ylabel('Grado de Pertenencia')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # Duración (salida) — mostrar nivel de pertenencia en el valor defuzzificado
    ax = axes[1, 1]
    duration = vars['irrigation_duration']
    out_val = output_value

    for term in duration.terms:
        mf = duration[term].mf
        ax.plot(duration.universe, mf, linewidth=2,
                label=term.replace('_', ' ').title())
        try:
            degree = float(np.interp(out_val, duration.universe, mf))
        except Exception:
            degree = 0.0
        ax.fill_between(duration.universe, 0, np.minimum(mf, degree), alpha=0.25)

    ax.axvline(out_val, color='red', linestyle='--', linewidth=3,
               label=f"Salida: {out_val:.2f} min")
    ax.set_title('Duración del Riego (Salida)', fontweight='bold')
    ax.set_xlabel('Duración (min)')
    ax.set_ylabel('Grado de Pertenencia')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def plot_multiple_simulations(results_list):
    """
    Genera un gráfico de barras comparando múltiples simulaciones.
    
    Args:
        results_list (list): Lista de diccionarios con resultados
            Cada diccionario debe tener: 'nombre', 'humedad', 'temperatura', 
            'radiacion', 'duracion'
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    nombres = [r['nombre'] for r in results_list]
    duraciones = [r['duracion'] for r in results_list]
    
    # Gráfico de barras de duraciones
    colors = plt.cm.viridis(np.linspace(0, 1, len(nombres)))
    bars = ax1.bar(range(len(nombres)), duraciones, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_xlabel('Caso de Prueba', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Duración del Riego (min)', fontsize=11, fontweight='bold')
    ax1.set_title('Comparación de Duraciones de Riego', fontsize=13, fontweight='bold')
    ax1.set_xticks(range(len(nombres)))
    ax1.set_xticklabels(nombres, rotation=45, ha='right', fontsize=9)
    ax1.grid(True, axis='y', alpha=0.3)
    
    # Añadir valores sobre las barras
    for i, (bar, dur) in enumerate(zip(bars, duraciones)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{dur:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Gráfico de inputs (heatmap simplificado)
    data_matrix = np.array([
        [r['humedad']/100 for r in results_list],
        [r['temperatura']/40 for r in results_list],
        [r['radiacion']/1000 for r in results_list]
    ])
    
    im = ax2.imshow(data_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax2.set_yticks([0, 1, 2])
    ax2.set_yticklabels(['Humedad', 'Temperatura', 'Radiación'], fontsize=10)
    ax2.set_xticks(range(len(nombres)))
    ax2.set_xticklabels(nombres, rotation=45, ha='right', fontsize=9)
    ax2.set_title('Valores de Entrada Normalizados', fontsize=13, fontweight='bold')
    
    # Añadir valores en el heatmap
    for i in range(3):
        for j in range(len(nombres)):
            text = ax2.text(j, i, f'{data_matrix[i, j]:.2f}',
                           ha="center", va="center", color="black", fontsize=8)
    
    cbar = plt.colorbar(im, ax=ax2)
    cbar.set_label('Valor Normalizado', fontsize=10)
    
    plt.tight_layout()
    plt.show()
