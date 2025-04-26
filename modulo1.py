import numpy as np # Importar numpy para operaciones con matrices

# Este módulo implementa un sistema de asignación de tareas utilizando el método de transporte.
class ProblemaTransporte:
    def __init__(self, costos, oferta, demanda):
        self.costos_originales = np.array(costos)
        self.oferta_original = np.array(oferta)
        self.demanda_original = np.array(demanda)
        self.costos = np.array(costos)
        self.oferta = np.array(oferta)
        self.demanda = np.array(demanda)
        self.ficticio = False
        self._balancear()

    def _balancear(self):
        total_oferta = self.oferta.sum()
        total_demanda = self.demanda.sum()
        
        if total_oferta > total_demanda:
            self.demanda = np.append(self.demanda, total_oferta - total_demanda)
            self.costos = np.c_[self.costos, np.zeros(len(self.oferta))]
            self.ficticio = True
        elif total_demanda > total_oferta:
            raise ValueError("La oferta total no puede ser menor que la demanda total")
            
    def matriz_original(self, solucion):
        if self.ficticio:
            return solucion[:, :-1]
        return solucion

# Este módulo implementa el solucionador del problema de transporte utilizando diferentes métodos.
class SolucionadorTransporte:
    def __init__(self, metodo='esquina_noroeste'):
        self.metodo = metodo
        
    def resolver(self, problema):
        if self.metodo == 'esquina_noroeste':
            return self._esquina_noroeste(problema)
        elif self.metodo == 'costo_minimo':
            return self._costo_minimo(problema)
        elif self.metodo == 'vogel':
            return self._vogel(problema)
        else:
            raise ValueError("Método no válido")

    def _esquina_noroeste(self, problema):
        solucion = np.zeros((len(problema.oferta), len(problema.demanda)))
        i, j = 0, 0
        
        while i < len(problema.oferta) and j < len(problema.demanda):
            cantidad = min(problema.oferta[i], problema.demanda[j])
            solucion[i][j] = cantidad
            problema.oferta[i] -= cantidad
            problema.demanda[j] -= cantidad
            
            if problema.oferta[i] == 0: i += 1
            if problema.demanda[j] == 0: j += 1
                
        return problema.matriz_original(solucion)

    def _costo_minimo(self, problema):
        solucion = np.zeros((len(problema.oferta), len(problema.demanda)))
        costos = problema.costos.astype(float).copy()  # Conversión a float
        
        while True:
            i, j = np.unravel_index(costos.argmin(), costos.shape)
            if costos[i, j] == np.inf:
                break
            
            cantidad = min(problema.oferta[i], problema.demanda[j])
            solucion[i][j] = cantidad
            problema.oferta[i] -= cantidad
            problema.demanda[j] -= cantidad
            
            if problema.oferta[i] == 0:
                costos[i, :] = np.inf
            if problema.demanda[j] == 0:
                costos[:, j] = np.inf
                
        return problema.matriz_original(solucion)

    def _vogel(self, problema):
        solucion = np.zeros((len(problema.oferta), len(problema.demanda)))
        costos = problema.costos.astype(float).copy()  # Conversión a float
        
        while True:
            dif_filas = np.diff(np.partition(costos, 1, axis=1)[:, :2], axis=1).flatten()
            dif_cols = np.diff(np.partition(costos, 1, axis=0)[:2, :], axis=0).flatten()
            
            max_dif = max(np.max(dif_filas), np.max(dif_cols))
            
            if max_dif == -np.inf: break
            
            if np.max(dif_filas) >= np.max(dif_cols):
                i = np.argmax(dif_filas)
                j = np.argmin(costos[i])
            else:
                j = np.argmax(dif_cols)
                i = np.argmin(costos[:, j])
                
            cantidad = min(problema.oferta[i], problema.demanda[j])
            solucion[i][j] = cantidad
            problema.oferta[i] -= cantidad
            problema.demanda[j] -= cantidad
            
            if problema.oferta[i] == 0:
                costos[i, :] = np.inf
            if problema.demanda[j] == 0:
                costos[:, j] = np.inf
                
        return problema.matriz_original(solucion)
    
