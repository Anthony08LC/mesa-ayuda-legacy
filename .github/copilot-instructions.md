# Mesa de ayuda del laboratorio

- Usa Python 3.12 y la biblioteca estándar. Ejecuta
  `python -m unittest discover -s tests -v` desde la raíz.
- La aplicación se ejecuta con `python -m helpdesk`. Las pruebas de integración
  usan bases SQLite temporales.
- Las cuentas incluidas son ficticias. La opción `--actor` simula una sesión
  para el aula. Conserva la validación por organización y por rol.
- Usa parámetros SQL para los valores. Reutiliza las reglas existentes de
  acceso, y guarda la mutación de estado y su historial en una transacción.
- Sigue el alcance y los criterios del issue. Antes de editar, identifica
  los puntos de entrada y las pruebas relacionadas. Al terminar, informa
  los archivos cambiados, los resultados y las dudas que sigan abiertas.
