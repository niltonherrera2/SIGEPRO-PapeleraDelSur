"""
SIGEPRO - Sistema de Gestión de Procedimientos y Solicitudes Técnicas
Papelera del Sur S.A.

Ejecutar con:  python sistema.py
Usuario de prueba: admin / admin123
"""
from getpass import getpass

from gestores import GestorProcedimientos, GestorSolicitudes, GestorTrabajadores
from modelo import Prioridad, Procedimiento, SolicitudTecnica, Trabajador, Usuario

NIVELES = ("Baja", "Media", "Alta")
MAX_INTENTOS = 3


# ----------------------------------------------------------------------
# Utilidades de entrada por consola
# ----------------------------------------------------------------------
def titulo(texto):
    print()
    print("=" * 60)
    print(texto.center(60))
    print("=" * 60)


def leer_texto(mensaje, obligatorio=True):
    while True:
        valor = input(mensaje).strip()
        if valor or not obligatorio:
            return valor
        print("  ! Este dato es obligatorio.")


def leer_opcion(mensaje, opciones):
    """Muestra opciones numeradas y devuelve la elegida."""
    for i, opcion in enumerate(opciones, 1):
        print(f"   {i}. {opcion}")
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and 1 <= int(valor) <= len(opciones):
            return opciones[int(valor) - 1]
        print(f"  ! Ingrese un número entre 1 y {len(opciones)}.")


def pausa():
    input("\nPresione ENTER para continuar...")


