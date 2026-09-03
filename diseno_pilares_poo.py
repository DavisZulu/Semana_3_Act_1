"""
diseno_pilares_poo.py
Semana 3 - Actividad 1: Encapsulamiento, Herencia y Polimorfismo.

Este programa evoluciona la solución de la Semana 2. Lee transacciones desde
un archivo de texto y crea un objeto especializado para cada tipo de operación.

Conceptos demostrados:
    Encapsulamiento: el monto se almacena en _monto y se valida con un setter.
    Herencia: las clases Crédito, Débito, Efectivo y Cripto reutilizan la base.
    Polimorfismo: cada clase implementa calcular_impacto() de forma diferente.

Formato esperado en transacciones.txt:
    IDENTIFICADOR,TIPO,MONTO

Ejemplo:
    T001,CREDITO,500000

Ejecución:
    python3 diseno_pilares_poo.py
"""


# ============================================================================
# 1. CLASE BASE: DATOS Y COMPORTAMIENTOS COMUNES
# ============================================================================
class TransaccionBase:
    """
    Representa la estructura común de todas las transacciones.

    El constructor, la validación del monto y los métodos de consulta se
    escriben una sola vez en esta clase. Las clases hijas los reutilizan y
    solamente implementan la regla que las hace diferentes.
    """

    def __init__(self, cliente_id, tipo, monto):
        """
        Inicializa una transacción.

        Parámetros:
            cliente_id: identificador del registro, por ejemplo T001.
            tipo: nombre del tipo de transacción.
            monto: valor monetario de la transacción.

        La asignación self.monto = monto pasa por el setter. De esta manera,
        incluso el valor inicial se valida antes de almacenarse.
        """
        self.cliente_id = cliente_id
        self.tipo = tipo
        self.monto = monto

    # Getter: permite consultar el monto mediante objeto.monto. El valor real
    # permanece almacenado internamente en el atributo protegido _monto.
    @property
    def monto(self):
        """Devuelve el monto protegido de la transacción."""
        return self._monto

    # Setter: se ejecuta al crear la transacción o al asignar un nuevo monto.
    # Convierte el dato a float y evita guardar cantidades negativas.
    @monto.setter
    def monto(self, nuevo_monto):
        """Valida y almacena un nuevo monto."""
        nuevo_monto = float(nuevo_monto)

        if nuevo_monto < 0:
            raise ValueError("El monto asignado no puede ser negativo.")

        # Se usa _monto para almacenar el dato sin llamar otra vez al setter.
        self._monto = nuevo_monto

    def calcular_impacto(self):
        """
        Declara el comportamiento que debe implementar cada clase hija.

        La clase base no posee una fórmula general. Si una hija olvida crear
        su propia versión, este error informa claramente qué falta.
        """
        raise NotImplementedError(
            "Cada tipo de transacción debe calcular su propio impacto."
        )

    def obtener_informacion(self):
        """Devuelve los datos principales en un texto fácil de leer."""
        return (
            f"ID: {self.cliente_id} | "
            f"Tipo: {self.tipo} | "
            f"Monto: ${self.monto:.2f}"
        )

    def obtener_monto(self):
        """Devuelve el monto para operaciones como el cálculo del total."""
        return self.monto

    def es_del_tipo(self, tipo_filtro):
        """Indica si la transacción corresponde al tipo solicitado."""
        return self.tipo == tipo_filtro


# ============================================================================
# 2. CLASES HIJAS: HERENCIA Y POLIMORFISMO
# ============================================================================
# Todas las hijas reciben el constructor, el getter, el setter y los métodos de
# consulta de TransaccionBase. Cada una sobrescribe calcular_impacto() con una
# regla propia; esa respuesta diferente al mismo método es el polimorfismo.


class TransaccionCredito(TransaccionBase):
    """Representa un crédito cuyo impacto corresponde al 2 % del monto."""

    def calcular_impacto(self):
        """Calcula un impacto porcentual del 2 %."""
        return self.monto * 0.02


class TransaccionDebito(TransaccionBase):
    """Representa un débito con una comisión fija de 1.500."""

    def calcular_impacto(self):
        """Devuelve la comisión fija de una transacción débito."""
        return 1500


class TransaccionEfectivo(TransaccionBase):
    """Representa una operación en efectivo con impacto del 1 %."""

    def calcular_impacto(self):
        """Calcula un impacto porcentual del 1 %."""
        return self.monto * 0.01


class TransaccionCripto(TransaccionBase):
    """Representa una operación con criptomonedas e impacto del 3 %."""

    def calcular_impacto(self):
        """Calcula un impacto porcentual del 3 %."""
        return self.monto * 0.03