# Este módulo maneja la entrada de datos desde un archivo o desde la consola.
class ManejadorDatos:
    @staticmethod
    def desde_archivo(ruta):
        with open(ruta, 'r') as f:
            lineas = [l.strip() for l in f.readlines() if l.strip()]
            
            try:
                N, M = map(int, lineas[0].split())
                matriz = [list(map(int, l.split())) for l in lineas[1:N+1]]
                S = list(map(int, lineas[N+1].split()))
                D = list(map(int, lineas[N+2].split()))
            except (IndexError, ValueError) as e:
                raise ValueError("Formato de archivo incorrecto") from e
                
            if len(matriz) != N or any(len(fila) != M for fila in matriz):
                raise ValueError("Dimensiones de matriz incorrectas")
                
            return matriz, S, D

    @staticmethod
    def desde_consola():
        def validar_entero(mensaje, min_val=0):
            while True:
                try:
                    valor = int(input(mensaje))
                    if valor < min_val:
                        print(f"Valor debe ser mayor o igual a {min_val}")
                        continue
                    return valor
                except ValueError:
                    print("Ingrese un número válido")
        
        N = validar_entero("Número de programadores: ", 1)
        M = validar_entero("Número de tareas: ", 1)
        
        print("\nIngrese matriz de costos (filas separadas por saltos de línea):")
        matriz = []
        for i in range(N):
            while True:
                fila = input(f"Fila {i+1}: ").split()
                if len(fila) != M:
                    print(f"Debe tener {M} elementos")
                    continue
                try:
                    fila = list(map(int, fila))
                    matriz.append(fila)
                    break
                except ValueError:
                    print("Solo se permiten números enteros")
        
        print("\nIngrese capacidad máxima de tareas por programador:")
        S = [validar_entero(f"Programador {i+1}: ", 0) for i in range(N)]
        
        print("\nIngrese programadores requeridos por tarea:")
        D = [validar_entero(f"Tarea {j+1}: ", 0) for j in range(M)]
        
        if sum(S) < sum(D):
            raise ValueError("La capacidad total no cubre la demanda")
            
        return matriz, S, D

def generar_reporte(solucion, costos):
    reporte = []
    total = 0
    for i in range(solucion.shape[0]):
        for j in range(solucion.shape[1]):
            if solucion[i][j] > 0:
                costo = solucion[i][j] * costos[i][j]
                reporte.append((
                    f"Programador {i+1}",
                    f"Tarea {j+1}",
                    solucion[i][j],
                    costos[i][j],
                    costo
                ))
                total += costo
    return reporte, total

def main():
    print("SISTEMA DE ASIGNACIÓN DE TAREAS CON TRANSPORTE\n")
    
    # Entrada de datos
    try:
        if input("¿Cargar datos desde archivo? (s/n): ").lower() == 's':
            ruta = input("Ruta del archivo: ")
            matriz, S, D = ManejadorDatos.desde_archivo(ruta)
        else:
            matriz, S, D = ManejadorDatos.desde_consola()
    except Exception as e:
        print(f"\nError: {e}")
        return

    # Selección de método
    print("\nMÉTODOS DE SOLUCIÓN:")
    print("1. Esquina Noroeste")
    print("2. Costo Mínimo")
    print("3. Aproximación de Vogel")
    metodo = input("Seleccione método (1-3): ")
    
    metodos = {'1': 'esquina_noroeste', '2': 'costo_minimo', '3': 'vogel'}
    metodo = metodos.get(metodo, 'esquina_noroeste')

    # Resolución del problema
    problema = ProblemaTransporte(matriz, S.copy(), D.copy())
    solucionador = SolucionadorTransporte(metodo)
    
    try:
        solucion = solucionador.resolver(problema)
        reporte, total = generar_reporte(solucion, problema.costos_originales)
    except Exception as e:
        print(f"\nError en optimización: {e}")
        return

    # Reporte de resultados
    print("\nREPORTE DETALLADO:")
    for asignacion in reporte:
        print(f"{asignacion[0]} -> {asignacion[1]}: "
              f"{asignacion[2]} asignaciones × {asignacion[3]} = {asignacion[4]}")
              
    print(f"\nCOSTO TOTAL MÍNIMO: {total}")

if __name__ == "__main__":
    main()

"""
¿Cargar datos desde archivo? (s/n): n
Número de programadores: 3
Número de tareas: 2

Ingrese matriz de costos (filas separadas por saltos de línea):
Fila 1: 10 20
Fila 2: 30 40
Fila 3: 50 60

Ingrese capacidad máxima de tareas por programador:
Programador 1: 2
Programador 2: 1
Programador 3: 1

Ingrese programadores requeridos por tarea:
Tarea 1: 2
Tarea 2: 2

MÉTODOS DE SOLUCIÓN:
1. Esquina Noroeste
2. Costo Mínimo
3. Aproximación de Vogel
Seleccione método (1-3): 2

REPORTE DETALLADO:
Programador 1 -> Tarea 1: 2 asignaciones × 10 = 20
Programador 2 -> Tarea 2: 1 asignaciones × 40 = 40
Programador 3 -> Tarea 2: 1 asignaciones × 60 = 60

"""