# main.py

# Este script permite al usuario seleccionar entre dos módulos para ejecutar y probar su funcionalidad.
# Los módulos son 'modulo1' y 'modulo2', cada uno con su propia función main().
def ejecutar_modulo1():
    import modulo1
    modulo1.main()

def ejecutar_modulo2():
    import modulo2
    modulo2.main()

# Función principal que controla el flujo del programa
def main():
    
    
    while True:
        print("\n¿Qué módulo desea probar?")
        print("1. Módulo 1")
        print("2. Módulo 2")
        print("3. Cerrar programa")

        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == '1':
            ejecutar_modulo1()
            modulo_actual = 'modulo1'
        elif opcion == '2':
            ejecutar_modulo2()
            modulo_actual = 'modulo2'
        elif opcion == '3':
            print("Cerrando programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione 1, 2 o 3.")
            continue

        if modulo_actual:
            while True:
                print("\n¿Qué desea hacer ahora?")
                print("1. Probar el mismo módulo nuevamente")
                print("2. Probar otro módulo")
                print("3. Cerrar programa")

                accion = input("Seleccione una opción (1-3): ").strip()

                if accion == '1':
                    print(f"\nRe-ejecutando el módulo '{modulo_actual}'...")
                    if modulo_actual == 'modulo1':
                        ejecutar_modulo1()
                    elif modulo_actual == 'modulo2':
                        ejecutar_modulo2()
                elif accion == '2':
                    break  # Volver a la selección de módulo
                elif accion == '3':
                    print("Cerrando programa...")
                    return  # Salir del programa principal
                else:
                    print("Opción inválida. Por favor, seleccione 1, 2 o 3.")

if __name__ == "__main__":
    main()