# ============================================================================
# 3. CREACIÓN DE OBJETOS SEGÚN EL TIPO
# ============================================================================
def crear_transaccion(cliente_id, tipo, monto):
    """
    Crea el objeto especializado que corresponde al tipo recibido.

    Centralizar esta decisión evita repartir condiciones por todo el programa.
    Si el tipo no está soportado, genera un ValueError que será manejado por la
    función encargada de leer el archivo.
    """
    # Normalizar permite aceptar CREDITO, Credito o credito de la misma manera.
    tipo = tipo.upper()

    if tipo == "CREDITO":
        return TransaccionCredito(cliente_id, tipo, monto)
    elif tipo == "DEBITO":
        return TransaccionDebito(cliente_id, tipo, monto)
    elif tipo == "EFECTIVO":
        return TransaccionEfectivo(cliente_id, tipo, monto)
    elif tipo == "CRIPTO":
        return TransaccionCripto(cliente_id, tipo, monto)
    else:
        raise ValueError(f"Tipo de transacción desconocido: {tipo}")


# ============================================================================
# 4. LECTURA Y CONVERSIÓN DEL ARCHIVO A OBJETOS
# ============================================================================
def leer_y_almacenar_datos(nombre_archivo):
    """
    Lee el archivo y convierte cada registro válido en un objeto.

    Cada línea debe contener cliente_id, tipo y monto separados por comas. El
    resultado es una lista que puede mezclar objetos de todas las clases hijas.
    Los registros con valores inválidos se reportan y se ignoran sin detener la
    lectura de las líneas siguientes.
    """
    lista_transacciones = []

    # El bloque with cierra automáticamente el archivo cuando termina la lectura.
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        # enumerate proporciona el número real de cada línea para los avisos.
        for numero_linea, linea in enumerate(archivo, start=1):
            # strip elimina espacios externos y split separa los tres campos.
            datos = linea.strip().split(",")

            # Solo se procesa una línea cuando contiene exactamente tres datos.
            if len(datos) == 3:
                try:
                    transaccion = crear_transaccion(
                        datos[0].strip(),
                        datos[1].strip(),
                        float(datos[2].strip()),
                    )

                    # La lista recibe únicamente objetos creados correctamente.
                    lista_transacciones.append(transaccion)

                except ValueError as error:
                    # Se identifica el registro y la línea sin detener el programa.
                    print(
                        f"Registro {datos[0].strip()} ignorado "
                        f"en la línea {numero_linea}: {error}"
                    )

    return lista_transacciones


# ============================================================================
# 5. FUNCIONES DE CONSULTA CONSERVADAS DE LA SEMANA 2
# ============================================================================
def calcular_monto_total(lista_transacciones):
    """Suma los montos de todos los objetos recibidos."""
    total_monto = 0.0

    for transaccion in lista_transacciones:
        total_monto = total_monto + transaccion.obtener_monto()

    return total_monto


def filtrar_por_tipo(lista_transacciones, tipo_filtro):
    """
    Devuelve una lista con las transacciones del tipo solicitado.

    Esta función se conserva porque sigue siendo útil para consultar grupos
    concretos, aunque la demostración principal recorra todos los objetos.
    """
    lista_filtrada = []

    for transaccion in lista_transacciones:
        if transaccion.es_del_tipo(tipo_filtro):
            lista_filtrada.append(transaccion)

    return lista_filtrada


# ============================================================================
# 6. FLUJO PRINCIPAL Y DEMOSTRACIÓN DEL POLIMORFISMO
# ============================================================================
def ejecutar_sistema():
    """
    Lee las transacciones, calcula el total y muestra el impacto de cada una.

    El ciclo final no pregunta qué clase tiene cada objeto. Siempre ejecuta
    calcular_impacto(), y Python selecciona la versión correspondiente.
    """
    transacciones = leer_y_almacenar_datos("transacciones.txt")
    monto_total = calcular_monto_total(transacciones)

    print(f"Monto total: ${monto_total:.2f}")
    print("\n--- Transacciones válidas e impacto ---")

    # Misma llamada, resultados distintos: aquí se observa el polimorfismo.
    for transaccion in transacciones:
        print(
            transaccion.obtener_informacion(),
            f"| Impacto: ${transaccion.calcular_impacto():.2f}",
        )


# Este bloque evita que la demostración se ejecute al importar las clases desde
# otro archivo. Solo inicia el sistema cuando ejecutamos este archivo directamente.
if __name__ == "__main__":
    ejecutar_sistema()
