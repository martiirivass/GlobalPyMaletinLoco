class Detector:
    def __init__(self,secuenciaADN :list[str],longitudMutacion: int=4) -> None:
        """
        Inicializa el detector de mutaciones con una secuencia de ADN y una longitud de mutación.
        
        Args:
            secuenciaADN (List[str]): Secuencia de ADN representada por lista de strings
            longitudMutacion (int): Longitud de la mutación que se considera válida (por defecto 4).
        """
        self.secuenciaADN=secuenciaADN
        self.longitudMutacion=longitudMutacion
    
    def detectar_mutantes(self) ->bool :
        '''
        Verifica si hay una mutación horizonta, vertical o diagonal
        
        Returns: True si hay mutacion, False en caso contrario.
        '''
        mutacion = (self.existeMutHorizontal() or self.existeMutVertical() or self.existeMutDiagonal())
        
        if mutacion and isinstance(mutacion, tuple):
            fila, columna, letra, direccion = mutacion
            print(f"Mutación detectada en {direccion}: fila {fila + 1}, columna {columna + 1}, letra: {letra}")
            return True
        else:
            print("No se detectaron mutaciones.")
            return False
    
    def existeMutHorizontal(self):
        '''
        Verifica si existe una mutación horizontal en la secuencia de ADN.
        
        Returns:
        Tupla con la fila, columna, letra y dirección si se encuentra una mutación,  o `False` si no se encuentra.
        '''
        for fila in range(len(self.secuenciaADN)):
            secuencia = self.secuenciaADN[fila]
            resultado = self.tieneSecuencia(secuencia)
            if resultado:
                columna, letra = resultado
                return (fila, columna, letra,"horizontal")
        return False

    def existeMutVertical(self):
        '''
        Verifica si existe una mutación vertical en la secuencia de ADN.
        Returns:
        Tupla con la fila, columna, letra y dirección si se encuentra una mutación, 
        o `False` si no se encuentra.
        '''
        longitud = len(self.secuenciaADN)
        for col in range(longitud):
            columna = [self.secuenciaADN[fila][col] for fila in range(longitud)]
            resultado = self.tieneSecuencia(columna)
            if resultado:
                fila, letra = resultado
                return (fila, col, letra,"vertical")
        return False
    
    def existeMutDiagonal(self):
        """
        Verifica si existe una mutación diagonal en la secuencia de ADN (tanto descendente como ascendente).
        
        Returns:
        Tupla con la fila, columna, letra y dirección si se encuentra una mutación, 
        o `False` si no se encuentra
        """
        # Método para comprobar mutación diagonal
        n = len(self.secuenciaADN)
        
        # Diagonales descendentes (de arriba izquierda a abajo derecha)
        for leer in range(n - self.longitudMutacion + 1):
            diagonalDescendenteCol = [self.secuenciaADN[leer + i][i] for i in range(n - leer)]
            diagonalDescendenteFila = [self.secuenciaADN[i][leer + i] for i in range(n - leer)]
            
            resultado_col = self.tieneSecuencia(diagonalDescendenteCol)
            if resultado_col:
                fila, letra = resultado_col
                return (leer + fila, fila, letra,"diagonal descendente")

            resultado_fila = self.tieneSecuencia(diagonalDescendenteFila)
            if resultado_fila:
                fila, letra = resultado_fila
                return (fila, leer + fila, letra,"diagonal descendente")
        
        # Diagonales ascendentes (de abajo izquierda a arriba derecha)
        for leer in range(n - self.longitudMutacion + 1):
            diagonalAscendenteCol = [self.secuenciaADN[n - 1 - leer - i][i] for i in range(n - leer)]
            diagonalAscendenteFila = [self.secuenciaADN[n - 1 - i][leer + i] for i in range(n - leer)]
            
            resultado_col = self.tieneSecuencia(diagonalAscendenteCol)
            if resultado_col:
                fila, letra = resultado_col
                return (n - 1 - leer - fila, fila, letra,"diagonal ascendente")

            resultado_fila = self.tieneSecuencia(diagonalAscendenteFila)
            if resultado_fila:
                fila, letra = resultado_fila
                return (n - 1 - fila, leer + fila, letra,"diagonal ascendente")
        
        return False

    def tieneSecuencia(self, secuenciaADN:list[str]):
        ''' 
        Verifica si una secuencia contiene caracteres consecutivos iguales hasta la longitud de mutación.
        
        Args:
        secuenciaADN (List[str]): La secuencia de ADN a verificar.
        
        Returns:
        Tupla con la posición inicial y el carácter de la mutación, 
        o `False` si no se encuentra ninguna mutación'''
        contador = 1
        for i in range(1, len(secuenciaADN)):
            if secuenciaADN[i] == secuenciaADN[i - 1]:
                contador += 1
                if contador == self.longitudMutacion:
                    return (i - self.longitudMutacion + 1, secuenciaADN[i])  # Retorna posición de inicio y letra
            else:
                contador = 1
        return False