# ----------------------------------------------------------------------
# Sistema principal
# ----------------------------------------------------------------------
class Sistema:
    def __init__(self):
        self.procedimientos = GestorProcedimientos()
        self.trabajadores = GestorTrabajadores()
        self.solicitudes = GestorSolicitudes()
        self.usuarios = []
        self.usuario_actual = None
        self._cargar_datos_iniciales()

    def _cargar_datos_iniciales(self):
        self.usuarios.append(Usuario("U001", "Ana", "Torres", "admin", "admin123", "Administrador"))
        self.usuarios.append(Usuario("U002", "Luis", "Paredes", "encargado", "enc123", "Encargado"))

        for t in (Trabajador("T001", "Carlos", "Ramírez", "Mantenimiento", "Técnico mecánico"),
                  Trabajador("T002", "María", "Quispe", "Producción", "Operaria de máquina"),
                  Trabajador("T003", "Jorge", "Salas", "Seguridad", "Supervisor SST")):
            self.trabajadores.registrar(t)

        self.procedimientos.registrar(Procedimiento(
            "PR-001", "Cambio de rodillos de la bobinadora", "Mantenimiento",
            "Reemplazo de rodillos desgastados de la bobinadora principal.",
            "Mantenimiento", "Carlos Ramírez",
            ["Bloquear y etiquetar la máquina (LOTO).",
             "Retirar la tensión del papel.",
             "Desmontar y reemplazar los rodillos.",
             "Probar en vacío antes de reanudar."]))
        self.procedimientos.registrar(Procedimiento(
            "PR-002", "Limpieza de la pulpadora", "Producción",
            "Limpieza semanal de la pulpadora para evitar atascos.",
            "Producción", "María Quispe",
            ["Detener la alimentación de fibra.",
             "Drenar el tanque.",
             "Retirar residuos con herramientas autorizadas."]))
        self.procedimientos.registrar(Procedimiento(
            "PR-003", "Uso de EPP en zona de calderas", "Seguridad",
            "Equipos de protección personal obligatorios en calderas.",
            "Seguridad", "Jorge Salas",
            ["Usar casco, lentes y guantes térmicos.",
             "Verificar el permiso de trabajo en caliente."]))

        self.solicitudes.registrar(self.trabajadores.buscar_por_codigo("T002"),
                                   "Atasco frecuente en la pulpadora", "Falla de equipo",
                                   "Media", "Alta",
                                   self.procedimientos.buscar_por_codigo("PR-002"))

    # ------------------------------------------------------------------
    # Login
    # ------------------------------------------------------------------
    def iniciar_sesion(self):
        titulo("SIGEPRO - PAPELERA DEL SUR S.A.")
        print("Iniciar sesión".center(60))
        for intento in range(1, MAX_INTENTOS + 1):
            usuario = leer_texto("Usuario    : ")
            contrasena = getpass("Contraseña : ")
            for u in self.usuarios:
                if u.validar_credenciales(usuario, contrasena):
                    self.usuario_actual = u
                    print(f"\nBienvenido(a), {u.nombre_completo()} ({u.rol}).")
                    return True
            restantes = MAX_INTENTOS - intento
            print(f"  ! Credenciales inválidas. Intentos restantes: {restantes}\n")
        print("Se superó el número de intentos. El sistema se cerrará.")
        return False

    # ------------------------------------------------------------------
    # Menú principal
    # ------------------------------------------------------------------
    def ejecutar(self):
        if not self.iniciar_sesion():
            return
        while True:
            titulo("MENÚ PRINCIPAL")
            print("   1. Gestionar procedimientos")
            print("   2. Gestionar trabajadores")
            print("   3. Gestionar solicitudes técnicas")
            print("   0. Salir")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "1":
                self.menu_procedimientos()
            elif opcion == "2":
                self.menu_trabajadores()
            elif opcion == "3":
                self.menu_solicitudes()
            elif opcion == "0":
                print(f"\nSesión cerrada. Hasta pronto, {self.usuario_actual.nombre}.")
                return
            else:
                print("  ! Opción no válida.")

    # ------------------------------------------------------------------
    # Módulo de procedimientos (HU1 - HU4)
    # ------------------------------------------------------------------
    def menu_procedimientos(self):
        acciones = {"1": self.registrar_procedimiento, "2": self.buscar_procedimiento,
                    "3": self.listar_procedimientos, "4": self.consultar_procedimiento,
                    "5": self.modificar_procedimiento}
        while True:
            titulo("GESTIONAR PROCEDIMIENTOS")
            print("   1. Registrar procedimiento")
            print("   2. Buscar procedimiento")
            print("   3. Listar procedimientos")
            print("   4. Consultar procedimiento")
            print("   5. Modificar procedimiento")
            print("   0. Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                return
            if opcion in acciones:
                acciones[opcion]()
                pausa()
            else:
                print("  ! Opción no válida.")

    def registrar_procedimiento(self):
        titulo("REGISTRAR PROCEDIMIENTO")
        codigo = leer_texto("Código       : ").upper()
        if self.procedimientos.buscar_por_codigo(codigo):
            print(f"  ! Ya existe un procedimiento con código {codigo}.")
            return
        nombre = leer_texto("Nombre       : ")
        categoria = leer_texto("Categoría    : ")
        descripcion = leer_texto("Descripción  : ")
        area = leer_texto("Área         : ")
        responsable = leer_texto("Responsable  : ")
        print("Indicaciones principales (deje vacío para terminar):")
        indicaciones = []
        while True:
            paso = leer_texto(f"  Paso {len(indicaciones) + 1}: ", obligatorio=False)
            if not paso:
                break
            indicaciones.append(paso)
        if not indicaciones:
            print("  ! Debe ingresar al menos una indicación. No se registró.")
            return
        self.procedimientos.registrar(Procedimiento(codigo, nombre, categoria, descripcion,
                                                    area, responsable, indicaciones))
        print(f"\n>> Procedimiento {codigo} registrado correctamente.")

    def buscar_procedimiento(self):
        titulo("BUSCAR PROCEDIMIENTO")
        texto = leer_texto("Ingrese código, nombre o categoría: ")
        resultados = self.procedimientos.buscar(texto)
        if not resultados:
            print("No se encontraron coincidencias.")
            return
        print(f"\nSe encontraron {len(resultados)} coincidencia(s):")
        self._tabla_procedimientos(resultados)

    def listar_procedimientos(self):
        titulo("LISTA DE PROCEDIMIENTOS")
        self._tabla_procedimientos(self.procedimientos.listar())
        print(f"Total: {self.procedimientos.cantidad()} procedimiento(s)")

    def consultar_procedimiento(self):
        titulo("CONSULTAR PROCEDIMIENTO")
        codigo = leer_texto("Código del procedimiento: ")
        p = self.procedimientos.buscar_por_codigo(codigo)
        if p is None:
            print(f"  ! No existe el procedimiento {codigo}.")
            return
        print()
        print(p.mostrar_detalle())

    def modificar_procedimiento(self):
        titulo("MODIFICAR PROCEDIMIENTO")
        codigo = leer_texto("Código del procedimiento: ")
        p = self.procedimientos.buscar_por_codigo(codigo)
        if p is None:
            print(f"  ! No existe el procedimiento {codigo}.")
            return
        print("Deje vacío el campo que no desea cambiar.")
        nombre = leer_texto(f"Nombre [{p.nombre}]: ", obligatorio=False)
        categoria = leer_texto(f"Categoría [{p.categoria}]: ", obligatorio=False)
        print(f"Estado actual: {p.estado}")
        estado = leer_opcion("Nuevo estado: ", list(Procedimiento.ESTADOS))
        p.modificar(nombre=nombre, categoria=categoria, estado=estado)
        print(f"\n>> Procedimiento {p.codigo} actualizado.")

    @staticmethod
    def _tabla_procedimientos(lista):
        print(f"{'CÓDIGO':<8}{'NOMBRE':<38}{'CATEGORÍA':<15}{'ÁREA':<15}{'ESTADO':<10}")
        print("-" * 86)
        for p in lista:
            print(f"{p.codigo:<8}{p.nombre[:36]:<38}{p.categoria:<15}{p.area:<15}{p.estado:<10}")

    # ------------------------------------------------------------------
    # Módulo de trabajadores (HU5)
    # ------------------------------------------------------------------
    def menu_trabajadores(self):
        acciones = {"1": self.registrar_trabajador, "2": self.buscar_trabajador,
                    "3": self.listar_trabajadores}
        while True:
            titulo("GESTIONAR TRABAJADORES")
            print("   1. Registrar trabajador")
            print("   2. Buscar trabajador")
            print("   3. Listar trabajadores")
            print("   0. Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                return
            if opcion in acciones:
                acciones[opcion]()
                pausa()
            else:
                print("  ! Opción no válida.")

    def registrar_trabajador(self):
        titulo("REGISTRAR TRABAJADOR")
        codigo = leer_texto("Código   : ").upper()
        if self.trabajadores.buscar_por_codigo(codigo):
            print(f"  ! Ya existe un trabajador con código {codigo}.")
            return
        nombre = leer_texto("Nombre   : ")
        apellido = leer_texto("Apellido : ")
        area = leer_texto("Área     : ")
        cargo = leer_texto("Cargo    : ")
        self.trabajadores.registrar(Trabajador(codigo, nombre, apellido, area, cargo))
        print(f"\n>> Trabajador {codigo} registrado correctamente.")

    def buscar_trabajador(self):
        titulo("BUSCAR TRABAJADOR")
        texto = leer_texto("Ingrese código o nombre: ")
        resultados = self.trabajadores.buscar(texto)
        if not resultados:
            print("No se encontraron coincidencias.")
        for t in resultados:
            print(t.mostrar_info())

    def listar_trabajadores(self):
        titulo("LISTA DE TRABAJADORES")
        for t in self.trabajadores.listar():
            print(t.mostrar_info())

    # ------------------------------------------------------------------
    # Módulo de solicitudes técnicas (HU6 - HU10)
    # ------------------------------------------------------------------
    def menu_solicitudes(self):
        acciones = {"1": self.registrar_solicitud, "2": self.calcular_prioridad,
                    "3": self.buscar_solicitud, "4": self.listar_solicitudes,
                    "5": self.actualizar_estado}
        while True:
            titulo("GESTIONAR SOLICITUDES TÉCNICAS")
            print("   1. Registrar solicitud")
            print("   2. Calcular prioridad")
            print("   3. Buscar / consultar solicitud")
            print("   4. Listar solicitudes")
            print("   5. Actualizar estado")
            print("   0. Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                return
            if opcion in acciones:
                acciones[opcion]()
                pausa()
            else:
                print("  ! Opción no válida.")

    def registrar_solicitud(self):
        titulo("REGISTRAR SOLICITUD TÉCNICA")
        trabajador = self.trabajadores.buscar_por_codigo(leer_texto("Código del trabajador: "))
        if trabajador is None:
            print("  ! Trabajador no registrado. Regístrelo primero.")
            return
        print(f"Trabajador: {trabajador.mostrar_info()}")
        descripcion = leer_texto("Descripción del problema: ")
        print("Tipo de solicitud:")
        tipo = leer_opcion("Opción: ", list(SolicitudTecnica.TIPOS))
        print("Nivel de urgencia:")
        urgencia = leer_opcion("Opción: ", list(NIVELES))
        print("Impacto en la actividad:")
        impacto = leer_opcion("Opción: ", list(NIVELES))
        codigo_proc = leer_texto("Procedimiento relacionado (código o vacío): ", obligatorio=False)
        procedimiento = self.procedimientos.buscar_por_codigo(codigo_proc) if codigo_proc else None
        if codigo_proc and procedimiento is None:
            print("  ! Procedimiento no encontrado; se registrará sin relación.")
        s = self.solicitudes.registrar(trabajador, descripcion, tipo, urgencia, impacto,
                                       procedimiento)
        print(f"\n>> Solicitud {s.codigo} registrada correctamente.\n")
        print(s.mostrar_detalle())

    def calcular_prioridad(self):
        titulo("CALCULAR PRIORIDAD")
        print("Nivel de urgencia:")
        urgencia = leer_opcion("Opción: ", list(NIVELES))
        print("Impacto en la actividad:")
        impacto = leer_opcion("Opción: ", list(NIVELES))
        p = Prioridad(urgencia, impacto)
        print(f"\nPuntaje urgencia : {Prioridad.PUNTAJES[urgencia]}")
        print(f"Puntaje impacto  : {Prioridad.PUNTAJES[impacto]}")
        print(f"Puntaje total    : {p.calcular_puntaje()}")
        print(f"Prioridad        : {p.determinar_nivel()}")
        print(f"Tiempo estimado  : {p.tiempo_estimado()} horas")

    def buscar_solicitud(self):
        titulo("BUSCAR SOLICITUD")
        texto = leer_texto("Ingrese código de solicitud o trabajador: ")
        resultados = self.solicitudes.buscar(texto)
        if not resultados:
            print("No se encontraron coincidencias.")
        for s in resultados:
            print()
            print(s.mostrar_detalle())

    def listar_solicitudes(self):
        titulo("LISTA DE SOLICITUDES")
        print(f"{'CÓDIGO':<9}{'TRABAJADOR':<20}{'PRIORIDAD':<11}{'TIEMPO':<9}{'ESTADO':<12}")
        print("-" * 61)
        for s in self.solicitudes.listar():
            print(f"{s.codigo:<9}{s.trabajador.nombre_completo():<20}"
                  f"{s.prioridad.determinar_nivel():<11}{str(s.prioridad.tiempo_estimado()) + ' h':<9}"
                  f"{s.estado:<12}")

    def actualizar_estado(self):
        titulo("ACTUALIZAR ESTADO DE SOLICITUD")
        s = self.solicitudes.buscar_por_codigo(leer_texto("Código de solicitud: "))
        if s is None:
            print("  ! Solicitud no encontrada.")
            return
        print(f"Estado actual: {s.estado}")
        nuevo = leer_opcion("Nuevo estado: ", list(SolicitudTecnica.ESTADOS))
        try:
            s.actualizar_estado(nuevo)
            print(f"\n>> Solicitud {s.codigo} ahora está: {s.estado}")
        except ValueError as error:
            print(f"  ! {error}")


if __name__ == "__main__":
    Sistema().ejecutar()
