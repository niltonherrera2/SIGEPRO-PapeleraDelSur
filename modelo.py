"""
Clases del modelo del Sistema de Gestión de Procedimientos y Solicitudes
Técnicas (SIGEPRO) - Papelera del Sur S.A.
"""
from datetime import date


# ----------------------------------------------------------------------
# Herencia: Persona es la clase base de Trabajador y Usuario
# ----------------------------------------------------------------------
class Persona:
    def __init__(self, codigo, nombre, apellido):
        self._codigo = codigo
        self._nombre = nombre
        self._apellido = apellido

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    def nombre_completo(self):
        return f"{self._nombre} {self._apellido}"

    def mostrar_info(self):
        return f"[{self._codigo}] {self.nombre_completo()}"


class Trabajador(Persona):
    def __init__(self, codigo, nombre, apellido, area, cargo):
        super().__init__(codigo, nombre, apellido)
        self._area = area
        self._cargo = cargo

    @property
    def area(self):
        return self._area

    @property
    def cargo(self):
        return self._cargo

    # Polimorfismo: redefine el método de la clase base
    def mostrar_info(self):
        return f"{super().mostrar_info()} - {self._cargo} ({self._area})"


class Usuario(Persona):
    def __init__(self, codigo, nombre, apellido, usuario, contrasena, rol):
        super().__init__(codigo, nombre, apellido)
        self._usuario = usuario
        self.__contrasena = contrasena  # atributo privado (encapsulamiento)
        self._rol = rol

    @property
    def usuario(self):
        return self._usuario

    @property
    def rol(self):
        return self._rol

    def validar_credenciales(self, usuario, contrasena):
        return self._usuario == usuario and self.__contrasena == contrasena

    def mostrar_info(self):
        return f"{super().mostrar_info()} - Rol: {self._rol}"


# ----------------------------------------------------------------------
# Procedimiento técnico
# ----------------------------------------------------------------------
class Procedimiento:
    ESTADOS = ("Vigente", "En revisión", "Obsoleto")

    def __init__(self, codigo, nombre, categoria, descripcion, area,
                 responsable, indicaciones, estado="Vigente", fecha_registro=None):
        self._codigo = codigo
        self._nombre = nombre
        self._categoria = categoria
        self._descripcion = descripcion
        self._area = area
        self._responsable = responsable
        self._indicaciones = list(indicaciones)
        self._estado = estado
        self._fecha_registro = fecha_registro or date.today()

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def categoria(self):
        return self._categoria

    @property
    def area(self):
        return self._area

    @property
    def estado(self):
        return self._estado

    def coincide(self, texto):
        """True si el texto aparece en el código, nombre o categoría."""
        texto = texto.lower()
        return (texto in self._codigo.lower()
                or texto in self._nombre.lower()
                or texto in self._categoria.lower())

    def modificar(self, nombre=None, categoria=None, descripcion=None,
                  area=None, responsable=None, estado=None, indicaciones=None):
        if nombre:
            self._nombre = nombre
        if categoria:
            self._categoria = categoria
        if descripcion:
            self._descripcion = descripcion
        if area:
            self._area = area
        if responsable:
            self._responsable = responsable
        if estado:
            if estado not in Procedimiento.ESTADOS:
                raise ValueError(f"Estado no válido: {estado}")
            self._estado = estado
        if indicaciones:
            self._indicaciones = list(indicaciones)

    def mostrar_detalle(self):
        lineas = [
            f"Código        : {self._codigo}",
            f"Nombre        : {self._nombre}",
            f"Categoría     : {self._categoria}",
            f"Descripción   : {self._descripcion}",
            f"Área          : {self._area}",
            f"Responsable   : {self._responsable}",
            f"Fecha registro: {self._fecha_registro:%d/%m/%Y}",
            f"Estado        : {self._estado}",
            "Indicaciones principales:",
        ]
        lineas += [f"  {i}. {texto}" for i, texto in enumerate(self._indicaciones, 1)]
        return "\n".join(lineas)


# ----------------------------------------------------------------------
# Prioridad: realiza el cálculo de las HU7 y HU8
# ----------------------------------------------------------------------
class Prioridad:
    PUNTAJES = {"Baja": 1, "Media": 2, "Alta": 3}
    HORAS_ATENCION = {"Baja": 48, "Media": 24, "Alta": 8}

    def __init__(self, urgencia, impacto):
        if urgencia not in Prioridad.PUNTAJES or impacto not in Prioridad.PUNTAJES:
            raise ValueError("Urgencia e impacto deben ser Baja, Media o Alta")
        self._urgencia = urgencia
        self._impacto = impacto

    @property
    def urgencia(self):
        return self._urgencia

    @property
    def impacto(self):
        return self._impacto

    def calcular_puntaje(self):
        return Prioridad.PUNTAJES[self._urgencia] + Prioridad.PUNTAJES[self._impacto]

    def determinar_nivel(self):
        puntaje = self.calcular_puntaje()
        if puntaje <= 3:
            return "Baja"
        if puntaje <= 5:
            return "Media"
        return "Alta"

    def tiempo_estimado(self):
        return Prioridad.HORAS_ATENCION[self.determinar_nivel()]


# ----------------------------------------------------------------------
# Solicitud técnica
# ----------------------------------------------------------------------
class SolicitudTecnica:
    ESTADOS = ("Pendiente", "En atención", "Atendida", "Cancelada")
    TIPOS = ("Consulta de procedimiento", "Falla de equipo", "Seguridad", "Otro")

    def __init__(self, codigo, trabajador, descripcion, tipo, urgencia, impacto,
                 procedimiento=None, fecha=None):
        self._codigo = codigo
        self._trabajador = trabajador          # asociación con Trabajador
        self._descripcion = descripcion
        self._tipo = tipo
        self._prioridad = Prioridad(urgencia, impacto)  # composición
        self._procedimiento = procedimiento    # asociación opcional
        self._fecha = fecha or date.today()
        self._estado = "Pendiente"

    @property
    def codigo(self):
        return self._codigo

    @property
    def trabajador(self):
        return self._trabajador

    @property
    def estado(self):
        return self._estado

    @property
    def prioridad(self):
        return self._prioridad

    def actualizar_estado(self, nuevo_estado):
        if nuevo_estado not in SolicitudTecnica.ESTADOS:
            raise ValueError(f"Estado no válido: {nuevo_estado}")
        if self._estado in ("Atendida", "Cancelada"):
            raise ValueError(f"La solicitud ya está {self._estado} y no puede cambiar")
        self._estado = nuevo_estado

    def mostrar_detalle(self):
        p = self._prioridad
        proc = (f"{self._procedimiento.codigo} - {self._procedimiento.nombre}"
                if self._procedimiento else "Ninguno")
        return "\n".join([
            f"Código        : {self._codigo}",
            f"Trabajador    : {self._trabajador.nombre_completo()}",
            f"Área          : {self._trabajador.area}",
            f"Descripción   : {self._descripcion}",
            f"Tipo          : {self._tipo}",
            f"Procedimiento : {proc}",
            f"Fecha         : {self._fecha:%d/%m/%Y}",
            f"Urgencia      : {p.urgencia}   Impacto: {p.impacto}",
            f"Puntaje       : {p.calcular_puntaje()} -> Prioridad {p.determinar_nivel()}",
            f"Tiempo estim. : {p.tiempo_estimado()} horas",
            f"Estado        : {self._estado}",
        ])
