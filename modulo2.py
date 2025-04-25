import numpy as np
from scipy.optimize import linear_sum_assignment

class Servidor:
    def __init__(self, id, capacidad):
        """
        Inicializa un nuevo servidor.
        :param id: Identificador único del servidor.
        :param capacidad: Capacidad total de procesamiento del servidor.
        """
        self.id = id
        self.capacidad = capacidad
        self.carga_actual = 0
        self.solicitudes_asignadas = []

    def asignar_solicitud(self, solicitud):
        """
        Asigna una solicitud al servidor si hay suficiente capacidad.
        :param solicitud: Objeto Solicitud a asignar.
        :return: True si la solicitud fue asignada, False en caso contrario.
        """
        if self.carga_actual + solicitud.requerimiento <= self.capacidad:
            self.solicitudes_asignadas.append(solicitud)
            self.carga_actual += solicitud.requerimiento
            return True
        return False

    def __str__(self):
        """
        Representación en cadena del servidor.
        :return: Cadena con el ID, carga actual y solicitudes asignadas.
        """
        return f"Servidor {self.id}: Carga {self.carga_actual}/{self.capacidad}, Solicitudes: {[s.id for s in self.solicitudes_asignadas]}"

class Solicitud:
    def __init__(self, id, requerimiento, prioridad):
        """
        Inicializa una nueva solicitud.
        :param id: Identificador único de la solicitud.
        :param requerimiento: Cantidad de recursos que requiere la solicitud.
        :param prioridad: Prioridad de la solicitud (un número mayor indica mayor urgencia).
        """
        self.id = id
        self.requerimiento = requerimiento
        self.prioridad = prioridad

    def __str__(self):
        """
        Representación en cadena de la solicitud.
        :return: Cadena con el ID, requerimiento y prioridad.
        """
        return f"Solicitud {self.id}: Req {self.requerimiento}, Prio {self.prioridad}"

class AsignadorSolicitudes:
    def __init__(self, servidores, solicitudes, matriz_costos):
        """
        Inicializa el asignador de solicitudes.
        :param servidores: Lista de objetos Servidor disponibles.
        :param solicitudes: Lista de objetos Solicitud a asignar.
        :param matriz_costos: Matriz numpy de costos donde matriz_costos[i][j]
                              es el costo de asignar la solicitud j al servidor i.
        :raises ValueError: Si las dimensiones de la matriz de costos no coinciden
                            con el número de servidores y solicitudes.
        """
        if matriz_costos.shape != (len(servidores), len(solicitudes)):
            raise ValueError(
                f"Las dimensiones de la matriz de costos ({matriz_costos.shape}) "
                f"deben coincidir con el número de servidores ({len(servidores)}) "
                f"y el número de solicitudes ({len(solicitudes)})."
            )
        self.servidores = servidores
        self.solicitudes = solicitudes
        self.matriz_costos = matriz_costos

    def optimizar_asignacion(self):
        """
        Optimiza la asignación de solicitudes a servidores utilizando el Método Húngaro,
        considerando la prioridad de las solicitudes.
        :return: Una lista de tuplas (servidor_id, solicitud_id, costo) que representan
                 la asignación óptima.
        """
        # Se extraen las prioridades de las solicitudes para ajustar la matriz de costos.
        # Las prioridades más altas disminuyen el costo efectivo, favoreciendo su asignación.
        prioridades = np.array([s.prioridad for s in self.solicitudes])
        matriz_ajustada = self.matriz_costos - prioridades * 1000  # Un factor grande para priorizar

        # Aplica el Método Húngaro para obtener los índices de filas y columnas
        # que corresponden a la asignación de costo mínimo.
        fila_ind, col_ind = linear_sum_assignment(matriz_ajustada)
        asignaciones = []

        # Itera sobre las asignaciones encontradas y asigna las solicitudes a los servidores,
        # verificando la capacidad del servidor.
        for f, c in zip(fila_ind, col_ind):
            servidor = self.servidores[f]
            solicitud = self.solicitudes[c]
            if servidor.asignar_solicitud(solicitud):
                asignaciones.append((servidor.id, solicitud.id, self.matriz_costos[f, c]))
            else:
                print(f"Advertencia: No se pudo asignar la Solicitud {solicitud.id} al Servidor {servidor.id} por falta de capacidad.")

        return asignaciones

    def reporte(self, asignaciones):
        """
        Genera un reporte de la asignación óptima, incluyendo las asignaciones,
        la carga de trabajo por servidor y el tiempo total de procesamiento.
        :param asignaciones: Lista de tuplas (servidor_id, solicitud_id, costo)
                             resultantes de la optimización.
        """
        print("\n" + "="*50)
        print("Reporte de Asignación Óptima".center(50))
        print("="*50)
        print("\nAsignaciones (Servidor -> Solicitud | Tiempo):")
        for s_id, r_id, costo in asignaciones:
            print(f"  ▸ Servidor {s_id} → Solicitud {r_id} | Tiempo: {costo}")
        print("\n" + "-"*50)
        print("Carga de Trabajo por Servidor:")
        for servidor in self.servidores:
            print(f"  {servidor}")
        costo_total = sum(c for _, _, c in asignaciones)
        print("\n" + "-"*50)
        print(f"Tiempo Total de Procesamiento: {costo_total}")
        print("="*50 + "\n")

