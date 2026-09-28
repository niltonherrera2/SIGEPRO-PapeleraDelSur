# SIGEPRO – Sistema de Gestión de Procedimientos y Solicitudes Técnicas

Trabajo final del curso **IS275 – Fundamentos de Programación 2** (UPC, NRC 2880).
Empresa: **Papelera del Sur S.A.**

## Integrantes

| Integrante | Rol / archivo a cargo |
|---|---|
| Walter Josué Soto Atuncar | Modelo de clases (`modelo.py`) |
| Edison Andrés Encarnacion Ramos | Clases gestoras (`gestores.py`) |
| Nilton Ángel Herrera Tarazona | Menús e inicio de sesión (`sistema.py`) |
| Jhonatan Miguel Lalangui Alama | Documentación y pruebas (`README.md`, `capturas/`) |

## Gestión del proyecto

- Tablero de Trello: https://trello.com/b/03DTboZM

## Descripción

Aplicación de consola en Python que permite:

- Registrar, buscar, listar, consultar y modificar procedimientos técnicos.
- Registrar y buscar trabajadores.
- Registrar solicitudes técnicas con **cálculo automático de prioridad**
  (urgencia + impacto: 2–3 baja, 4–5 media, 6 alta) y **tiempo estimado de atención**
  (48 h, 24 h u 8 h).
- Actualizar el estado de las solicitudes (Pendiente, En atención, Atendida, Cancelada).

## Estructura

```
modelo.py      Persona, Trabajador, Usuario, Procedimiento, Prioridad, SolicitudTecnica
gestores.py    GestorProcedimientos, GestorTrabajadores, GestorSolicitudes
sistema.py     Clase Sistema: login, menús y programa principal
capturas/      Diagrama de clases y pantallas de funcionamiento
```

## Cómo ejecutar

Requiere Python 3.10 o superior (sin librerías externas).

```
python sistema.py
```

Usuarios de prueba: `admin` / `admin123` y `encargado` / `enc123`.