class Mutador:
    def __init__(self, base_nitrogenada, tipoMutacion, secuenciaADN):
        self.base_nitrogenada = base_nitrogenada  # Especifica cuál de las bases se repetirá 4 veces
        self.tipoMutacion = tipoMutacion  # Dirección de la mutación
        self.secuenciaADN = secuenciaADN  # La lista de strings que forman el ADN
    
    def crear_mutante(self):
        pass  # Método vacío, sin retorno de valor


class Radiacion(Mutador):  # Clase hija para mutar en horizontal o vertical
    def __init__(self, base_nitrogenada, tipoMutacion, secuenciaADN):
        super().__init__(base_nitrogenada, tipoMutacion, secuenciaADN)
      
    def crear_mutante(self, base_nitrogenada, posicion_inicial, orientacion_de_la_mutacion):
        fila, columna = posicion_inicial
        try:
            # Comprobar si la posición inicial está dentro de los límites
            if fila < 0 or fila >= len(self.secuenciaADN) or columna < 0 or columna >= len(self.secuenciaADN[0]):
                raise IndexError("La posición inicial está fuera de los límites de la matriz.")

            # Realizar la mutación según la orientación
            if orientacion_de_la_mutacion.upper() == 'H':
                # Mutación horizontal: cambiar la base en la posición indicada
                for i in range(columna, min(columna + 4, len(self.secuenciaADN[fila]))):  # 4 es el número de posiciones a mutar
                    # Mutamos en la fila, comenzando desde la columna especificada, reemplazando con base_nitrogenada
                    self.secuenciaADN[fila][i] = base_nitrogenada
                
            elif orientacion_de_la_mutacion.upper() == 'V':
                # Mutación vertical: aplicar la base nitrogenada en la columna de cada fila
                if fila + 3 < len(self.secuenciaADN):  # Verifica que haya espacio suficiente para la mutación
                    for i in range(fila, min(fila + 4, len(self.secuenciaADN))):
                        # Asegurarse de que la columna no se salga de los límites
                        if columna < len(self.secuenciaADN[i]):
                            self.secuenciaADN[i][columna] = base_nitrogenada
                        else:
                            raise IndexError("La mutación vertical se sale de los límites de la matriz.")
                else:
                    raise IndexError("La mutación vertical no cabe en la matriz desde la posición inicial.")
            else:
                raise ValueError("La orientación debe ser 'H' (horizontal) o 'V' (vertical).")
        
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")

        # Imprimir la secuencia de ADN resultante
        for fila in self.secuenciaADN:
            print(fila)  # Imprimir cada fila (como lista de caracteres)

        return self.secuenciaADN  # Retornar la matriz modificada

    
