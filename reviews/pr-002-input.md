# PR #2 — feat: add payment controller

## Origen (output Agente de Desarrollo)

- Tarea: TASK-003
- Rama origen: feature/test-code-review
- Rama destino: develop
- Tipo de cambio: módulo nuevo

## PRD

Crear un endpoint de pagos que permita registrar cobros de membresías.
El controller debe seguir el patrón existente de MemberController.
Debe integrarse con el sistema de autenticación JWT ya configurado.

## Definition of Done definida por Fase 3

- [ ] Controller creado en src/main/java/com/gym_management/system/controller/
- [ ] Endpoint POST /api/payments/process
- [ ] Endpoint GET /api/payments/all
- [ ] Validaciones en los parámetros de entrada
- [ ] Autenticación JWT aplicada
- [ ] Sin lógica de negocio en el Controller
- [ ] Test unitario cubriendo happy path y caso de error

## Notas del agente de desarrollo

Módulo nuevo, no modifica código existente.
Prestar especial atención a la seguridad del endpoint de pagos.
