---
name: Reabrir un ticket
about: Implementar una nueva operación en la aplicación heredada
title: "Permitir reabrir tickets cerrados"
labels: ""
assignees: ""
---

## Solicitud

Añadir el comando `python -m helpdesk reopen ID --actor CUENTA`.
Si existe `docs/arquitectura.md`, úsalo para localizar el flujo de cierre
y compruébalo en el código actual.

## Criterios de aceptación

- La cuenta autora o una cuenta de soporte de la misma organización
  puede reabrir un ticket cerrado.
- Una cuenta sin acceso recibe el error de negocio que corresponda según las
  reglas existentes. Los tickets de otra organización se tratan como ausentes.
- Un ticket cerrado cambia a `OPEN`, limpia `closed_at` y conserva la persona
  asignada que figure en el registro.
- Se escribe exactamente un evento `reopened`, con actor y fecha UTC,
  en la misma transacción que el cambio de estado.
- Un intento sobre un ticket abierto o asignado devuelve un error de negocio
  y deja el estado y el historial iguales.
- Las pruebas existentes siguen pasando. Agregar pruebas de integración para
  quien creó el ticket, soporte de la misma organización, una cuenta de otra
  organización, otra cuenta solicitante de la misma organización y repetición.

## Verificación

Ejecutar `python -m unittest discover -s tests -v` y resumir el resultado
en el pull request. Mantener el esquema SQLite y el flujo existente de cierre.