# ------------------ Módulo de Entrada de Datos ------------------
def ingresar_entero(mensaje, min_val=1):
    """
    Solicita al usuario un número entero y lo valida.
    :param mensaje: Mensaje a mostrar al usuario.
    :param min_val: Valor mínimo aceptado (por defecto 1).
    :return: El número entero ingresado por el usuario.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= min_val:
                return valor
            print(f"Error: Debe ser ≥ {min_val}")
        except ValueError:
            print("Error: Ingrese un número entero válido")

def ingresar_servidores():
    """
    Permite al usuario ingresar la información de los servidores.
    :return: Una lista de objetos Servidor.
    """
    num_servidores = ingresar_entero("Número de servidores: ")
    return [Servidor(i, ingresar_entero(f"Capacidad del servidor {i}: ")) for i in range(num_servidores)]

def ingresar_solicitudes():
    """
    Permite al usuario ingresar la información de las solicitudes.
    :return: Una lista de objetos Solicitud.
    """
    num_solicitudes = ingresar_entero("Número de solicitudes: ")
    return [
        Solicitud(
            i,
            ingresar_entero(f"Requerimiento de la solicitud {i}: "),
            ingresar_entero(f"Prioridad (1-5) de la solicitud {i}: ", 1)
        ) for i in range(num_solicitudes)
    ]

def ingresar_matriz_costos(servidores, solicitudes):
    """
    Permite al usuario ingresar la matriz de costos de asignación.
    :param servidores: Lista de objetos Servidor.
    :param solicitudes: Lista de objetos Solicitud.
    :return: Una matriz numpy de costos.
    """
    num_servidores = len(servidores)
    num_solicitudes = len(solicitudes)
    print("\nIngrese la matriz de costos (tiempos de procesamiento):")
    matriz_costos = np.zeros((num_servidores, num_solicitudes))
    for i in range(num_servidores):
        for j in range(num_solicitudes):
            matriz_costos[i, j] = ingresar_entero(f"Servidor {servidores[i].id} → Solicitud {solicitudes[j].id}: ")
    return matriz_costos

def cargar_datos_prueba():
    """
    Proporciona datos de prueba para ejecutar el programa sin entrada manual.
    :return: Una tupla con la lista de servidores, la lista de solicitudes y la matriz de costos.
    """
    servidores = [Servidor(0, 8), Servidor(1, 6), Servidor(2, 7)]
    solicitudes = [
        Solicitud(0, 3, 2),
        Solicitud(1, 2, 3),
        Solicitud(2, 4, 1),
        Solicitud(3, 2, 2)
    ]
    matriz_costos = np.array([
        [12, 7, 9, 7],
        [8, 9, 6, 6],
        [7, 17, 12, 14]
    ])
    return servidores, solicitudes, matriz_costos

def main():
    """
    Función principal del programa. Permite al usuario elegir entre usar datos de prueba
    o ingresar los datos manualmente y luego realiza la asignación óptima.
    """
    print("""
    ====================================
        OPTIMIZADOR DE ASIGNACIÓN CLOUD
    ====================================
    1. Usar datos de prueba
    2. Ingresar datos manualmente
    """)

    opcion = input("Seleccione una opción (1/2): ").strip()

    if opcion == '1':
        servidores, solicitudes, matriz_costos = cargar_datos_prueba()
    elif opcion == '2':
        print("\n" + "-"*40)
        print("INGRESO DE DATOS".center(40))
        print("-"*40)
        servidores = ingresar_servidores()
        solicitudes = ingresar_solicitudes()
        matriz_costos = ingresar_matriz_costos(servidores, solicitudes)
    else:
        print("Opción inválida. Saliendo...")
        return

    try:
        asignador = AsignadorSolicitudes(servidores, solicitudes, matriz_costos)
        asignaciones = asignador.optimizar_asignacion()
        asignador.reporte(asignaciones)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()