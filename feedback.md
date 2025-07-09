El TP en general está muy bien pero tiene roto el código en la parte del método de la potencia. Si bien eso no afecta tanto a los 
resultados y seguramente no cambien demasiado sus conclusiones, es importante que lo arreglen y que vuelvan a generar 
los resultados y ajusten lo que escribieron a eso para reentregar. Abajo les dejo las cosas más importantes a retocar y 
en el código y el notebook es fui dejando comentarios que empiezan con "VALEN:" y "#>".

Si tienen consultas para la reentrega, la semana que viene voy a estar por el discord para responder cosas. Voy a tratar 
de estar disponible el martes y seguro el miércoles. Los otros días no aseguro nada. 
Si quieren me pueden arrobar por discord para ver si estoy y nos metemos en una sala para ver lo que necesiten.
Por si no están en el discord de la materia, este es el link (vence en una semana): https://discord.gg/6RDuxRPX

Cosas importantes:
- calcula_lambda no calcula un autovalor a partir de un autovector, calcula el $\Lambda$ del laplaciano. Por eso están 
calculando cualquier cosa en el método de la potencia. También están shifteando dos veces en metpotI2 (porque shiftean 
primero una vez ahí y otra en metpotI). Hay algunos bugs más que les marqué en el código, recomendaría reescribir 
esas funciónes (las cuatro de metpot) con cuidado y aprovechando las funciones que van haciendo.
- Expliquen que es un vector de Fiedler y de donde sacaron eso.
- Hablen un poco más en el 4.

Detalles:
- En el 2b les faltó el último pedacito.
- Hay algunas cosas en el 5 que no están bien y deberían revisar, principalmente sobre el TP1. Les dejé comentarios.