
"""
Implementación de estructuras de datos clásicas en Python:

    - Stack  (LIFO  - Last In, First Out)
    - Queue  (FIFO  - First In, First Out)
    - OrderedTable / Hash / Dictionary (que preserva el orden de inserción)

Se apoya en librerías estándar de Python:
    - collections.deque -> estructura doblemente enlazada muy eficiente
                           para operaciones en ambos extremos (O(1)).
    - collections.OrderedDict -> diccionario que recuerda el orden de
                           inserción y permite reordenar sus elementos.

Autor: OreateAI
"""

from collections import deque, OrderedDict
from typing import Any, Iterator, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Excepciones propias
# ---------------------------------------------------------------------------
class EstructuraVaciaError(Exception):
    """Se lanza cuando se intenta acceder a una estructura sin elementos."""
    pass


# ===========================================================================
# STACK (LIFO)
# ===========================================================================
class Stack:
    """Pila (LIFO): el último elemento en entrar es el primero en salir.

    Operaciones clásicas:
        push    -> apilar un elemento
        pop     -> desapilar y devolver el elemento del tope
        peek    -> consultar el tope sin extraerlo
        is_empty-> indica si la pila está vacía
        size    -> número de elementos
        clear   -> vaciar la pila
    """

    def __init__(self, iterable=None) -> None:
        # deque es muy eficiente para añadir/quitar por el mismo extremo.
        self._datos: deque = deque(iterable or [])

    def push(self, elemento: Any) -> None:
        """Apila un elemento en el tope de la pila."""
        self._datos.append(elemento)

    def pop(self) -> Any:
        """Extrae y devuelve el elemento del tope. Error si está vacía."""
        if self.is_empty():
            raise EstructuraVaciaError("pop() sobre una pila vacía")
        return self._datos.pop()

    def peek(self) -> Any:
        """Devuelve (sin extraer) el elemento del tope. Error si está vacía."""
        if self.is_empty():
            raise EstructuraVaciaError("peek() sobre una pila vacía")
        return self._datos[-1]

    def is_empty(self) -> bool:
        """True si la pila no tiene elementos."""
        return len(self._datos) == 0

    def size(self) -> int:
        """Número de elementos en la pila."""
        return len(self._datos)

    def clear(self) -> None:
        """Elimina todos los elementos."""
        self._datos.clear()

    # ----- Métodos "mágicos" para una API más pythonica -----
    def __len__(self) -> int:
        return len(self._datos)

    def __iter__(self) -> Iterator[Any]:
        # Iterar del tope hacia la base (orden LIFO).
        return reversed(self._datos)

    def __repr__(self) -> str:
        # El último de la lista es el tope.
        return f"Stack(base->tope: {list(self._datos)})"


# ===========================================================================
# QUEUE (FIFO)
# ===========================================================================
class Queue:
    """Cola (FIFO): el primer elemento en entrar es el primero en salir.

    Operaciones clásicas:
        enqueue -> encolar un elemento (al final)
        dequeue -> desencolar y devolver el elemento del frente
        front   -> consultar el frente sin extraerlo
        rear    -> consultar el último elemento sin extraerlo
        is_empty-> indica si la cola está vacía
        size    -> número de elementos
        clear   -> vaciar la cola
    """

    def __init__(self, iterable=None) -> None:
        self._datos: deque = deque(iterable or [])

    def enqueue(self, elemento: Any) -> None:
        """Añade un elemento al final de la cola."""
        self._datos.append(elemento)

    def dequeue(self) -> Any:
        """Extrae y devuelve el elemento del frente. Error si está vacía."""
        if self.is_empty():
            raise EstructuraVaciaError("dequeue() sobre una cola vacía")
        return self._datos.popleft()

    def front(self) -> Any:
        """Devuelve (sin extraer) el elemento del frente. Error si está vacía."""
        if self.is_empty():
            raise EstructuraVaciaError("front() sobre una cola vacía")
        return self._datos[0]

    def rear(self) -> Any:
        """Devuelve (sin extraer) el último elemento. Error si está vacía."""
        if self.is_empty():
            raise EstructuraVaciaError("rear() sobre una cola vacía")
        return self._datos[-1]

    def is_empty(self) -> bool:
        """True si la cola no tiene elementos."""
        return len(self._datos) == 0

    def size(self) -> int:
        """Número de elementos en la cola."""
        return len(self._datos)

    def clear(self) -> None:
        """Elimina todos los elementos."""
        self._datos.clear()

    # ----- Métodos "mágicos" -----
    def __len__(self) -> int:
        return len(self._datos)

    def __iter__(self) -> Iterator[Any]:
        # Iterar del frente al final (orden FIFO).
        return iter(self._datos)

    def __repr__(self) -> str:
        return f"Queue(frente->final: {list(self._datos)})"


