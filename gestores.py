"""
Clases gestoras: administran las colecciones de objetos del modelo
(registro, búsqueda, listado y consulta).
"""
from modelo import SolicitudTecnica


class GestorProcedimientos:
    def __init__(self):
        self._procedimientos = []

    def registrar(self, procedimiento):
        if not procedimiento.codigo or not procedimiento.nombre:
            raise ValueError("El código y el nombre son obligatorios")
        if self.buscar_por_codigo(procedimiento.codigo):
            raise ValueError(f"Ya existe un procedimiento con código {procedimiento.codigo}")
        self._procedimientos.append(procedimiento)

    def buscar_por_codigo(self, codigo):
        for p in self._procedimientos:
            if p.codigo.lower() == codigo.lower():
                return p
        return None

    def buscar(self, texto):
        return [p for p in self._procedimientos if p.coincide(texto)]

    def listar(self):
        return list(self._procedimientos)

    def cantidad(self):
        return len(self._procedimientos)


class GestorTrabajadores:
    def __init__(self):
        self._trabajadores = []

    def registrar(self, trabajador):
        if not trabajador.codigo or not trabajador.nombre:
            raise ValueError("El código y el nombre son obligatorios")
        if self.buscar_por_codigo(trabajador.codigo):
            raise ValueError(f"Ya existe un trabajador con código {trabajador.codigo}")
        self._trabajadores.append(trabajador)

    def buscar_por_codigo(self, codigo):
        for t in self._trabajadores:
            if t.codigo.lower() == codigo.lower():
                return t
        return None

    def buscar(self, texto):
        texto = texto.lower()
        return [t for t in self._trabajadores
                if texto in t.codigo.lower() or texto in t.nombre_completo().lower()]

    def listar(self):
        return list(self._trabajadores)


class GestorSolicitudes:
    def __init__(self):
        self._solicitudes = []
        self._correlativo = 0

    def generar_codigo(self):
        self._correlativo += 1
        return f"SOL-{self._correlativo:03d}"

    def registrar(self, trabajador, descripcion, tipo, urgencia, impacto,
                  procedimiento=None):
        if not descripcion:
            raise ValueError("La descripción del problema es obligatoria")
        solicitud = SolicitudTecnica(self.generar_codigo(), trabajador, descripcion,
                                     tipo, urgencia, impacto, procedimiento)
        self._solicitudes.append(solicitud)
        return solicitud

    def buscar_por_codigo(self, codigo):
        for s in self._solicitudes:
            if s.codigo.lower() == codigo.lower():
                return s
        return None

    def buscar(self, texto):
        """Busca por código de solicitud o por nombre/código del trabajador."""
        texto = texto.lower()
        return [s for s in self._solicitudes
                if texto in s.codigo.lower()
                or texto in s.trabajador.codigo.lower()
                or texto in s.trabajador.nombre_completo().lower()]

    def listar(self):
        return list(self._solicitudes)
