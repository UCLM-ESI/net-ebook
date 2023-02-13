# Chat UDP

En esta sesión de laboratorio vamos a realizar un ejemplo mínimo de programación con sockets en Python3.
Todo (o casi todo) lo que vamos a realizar en esta sesión se podría realizar utilizando herramientas de terminal como `ncat`,
pero el objetivo es dar unos primeros pasos con Python 3 y la utilización de la librería `socket` para realizar conexiones de red.

## ¿Por qué UDP?

Como ya os sonará de la asignatura Redes 1, en la **capa de transporte** de la pila TCP/IP existen 2 protocolos principales:
_Transport Control Protocol_, o TCP, y _User Datagram Protocol_, o UDP.

La principal similitud entre ambos protocolos es que ambos utilizan un número natural como direccionamiento: el puerto.
En ambos protocolos el valor del puerto puede ir desde 0 a 65536.

En cuanto a difrencias, el transporte realizado mediante TCP está orientado a conexión:
existen dentro del protocolo una serie de herramientas para comprobar que los mensajes que se envían son recibidos por el destinatario,
y herramientas para que si no se tiene esa confirmación, se reenvíe el paquete.

En cuanto a UDP, **no está orientado a conexión**, no dispone de herramientas para comprobar que un mensaje ha sido recibido y entregado al destinatario,
ni siquiera sabemos si el destinatario está o no escuchando en su puerto.

En esta sesión vamos a utilizar UDP por su simplicidad para una primera aproximación al uso de sockets.

## Hello world

En éste primer ejemplo vamos a escribir dos programas que se comuniquen a través de UDP con las siguientes características:

- Un cliente que envíe un mensaje que contenga la palabra "hello".
- Un servidor que imprima el mensaje recibido por la pantalla en el terminal.

### El cliente

```{literalinclude} ./src/udp-chat/client1.py
---
language: python
---
```
[Descarga](https://joselsegura.github.io/redes2-lab/src/client1.py)

Para poder ejecutar el ejemplo anterior, copiarlo y pegarlo en un editor de texto, guardar el fichero y dadle permisos.

```bash
chmod u+x client1.py
./client.py
```

### El servidor

```{literalinclude} src/udp-chat/server1.py
---
language: python
---
```
[Descarga](https://joselsegura.github.io/redes2-lab/src/udp-chat/server1.py)

Copia y pega el código en un fichero nuevo y dale permisos de la misma manera:

```bash
chmod u+x server1.py
./server.py
```

## Hello world con respuesta

A continuación vamos a modificar el código anterior para que el servidor envíe una respuesta al cliente.
Además, el cliente mostrará dicha respuesta por su salida estándar:

### Servidor

```{literalinclude} src/udp-chat/server2.py
---
language: python
---
```
[Descarga](https://joselsegura.github.io/redes2-lab/src/server2.py)

### Cliente

```{literalinclude} src/udp-chat/client2.py
---
language: python
---
```
[Descarga](https://joselsegura.github.io/redes2-lab/src/client2.py)

## Entrada de usuario

Ahora vamos a escribir una pequeña aplicación de chat cliente-servidor. Deberá cumplir con lo siguiente:

- Comunicación bidireccional, pero no simultánea (el cliente inicia la conversación).
- La aplicación termina si cualquiera de los dos envía la cadena "bye".

### Pistas

- Para leer una cadena desde la entrada estándar desde un programa python usaremos la función `input()`.
- Para terminar un bucle podemos utilizar `break`.

## Simultáneos

Modificaremos el ejercicio anterior de manera que cualquiera de los pares sea capaz de enviar y recibir en cualquier momento
(no por turnos).

### Pistas

- Usaremos hilos
