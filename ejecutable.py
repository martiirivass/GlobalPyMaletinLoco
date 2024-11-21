'''FUNCION PARA SOLICITAR EL ADN'''
def solicitarMatriz():
    secuenciaADN=[] #matrizADN como lista de strings
    print("Ingrese una matriz de ADN 6x6, el ADN solo contendrá (T),(C),(G),(A), en caso contrario no será válida.")
    
    for i in range(6):
        while True:
            fila=input(f"Ingrese la fila {i+1}: ").strip().upper()  #Strip para eliminar espacios en blancos y upper para que cualquier dato esté en Mayus.
            
            if len(fila) ==6 and all(caracter in "ATCG" for caracter in fila):  #Verificar que la fila no sea mayor a 6 y que los caracteres sean los correctos
                secuenciaADN.append(list(fila)) #Si se cumple agrega el string a la lista
                break
            else:
                print("Error, areguresé de que la fila contenga 6 caracteres de (T),(C),(G) y (A)")
    return secuenciaADN #Retorna la lista con los 6 strings que le asignamos en el for


'''FUNCION PARA EL MENÚ'''
def opcionMenu():
    print("\nMenú Principal")
    print("1.Detectar Mutantes\n2.Mutar el ADN\n3.Sanar el ADN\n4.Salir")
    opcion={
        "1":"Detectar Mutantes",
        "2":"Mutar el ADN",
        "3":"Sanar el ADN",
        "4":"Salir",
    }



import random
from clases import Detector,Sanador,Mutador,Radiacion,Virus

# Solicitar la matriz de ADN y guardar el ADN original
secuenciaADN = solicitarMatriz()

# Instanciar la clase Sanador con la secuencia de ADN
sanador = Sanador(secuenciaADN)


originalADN = [fila[:] for fila in secuenciaADN]  # Guardar una copia original

# Mostrar la matriz de ADN ingresada
for fila in secuenciaADN:
    print(fila)

def sanarADN():
    global secuenciaADN
    secuenciaADN = [fila[:] for fila in originalADN]  # Restaurar el ADN original
    print("El ADN ha sido restaurado a su estado original.")
    
while True:
    opcionMenu()  #Llamamos a la función del Menú
    opcion=int(input("Elija una opcion\n")) #Input para elegir una opcion

    if opcion==1: #Detectar mutantes
        detector=Detector(secuenciaADN)
        if detector.detectar_mutantes():
            print("")
            pass
    
    elif opcion==2: #Mutar el ADN
        print("\nMUTACIÓN DE ADN")
        base_nitrogenada=input("¿Con que base nitrogenada quiere mutar el ADN? (T),(C),(G),(A)").strip().upper()
        tipo_mutacion=input("Quiere mutar el ADN en:\n(D)diagonal\n(H)horizontal o (V)vertical").strip().upper()
        if (base_nitrogenada in ["T", "C", "G", "A"]) and (tipo_mutacion in ["D", "H", "V"]):
            mutadores = {
            'D': Virus(base_nitrogenada, tipo_mutacion, secuenciaADN),
            'H': Radiacion(base_nitrogenada, tipo_mutacion, secuenciaADN),
            'V': Radiacion(base_nitrogenada, tipo_mutacion, secuenciaADN)
            }

            # Verificar si el tipo de mutación es válido y llamar a la clase correspondiente
            mutador = mutadores.get(tipo_mutacion.upper())
            if mutador:
            # Solicitar la posición inicial y la orientación para mutar el ADN
                fila = int(input("Ingrese la fila de la posición inicial: (0 a 5) "))
                columna = int(input("Ingrese la columna de la posición inicial: (0 a 5)"))
                posicion_inicial = (fila, columna)
            
                # Si el tipo es 'D', solo se necesita la orientación
                if tipo_mutacion.upper() == 'D':
                    secuenciaADN = mutador.crear_mutante(base_nitrogenada, posicion_inicial, tipo_mutacion)
                else:
                    orientacion = input("¿Quiere mutar horizontal (H) o vertical (V)? ").strip().upper()
                    secuenciaADN = mutador.crear_mutante(base_nitrogenada, posicion_inicial, orientacion)
                print("Mutación completada.")
            else:
                print("Tipo de mutación inválido.")
        else:
            print("Base nitrogenada o tipo de mutación inválido.")
            
    elif opcion == 3:  # Sanar el ADN
        sanador.sanar_mutantes()  # Llamar al método sanarADN() de la clase Sanador
        pass
    elif opcion==4:
        print("Saliendo...")
        break
    else:
        print("Caracter inválido, intente de vuelta")
        pass
