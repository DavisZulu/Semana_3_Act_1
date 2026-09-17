# Semana 3 — Encapsulamiento, Herencia y Polimorfismo

**Proyecto:** Quantum Core — Sistema de gestión de transacciones
**Autor:** Deibis Zuluaga Baena
**Núcleo:** Fundamentos de Software · CEIPA Business School
**Docente:** Simón Peláez Loaiza
**Repositorio:** https://github.com/DavisZulu/Semana_3_Act_1

## Descripción

En esta actividad se tomó como punto de partida el archivo
`transaccion_poo_v1.py` de la Semana 2 y se transformó en una solución más
segura, organizada y extensible mediante los fundamentos de la Programación
Orientada a Objetos.

El resultado principal es `diseno_pilares_poo.py`, un programa que lee
transacciones desde un archivo de texto, valida sus datos, crea objetos
especializados según el tipo de operación y calcula un impacto diferente para
cada clase.

## Objetivo

Aplicar los siguientes conceptos:

- **Encapsulamiento:** proteger el monto y validar los valores antes de
  almacenarlos.
- **Herencia:** reutilizar los datos y métodos comunes mediante una clase base.
- **Polimorfismo:** utilizar el mismo método con resultados diferentes según la
  clase del objeto.
- **Manejo de errores:** identificar registros incorrectos sin detener el
  procesamiento de los demás datos.
- **Organización:** separar la creación, lectura, consulta y presentación de las
  transacciones.

## Archivos de la actividad

```text
Semana_3/
├── diseno_pilares_poo.py
├── transacciones.txt
└── README.md
```

- `diseno_pilares_poo.py`: contiene las clases y la lógica del programa.
- `transacciones.txt`: contiene 20 registros simulados.
- `README.md`: documenta el desarrollo y los resultados de la actividad.

## Proceso realizado

### 1. Preparación del archivo

Se creó la carpeta `Semana_3`. Después se copió
`Semana_2/transaccion_poo_v1.py` y se renombró como
`diseno_pilares_poo.py`.

Este procedimiento permitió conservar la solución de la Semana 2 y desarrollar
la nueva versión sin modificar el trabajo anterior.

### 2. Encapsulamiento del monto

En la versión anterior, el monto era un atributo público:

```python
self.monto = monto
```

En la nueva versión, el valor real se guarda internamente como
`self._monto`. Para consultar y modificar este dato se utilizan un getter y
un setter:

```python
@property
def monto(self):
    return self._monto

@monto.setter
def monto(self, nuevo_monto):
    nuevo_monto = float(nuevo_monto)

    if nuevo_monto < 0:
        raise ValueError("El monto asignado no puede ser negativo.")

    self._monto = nuevo_monto
```

El constructor utiliza `self.monto = monto` para que el valor inicial también
pase por el setter y sea validado.

### 3. Validación de datos

El setter rechaza cualquier monto menor que cero mediante `ValueError`.

El archivo de prueba conserva el registro proporcionado por el profesor:

```text
T005,CREDITO,-1
```

Al procesarlo, el programa muestra:

```text
Registro T005 ignorado en la línea 5: El monto asignado no puede ser negativo.
```

El mensaje indica tanto el identificador como la línea exacta donde se encontró
el problema.

### 4. Creación de la clase base

La clase original se convirtió en `TransaccionBase`. Allí se encuentran los
elementos compartidos por todos los tipos:

- Constructor.
- Identificador.
- Tipo.
- Monto protegido.
- Getter y setter.
- Validación.
- Métodos de consulta.
- Declaración de `calcular_impacto()`.

El método de la clase base utiliza `NotImplementedError` para dejar claro que
cada clase hija debe proporcionar su propia fórmula:

```python
def calcular_impacto(self):
    raise NotImplementedError(
        "Cada tipo de transacción debe calcular su propio impacto."
    )
```

### 5. Herencia

Se crearon cuatro clases hijas:

```python
class TransaccionCredito(TransaccionBase):
    ...

class TransaccionDebito(TransaccionBase):
    ...

class TransaccionEfectivo(TransaccionBase):
    ...

class TransaccionCripto(TransaccionBase):
    ...
```

Todas heredan el constructor, el getter, el setter, la validación y los métodos
de información. Por esa razón, no es necesario repetir esas partes en cada
clase.

