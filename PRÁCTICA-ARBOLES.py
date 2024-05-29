class Nodo:
    def __init__(self, valor, prioridad):
        self.valor = valor
        self.prioridad = prioridad
        self.izquierdo = None
        self.derecho = None
        self.padre = None

class MinHeap:
    def __init__(self):
        self.raiz = None
        self.tamaño = 0

    def insertar(self, valor, prioridad):
        nuevo_nodo = Nodo(valor, prioridad)
        if not self.raiz:
            self.raiz = nuevo_nodo
        else:
            self._insertar_nodo(self.raiz, nuevo_nodo)
        self.tamaño += 1

    def _insertar_nodo(self, raiz, nuevo_nodo):
        cola = [raiz]
        while cola:
            actual = cola.pop(0)
            if not actual.izquierdo:
                actual.izquierdo = nuevo_nodo
                nuevo_nodo.padre = actual
                self.subir(nuevo_nodo)
                return
            elif not actual.derecho:
                actual.derecho = nuevo_nodo
                nuevo_nodo.padre = actual
                self.subir(nuevo_nodo)
                return
            else:
                cola.append(actual.izquierdo)
                cola.append(actual.derecho)

    def extraer_min(self):
        if not self.raiz:
            return None

        valor_min = self.raiz.valor
        if self.tamaño == 1:
            self.raiz = None
        else:
            ultimo_nodo = self.obtener_ultimo_nodo()
            self.reemplazar_raiz(ultimo_nodo)
            self.bajar(self.raiz)

        self.tamaño -= 1
        return valor_min

    def reemplazar_raiz(self, nodo):
        if nodo.padre.derecho == nodo:
            nodo.padre.derecho = None
        else:
            nodo.padre.izquierdo = None
        nodo.izquierdo = self.raiz.izquierdo
        nodo.derecho = self.raiz.derecho
        if nodo.izquierdo:
            nodo.izquierdo.padre = nodo
        if nodo.derecho:
            nodo.derecho.padre = nodo
        self.raiz = nodo

    def obtener_ultimo_nodo(self):
        cola = [self.raiz]
        ultimo_nodo = None
        while cola:
            ultimo_nodo = cola.pop(0)
            if ultimo_nodo.izquierdo:
                cola.append(ultimo_nodo.izquierdo)
            if ultimo_nodo.derecho:
                cola.append(ultimo_nodo.derecho)
        return ultimo_nodo

    def subir(self, nodo):
        while nodo.padre and nodo.padre.prioridad > nodo.prioridad:
            nodo.valor, nodo.prioridad, nodo.padre.valor, nodo.padre.prioridad = nodo.padre.valor, nodo.padre.prioridad, nodo.valor, nodo.prioridad
            nodo = nodo.padre

    def bajar(self, nodo):
        while nodo.izquierdo or nodo.derecho:
            menor = nodo
            if nodo.izquierdo and nodo.izquierdo.prioridad < menor.prioridad:
                menor = nodo.izquierdo
            if nodo.derecho and nodo.derecho.prioridad < menor.prioridad:
                menor = nodo.derecho

            if menor != nodo:
                nodo.valor, nodo.prioridad, menor.valor, menor.prioridad = menor.valor, menor.prioridad, nodo.valor, nodo.prioridad
                nodo = menor
            else:
                break

