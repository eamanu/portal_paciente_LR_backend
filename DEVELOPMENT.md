# Introducción

Este documento tiene como objetivo establecer la metodología que se utilizará
en el desarrollo del backend del Portal de Pacientes del La Rioja. De esta manera
se podrá realizar las tareas de manera más ordenada y coordinada. 


# Ciclo de desarrollo

Cada bug o feature, que se vaya a a resolver y/o desarrollar, debe comenzar estar
registrado en una tarjeta de Trello.

Los pasos o camino que debe seguir una tarjeta es la siguiente:

  1. Sprint Backlog: Las tarjetas que se enecuentra en este estado, signfica que están
  abiertas, y listas para que se comience su desarrollo.
  2. En Proceso: Cuando se comienza a trabajar en la tarjeta, se debe mover la 
  tarjeta a este estado. Este, significa que se está trabajando en la tarea, y todavía
  no está lista para una revisión o tests. Es para denotar que "estoy trabajando en esto".
  3. In Review: Signfica que el código o la tarea está en revisión. La tarea dejó de estar
  "en proceso"  para estar listo, y necesita la revisión de un par. La tarea acá puede estar
  aprobada y pasar "In testing" o puede necesitar cambios grandes y necesitar un gran volumen
  de trabajo, por lo que la tarea debe pasar a "En proceso". Observaciones pequeñas en el
  código o tarea no requiere más de 8 horas de trabajo, se puede mantener en "in review".
  4. In Testing: Esto signfica que el código o tarea pasó correctamente la revisión de par, y
  ahora necesita ser testado. Una vez que finaliza la revisión y está todo ok, se mueve a
  "Sprint Completados". Si no está ok, es decir falla algún tests, se mueve a "En proceso".
  5. Sprint Completados: Fin de la tarea. Aca se mueven todas las tarjetas que ya están
  finalizada en el sprint actual.

Cuando se asigna una tarjeta de Trello a una persona, esta persona es responsable de mantener
la tarjeta actualizada y en su estado correcto. Se pide mantener siempre actualizada con
comentarios explicando los avances o problemas que se tiene en la tarjeta, de esta manera
el equipo compleo sabe si hay un problema que necesita atención.

# Backend

El backend está escrito en Python 3.9. Existe muchos recursos de Python en internet que se puede
consultar. La Documentación oficial de Python se la puede encontrar acá [0] y acá en español [1].

Se utiliza el framework FastAPI [2] en el desarrollo.

## Commits

Se recomiendo que cada commit sea atómico, y lo más consiso posible. En el mensaje del commit
siempre se debe colocar le mayor detalle posible de lo que se está agregando.

Como es un proyecto que recien está comenzando es dificil genera commits pequeños, pero en la
medida que se pueda, lo haremos. Algo de recursos para leer sobre commits [3][4][5].




[0] https://docs.python.org/3.9/
[1] https://docs.python.org/es/3.9/
[2] https://fastapi.tiangolo.com
[3] https://www.freecodecamp.org/news/writing-good-commit-messages-a-practical-guide/
[4] https://www.conventionalcommits.org/en/v1.0.0/
[5] https://www.linkedin.com/pulse/how-write-good-commit-messages-yuvraj-singh-rajawat/