### 6. Polimorfismo

Cada clase hija sobrescribe `calcular_impacto()`:

| Tipo | Regla | Ejemplo con 100.000 |
|---|---:|---:|
| Crédito | 2 % del monto | 2.000 |
| Débito | Comisión fija de 1.500 | 1.500 |
| Efectivo | 1 % del monto | 1.000 |
| Cripto | 3 % del monto | 3.000 |

El programa recorre todos los objetos con una sola instrucción:

```python
transaccion.calcular_impacto()
```

La llamada es la misma, pero Python ejecuta la fórmula correspondiente a la
clase real de cada objeto.

### 7. Selección del tipo de objeto

Se creó `crear_transaccion()` para decidir qué clase debe instanciarse según
el tipo leído:

```python
if tipo == "CREDITO":
    return TransaccionCredito(cliente_id, tipo, monto)
elif tipo == "DEBITO":
    return TransaccionDebito(cliente_id, tipo, monto)
elif tipo == "EFECTIVO":
    return TransaccionEfectivo(cliente_id, tipo, monto)
elif tipo == "CRIPTO":
    return TransaccionCripto(cliente_id, tipo, monto)
```

Antes de comparar, `tipo.upper()` normaliza el texto. De esta manera se pueden
recibir valores escritos como `credito`, `Credito` o `CREDITO`.

### 8. Lectura robusta del archivo

La función `leer_y_almacenar_datos()`:

1. Abre `transacciones.txt`.
2. Recorre las líneas mediante `enumerate()`.
3. Separa el identificador, el tipo y el monto.
4. Intenta crear el objeto correspondiente.
5. Agrega a la lista únicamente los objetos válidos.
6. Informa los errores y continúa con las líneas siguientes.

El bloque `try/except` evita que un registro inválido detenga todo el
programa.

### 9. Datos adicionales

El archivo original del profesor contenía 6 registros. Se conservaron y se
agregaron 14 transacciones simuladas para tener 20 casos en total.

Los datos adicionales permiten probar:

- Diferentes montos.
- Los cuatro tipos implementados.
- Un monto negativo.
- El valor límite de cero.
- Cálculos porcentuales y una comisión fija.

De los 20 registros, 19 son válidos y uno es rechazado correctamente.

### 10. Funciones conservadas

Se mantuvieron dos funciones útiles de la solución anterior:

- `calcular_monto_total()`: suma los montos de las transacciones válidas.
- `filtrar_por_tipo()`: devuelve únicamente los objetos del tipo solicitado.

Aunque la demostración principal muestra todas las transacciones, la función de
filtrado permanece disponible para futuras consultas.

## Ejecución

Desde la terminal, entrar en la carpeta:

```bash
cd /Users/deibiszuluaga/Desktop/ProyectosCeipa/Semana_3
```

Ejecutar:

```bash
python3 diseno_pilares_poo.py
```

## Resultado verificado

El programa:

- Detecta el monto negativo de `T005`.
- Continúa procesando los otros 19 registros.
- Calcula un monto total válido de `$7.580.000`.
- Muestra la información y el impacto de cada transacción.
- Finaliza sin errores.

Ejemplo parcial:

```text
Registro T005 ignorado en la línea 5: El monto asignado no puede ser negativo.
Monto total: $7580000.00

--- Transacciones válidas e impacto ---
ID: T001 | Tipo: CREDITO | Monto: $500000.00 | Impacto: $10000.00
ID: T002 | Tipo: DEBITO | Monto: $80000.00 | Impacto: $1500.00
ID: T006 | Tipo: EFECTIVO | Monto: $10000.00 | Impacto: $100.00
ID: T007 | Tipo: CRIPTO | Monto: $250000.00 | Impacto: $7500.00
```

## Conclusiones

El encapsulamiento impide almacenar montos negativos y mantiene el dato bajo el
control de la clase. La herencia evita repetir el constructor y las
validaciones. El polimorfismo permite procesar diferentes clases con la misma
llamada a `calcular_impacto()`.

La incorporación de Efectivo y Cripto demuestra que la solución puede ampliarse
mediante nuevas clases hijas. El manejo de errores garantiza que un dato
incorrecto sea identificado sin perder el procesamiento de los registros
válidos.