class Virus(Mutador):  #Clase hija para mutar en diagonal
    def __init__(self, base_nitrogenada, tipoMutacion, secuenciaADN):
        super().__init__(base_nitrogenada, tipoMutacion, secuenciaADN)
        
        
        
    def crear_mutante(self,base_nitrogenada,posicionInicial,orientacionMutacion):    
        fila, columna = posicionInicial
        n = len(self.secuenciaADN)

        try:
            #Comprobar que la posiciona inicial este dentro de la matriz
            if not (0 <= fila < n and 0 <= columna < n):
                raise IndexError("La posición inicial está fuera de los límites de la matriz.")

            # Insertar mutación en diagonal descendente
            if fila + 3 < n and columna + 3 < n:
                for i in range(4):
                    fila_modificada = ''.join(self.secuenciaADN[fila + i])
                    fila_modificada = (
                        fila_modificada[:columna + i] +
                        base_nitrogenada +
                        fila_modificada[columna + i + 1:]
                    )
                    self.secuenciaADN[fila + i] = list(fila_modificada)
    
            else:
                # Si no cabe la diagonal descendente, intentamos la ascendente
                if fila - 3 >= 0 and columna + 3 < n:
                    for i in range(4):
                        fila_modificada = ''.join(self.secuenciaADN[fila - i])
                        fila_modificada = (
                            fila_modificada[:columna + i] +
                            base_nitrogenada +
                            fila_modificada[columna + i + 1:]
                        )
                        self.secuenciaADN[fila - i] = list(fila_modificada)
                else:
                    raise IndexError("La mutación diagonal no cabe en la posición inicial.")

        except (ValueError, IndexError) as e:
            print(f"Error al crear mutante: {e}")
        
        for fila in self.secuenciaADN:
            print(fila)                     # Imprimir cada fila

        return self.secuenciaADN  # Retornar la matriz modificada
    
import random #Para la clase sanador 
class Sanador:
    def __init__(self, secuenciaADN):
        self.secuenciaADN = secuenciaADN

    # Función para sanar el ADN, cambiando las secuencias de más de 4 bases repetidas
    def sanar_mutantes(self):
        # Comprobar todas las filas, columnas y diagonales
        for i in range(6):
            for j in range(6):
                # Si hay 4 o más letras iguales consecutivas en alguna dirección, se modifica
                if self.comprobarSecuencia(i, j):
                    # Realizar la modificación en el ADN
                    self.modificarADN(i, j)

        # Mostrar el ADN después de sanarlo
        print("El ADN ha sido sanado:")
        self.mostrarADN()

    def comprobarSecuencia(self, fila, columna):
        # Comprobar si hay 4 o más letras iguales consecutivas en fila, columna o diagonal
        if self.contarConsecutivos(fila, columna, 'H') >= 4 or self.contarConsecutivos(fila, columna, 'V') >= 4 or self.contarConsecutivos(fila, columna, 'D') >= 4:
            return True
        return False

    def contarConsecutivos(self, fila, columna, direccion):
        """
        Cuenta cuántos caracteres consecutivos iguales hay en una fila, columna o diagonal
        según la dirección indicada ('H', 'V', 'D' para diagonal).
        """
        base = self.secuenciaADN[fila][columna]
        count = 0

        if direccion == 'H':  # Horizontal
            for c in range(columna, 6):
                if self.secuenciaADN[fila][c] == base:
                    count += 1
                else:
                    break
        elif direccion == 'V':  # Vertical
            for r in range(fila, 6):
                if self.secuenciaADN[r][columna] == base:
                    count += 1
                else:
                    break
        elif direccion == 'D':  # Diagonal
            r, c = fila, columna
            while r < 6 and c < 6 and self.secuenciaADN[r][c] == base:
                count += 1
                r += 1
                c += 1
        return count

    def modificarADN(self, fila, columna):
        """
        Cambiar el valor del ADN para que no haya más de 4 bases consecutivas iguales.
        Se elige un cambio aleatorio a una base diferente.
        """
        # Obtener la base actual
        baseActual = self.secuenciaADN[fila][columna]

        # Definir un conjunto de bases posibles
        bases = ['A', 'T', 'C', 'G']
        bases.remove(baseActual)  # Eliminar la base actual para evitar que se repita

        # Elegir una base diferente al azar
        nuevaBase = random.choice(bases)

        # Modificar el valor de la base en esa posición
        self.secuenciaADN[fila][columna] = nuevaBase

    def mostrarADN(self):
        """Función para mostrar el ADN"""
        for fila in self.secuenciaADN:
            print(fila)
