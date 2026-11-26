# Mesa de ayuda legacy

Aplicación de terminal para un laboratorio de agentes de código. Usa Python
3.12, SQLite y cuentas ficticias. La versión de partida permite crear, asignar,
cerrar y consultar tickets.

## Arranque

Abre la carpeta del proyecto en VS Code. Ejecuta desde su raíz:

```sh
python -m helpdesk init-demo
python -m helpdesk list --actor alice
python -m helpdesk history 2 --actor alice
python -m unittest discover -s tests -v
```

En Windows, si tu instalación usa el lanzador `py`, reemplaza `python` por
`py -3.12`. En macOS o Linux, puede que el ejecutable se llame `python3`.

| Cuenta | Organización | Rol |
| --- | --- | --- |
| `alice` | `acme` | Solicitante y autora de los tickets 1 y 2 |
| `bob` | `acme` | Solicitante |
| `sofia` | `acme` | Soporte |
| `ana` | `otra` | Soporte |

El ticket 2 ya está cerrado en la base de demostración. La opción `--actor`
representa una sesión simulada de la práctica. Para empezar con otra base,
coloca `--db practica.sqlite3` antes del subcomando.

## Trabajo en GitHub

Las plantillas de Issues definen el diagnóstico inicial y la nueva
funcionalidad. El agente **Explorador legacy** se configura en
`.github/agents/`. El workflow **CI mesa de ayuda** ejecuta las pruebas
y publica una lista de archivos versionados.

El repositorio base tiene cinco pruebas. Usa ramas separadas para el mapa de
arquitectura y para la reapertura.