class ColaPrioridad:
    def __init__(self):
        self.min_heap = MinHeap()

    def encolar(self, valor, prioridad):
        self.min_heap.insertar(valor, prioridad)

    def desencolar(self):
        return self.min_heap.extraer_min()

    def consultar_proximo(self):
        if not self.min_heap.raiz:
            return None
        return self.min_heap.raiz.valor

    def mostrar_todos(self):
        if not self.min_heap.raiz:
            return []
        return self.mostrar_nodos([self.min_heap.raiz])

    def mostrar_nodos(self, nodos):
        resultado = []
        while nodos:
            actual = nodos.pop(0)
            resultado.append(actual.valor)
            if actual.izquierdo:
                nodos.append(actual.izquierdo)
            if actual.derecho:
                nodos.append(actual.derecho)
        return resultado

    def mostrar_por_prioridad(self, prioridad):
        if not self.min_heap.raiz:
            return []
        return self.mostrar_nodos_por_prioridad([self.min_heap.raiz], prioridad)

    def mostrar_nodos_por_prioridad(self, nodos, prioridad):
        resultado = []
        while nodos:
            actual = nodos.pop(0)
            if actual.prioridad == prioridad:
                resultado.append(actual.valor)
            if actual.izquierdo:
                nodos.append(actual.izquierdo)
            if actual.derecho:
                nodos.append(actual.derecho)
        return resultado

    def eliminar_paciente(self, identificador):
        if not self.min_heap.raiz:
            return False
        return self.eliminar_nodo(self.min_heap.raiz, identificador)

    def eliminar_nodo(self, nodo, identificador):
        if not nodo:
            return False

        if nodo.valor['id'] == identificador:
            if self.min_heap.tamaño == 1:
                self.min_heap.raiz = None
            else:
                ultimo_nodo = self.min_heap.obtener_ultimo_nodo()
                self.min_heap.reemplazar_raiz(ultimo_nodo)
                self.min_heap.bajar(self.min_heap.raiz)
            self.min_heap.tamaño -= 1
            return True

        if self.eliminar_nodo(nodo.izquierdo, identificador) or self.eliminar_nodo(nodo.derecho, identificador):
            return True

        return False

class Paciente:
    def __init__(self, cedula, nombre, edad, genero, triaje):
        self.cedula = cedula
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.triaje = triaje

    def a_dict(self):
        return {'cedula': self.cedula, 'nombre': self.nombre, 'edad': self.edad, 'genero': self.genero, 'triaje': self.triaje}

def menu_principal():
    cola_prioridad = ColaPrioridad()
    while True:
        print("1. Registrar paciente")
        print("2. Consultar paciente próximo a atención")
        print("3. Atender siguiente paciente")
        print("4. Consultar pacientes en espera")
        print("5. Consultar pacientes en espera por triaje")
        print("6. Eliminar paciente")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            cedula = input("Ingrese la cédula del paciente: ")
            nombre = input("Ingrese nombre del paciente: ")
            edad = int(input("Ingrese edad del paciente: "))
            genero = input("Ingrese género del paciente: ")
            triaje = int(input("Ingrese triaje del paciente (1-5): "))
            paciente = Paciente(cedula, nombre, edad, genero, triaje)
            cola_prioridad.encolar(paciente.a_dict(), triaje)
            print("Paciente registrado exitosamente.")
        elif opcion == '2':
            proximo_paciente = cola_prioridad.consultar_proximo()
            if proximo_paciente:
                print("Próximo paciente a atender:", proximo_paciente)
            else:
                print("No hay pacientes en espera.")
        elif opcion == '3':
            paciente_atendido = cola_prioridad.desencolar()
            if paciente_atendido:
                print("Atendiendo paciente:", paciente_atendido)
            else:
                print("No hay pacientes en espera.")
        elif opcion == '4':
            pacientes = cola_prioridad.mostrar_todos()
            if pacientes:
                print("Pacientes en espera:")
                for paciente in pacientes:
                    print(paciente)
            else:
                print("No hay pacientes en espera.")
        elif opcion == '5':
            triaje = int(input("Ingrese triaje para consultar (1-5): "))
            pacientes = cola_prioridad.mostrar_por_prioridad(triaje)
            if pacientes:
                print(f"Pacientes en espera con triaje {triaje}:")
                for paciente in pacientes:
                    print(paciente)
            else:
                print(f"No hay pacientes en espera con triaje {triaje}.")
        elif opcion == '6':
            cedula = input("Ingrese la cédula del paciente a eliminar: ")
            if cola_prioridad.eliminar_paciente(cedula):
                print("Paciente eliminado exitosamente.")
            else:
                print("Paciente no encontrado.")
        elif opcion == '7':
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu_principal()
