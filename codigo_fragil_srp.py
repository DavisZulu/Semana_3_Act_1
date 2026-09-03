# codigo_fragil_srp.py
# Semana 3 - Actividad 2: codigo para ANALIZAR (no hay que corregirlo en codigo,
# solo diagnosticar las violaciones de SRP y OCP en el informe).
# Para ejecutar:  python codigo_fragil_srp.py


class GestorTransaccionPrincipal:
    def __init__(self, datos):
        self.datos = datos  # ej: {"id": "T001", "tipo": "CREDITO", "monto": 500000}

    def procesar_y_validar_y_reportar(self):
        # 1) RESPONSABILIDAD: validacion de datos
        if self.datos["monto"] < 0:
            print("ERROR: el monto no puede ser negativo.")
            return
        if self.datos["tipo"] not in ("CREDITO", "DEBITO"):
            print("ERROR: tipo de transaccion desconocido.")
            return

        # 2) RESPONSABILIDAD: logica de negocio
        if self.datos["tipo"] == "CREDITO":
            impacto = self.datos["monto"] * 0.02
        else:
            impacto = 1500

        # 3) RESPONSABILIDAD: reporte (formato texto plano)
        print("===== REPORTE =====")
        print("ID:", self.datos["id"])
        print("Tipo:", self.datos["tipo"])
        print("Monto:", self.datos["monto"])
        print("Impacto:", impacto)


# Ejemplo de uso
gestor = GestorTransaccionPrincipal({"id": "T001", "tipo": "CREDITO", "monto": 500000})
gestor.procesar_y_validar_y_reportar()