# ===========================================================================
# TABLE / HASH / DICTIONARY (ordenado por inserción)
# ===========================================================================
class OrderedTable:
    """Tabla hash / diccionario que PRESERVA el orden de inserción.

    Internamente usa collections.OrderedDict, que garantiza el recorrido
    en el mismo orden en que se insertaron las claves y permite reordenar.

    Operaciones clásicas:
        put / set   -> insertar o actualizar un par (clave, valor)
        get         -> obtener el valor de una clave (con valor por defecto)
        remove      -> eliminar una clave y devolver su valor
        contains    -> comprobar si existe una clave
        keys/values/items -> vistas de la tabla
        move_to_end -> mover una clave al final (o al principio)
        is_empty / size / clear
    """

    def __init__(self, inicial=None) -> None:
        self._datos: "OrderedDict[Any, Any]" = OrderedDict()
        if inicial:
            # Acepta un dict o una lista de tuplas (clave, valor).
            items = inicial.items() if isinstance(inicial, dict) else inicial
            for clave, valor in items:
                self._datos[clave] = valor

    def put(self, clave: Any, valor: Any) -> None:
        """Inserta o actualiza el valor asociado a una clave.

        Si la clave es nueva, se añade al final (preservando el orden).
        Si ya existía, se actualiza su valor y mantiene su posición.
        """
        self._datos[clave] = valor

    # Alias habitual.
    set = put

    def get(self, clave: Any, por_defecto: Optional[Any] = None) -> Any:
        """Devuelve el valor de la clave, o 'por_defecto' si no existe."""
        return self._datos.get(clave, por_defecto)

    def remove(self, clave: Any) -> Any:
        """Elimina la clave y devuelve su valor. KeyError si no existe."""
        if clave not in self._datos:
            raise KeyError(f"La clave {clave!r} no existe en la tabla")
        return self._datos.pop(clave)

    def contains(self, clave: Any) -> bool:
        """True si la clave existe en la tabla."""
        return clave in self._datos

    def keys(self) -> List[Any]:
        """Lista de claves en orden de inserción."""
        return list(self._datos.keys())

    def values(self) -> List[Any]:
        """Lista de valores en orden de inserción."""
        return list(self._datos.values())

    def items(self) -> List[Tuple[Any, Any]]:
        """Lista de pares (clave, valor) en orden de inserción."""
        return list(self._datos.items())

    def move_to_end(self, clave: Any, last: bool = True) -> None:
        """Mueve una clave al final (last=True) o al principio (last=False)."""
        if clave not in self._datos:
            raise KeyError(f"La clave {clave!r} no existe en la tabla")
        self._datos.move_to_end(clave, last=last)

    def is_empty(self) -> bool:
        """True si la tabla no tiene elementos."""
        return len(self._datos) == 0

    def size(self) -> int:
        """Número de pares (clave, valor)."""
        return len(self._datos)

    def clear(self) -> None:
        """Elimina todos los elementos."""
        self._datos.clear()

    # ----- Métodos "mágicos" para usarla como un dict -----
    def __setitem__(self, clave: Any, valor: Any) -> None:
        self.put(clave, valor)

    def __getitem__(self, clave: Any) -> Any:
        return self._datos[clave]

    def __delitem__(self, clave: Any) -> None:
        self.remove(clave)

    def __contains__(self, clave: Any) -> bool:
        return self.contains(clave)

    def __len__(self) -> int:
        return len(self._datos)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._datos)

    def __repr__(self) -> str:
        return f"OrderedTable({list(self._datos.items())})"


# ===========================================================================
# PROGRAMA DE DEMOSTRACIÓN
# ===========================================================================
def _titulo(texto: str) -> None:
    """Imprime un título decorado para separar las secciones de la demo."""
    print("\n" + "=" * 60)
    print(f"  {texto}")
    print("=" * 60)


def demo_stack() -> None:
    _titulo("STACK (LIFO) - Pila")
    pila = Stack()
    print("¿Vacía al inicio?:", pila.is_empty())

    for n in (10, 20, 30):
        pila.push(n)
        print(f"  push({n}) -> {pila}")

    print("peek() (tope):", pila.peek())
    print("size():", pila.size())

    print("pop():", pila.pop(), "->", pila)
    print("pop():", pila.pop(), "->", pila)
    print("Recorrido (tope->base):", list(pila))
    print("¿Vacía ahora?:", pila.is_empty())


def demo_queue() -> None:
    _titulo("QUEUE (FIFO) - Cola")
    cola = Queue()
    print("¿Vacía al inicio?:", cola.is_empty())

    for cliente in ("Ana", "Luis", "Marta"):
        cola.enqueue(cliente)
        print(f"  enqueue({cliente!r}) -> {cola}")

    print("front() (frente):", cola.front())
    print("rear()  (final):", cola.rear())
    print("size():", cola.size())

    print("dequeue():", cola.dequeue(), "->", cola)
    print("dequeue():", cola.dequeue(), "->", cola)
    print("Recorrido (frente->final):", list(cola))
    print("¿Vacía ahora?:", cola.is_empty())


def demo_tabla() -> None:
    _titulo("TABLE / HASH / DICTIONARY (ordenado)")
    tabla = OrderedTable()
    print("¿Vacía al inicio?:", tabla.is_empty())

    # Insertar con put() y con sintaxis de corchetes.
    tabla.put("nombre", "Carlos")
    tabla["edad"] = 30
    tabla["ciudad"] = "Madrid"
    print("Tras inserciones:", tabla)

    print("get('edad'):", tabla.get("edad"))
    print("get('pais', 'N/D'):", tabla.get("pais", "N/D"))
    print("'ciudad' in tabla:", "ciudad" in tabla)

    # Actualizar un valor existente (conserva su posición).
    tabla["edad"] = 31
    print("Tras actualizar 'edad':", tabla)

    # Mover una clave al final para demostrar el control de orden.
    tabla.move_to_end("nombre")
    print("Tras move_to_end('nombre'):", tabla)

    print("keys():", tabla.keys())
    print("values():", tabla.values())
    print("items():", tabla.items())

    valor = tabla.remove("ciudad")
    print(f"remove('ciudad') -> {valor!r} ->", tabla)
    print("size():", tabla.size())


def main() -> None:
    print("DEMOSTRACIÓN DE ESTRUCTURAS DE DATOS CLÁSICAS")
    demo_stack()
    demo_queue()
    demo_tabla()
    print("\nFin de la demostración.")


if __name__ == "__main__":
    main()
