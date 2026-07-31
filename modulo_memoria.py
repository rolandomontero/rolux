# modulo_memoria.py

import json
import os

# --- Configuración Inicial ---
# Define la ruta al archivo de memoria. 
# Se puede pasar como argumento a las funciones o usar una variable global.
ARCHIVO_MEMORIA = "memoria_curricular_1ero_medio.json"

# --- Función para Cargar la Memoria ---
def cargar_memoria(ruta_archivo=ARCHIVO_MEMORIA):
    """
    Carga el archivo de memoria curricular (JSON) y lo devuelve como un diccionario.

    Args:
        ruta_archivo (str): Ruta al archivo JSON de memoria. 
                            Por defecto, usa 'memoria_curricular_1ero_medio.json'.

    Returns:
        dict: Contenido del archivo JSON como diccionario.
        
    Raises:
        FileNotFoundError: Si el archivo no se encuentra en la ruta especificada.
        json.JSONDecodeError: Si el archivo no tiene un formato JSON válido.
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            memoria = json.load(archivo)
            print(f"[INFO MÓDULO] Memoria cargada exitosamente desde '{ruta_archivo}'.")
            return memoria
    except FileNotFoundError:
        print(f"[ERROR MÓDULO] Archivo de memoria no encontrado en: {ruta_archivo}")
        print("Asegúrese de que el archivo exista y la ruta sea correcta.")
        raise
    except json.JSONDecodeError:
        print(f"[ERROR MÓDULO] El archivo '{ruta_archivo}' no tiene un formato JSON válido.")
        raise

# --- Función para Buscar en la Memoria ---
def consultar_memoria_curricular(eje_tematico, numero_unidad, oa_numero=None, archivo_memoria=ARCHIVO_MEMORIA):
    """
    Función principal para que el agente consulte la memoria.
    Busca la información de un Eje y Unidad específicos, y opcionalmente de un OA.

    Args:
        eje_tematico (str): El eje del currículum ('Biologia', 'Fisica', 'Quimica').
        numero_unidad (str or int): Número de la unidad (ej. '1', '2').
        oa_numero (str, optional): Número del Objetivo de Aprendizaje (ej. 'OA4', 'OA17'). 
                                    Si es None, devuelve toda la información de la unidad.
        archivo_memoria (str): Ruta al archivo de memoria.

    Returns:
        dict or str: 
            - Si se encuentra la información, devuelve un diccionario con la sección 
              de la memoria solicitada (unidad completa o un OA específico).
            - Si no se encuentra, devuelve un mensaje de error como string.
            - Si ocurre un error al cargar, propaga la excepción.
    """
    try:
        # 1. Cargar toda la memoria
        memoria = cargar_memoria(archivo_memoria)
        
        # 2. Navegar por los ejes y unidades (estructura basada en el JSON de ejemplo)
        # Primero, buscamos el eje principal
        if eje_tematico not in memoria:
            mensaje = f"[ERROR] Eje '{eje_tematico}' no encontrado en la memoria. "
            mensaje += f"Los ejes disponibles son: {list(memoria.keys())}"
            return mensaje
            
        # Luego, buscamos la unidad dentro del eje
        eje = memoria[eje_tematico]
        # El número de unidad se convierte a string para consistencia (ej. '1')
        unidad_str = str(numero_unidad)
        if unidad_str not in eje:
            mensaje = f"[ERROR] Unidad '{unidad_str}' no encontrada para el eje '{eje_tematico}'. "
            mensaje += f"Las unidades disponibles son: {list(eje.keys())}"
            return mensaje
            
        unidad = eje[unidad_str]
        
        # 3. Si se solicitó un OA específico, buscarlo dentro de la unidad
        if oa_numero:
            if 'objetivos' in unidad:
                for objetivo in unidad['objetivos']:
                    # Busca por el número del OA (ej. 'OA 4', 'OA 17')
                    if objetivo.get('numero') == oa_numero or oa_numero in objetivo.get('numero', ''):
                        return objetivo
                # Si no se encuentra el OA
                mensaje = f"[ERROR] OA '{oa_numero}' no encontrado en la Unidad {unidad_str} de {eje_tematico}."
                return mensaje
            else:
                mensaje = f"[ERROR] La estructura de la Unidad {unidad_str} no contiene 'objetivos'."
                return mensaje
        
        # 4. Si no se pidió un OA específico, devolver toda la información de la unidad
        return unidad

    except (FileNotFoundError, json.JSONDecodeError) as e:
        # Relanzar la excepción para que el agente la maneje
        raise e

# --- Ejemplo de uso y prueba del módulo ---
if __name__ == '__main__':
    print("--- Prueba del Módulo de Memoria ---")
    
    # Ejemplo: Consultar toda la Unidad 1 de Biología
    print("\n1. Consultando Unidad 1 de Biología:")
    info_unidad_1 = consultar_memoria_curricular('Biologia', '1')
    print(json.dumps(info_unidad_1, indent=4, ensure_ascii=False))  # Imprimir en formato JSON bonito
    
    # Ejemplo: Consultar el OA 4 de Biología, Unidad 2
    print("\n2. Consultando OA4 de Biología, Unidad 2:")
    info_oa_4 = consultar_memoria_curricular('Biologia', '2', 'OA4')
    print(json.dumps(info_oa_4, indent=4, ensure_ascii=False))

    # Ejemplo: Error de búsqueda
    print("\n3. Probando búsqueda con error (Eje inexistente):")
    error_eje = consultar_memoria_curricular('Astronomia', '1')
    print(error_eje)

    print("\n--- Fin de la prueba ---")