(chap:redes)=
# Redes y protocolos


Internet tiene un nombre perfectamente autodefinido. Internet es una inter-red
(**inter-net**work), es decir, un sistema formado por la interconexión de miles de
redes de computadores.

Una red de computadores es simplemente un conjunto de computadores autónomos [^1]
conectados entre sí de modo que puedan compartir recursos (datos o dispositivos.). Todos
los computadores de una red concreta utilizan una misma tecnología de comunicaciones
(p.ej: WiFi). Denominamos a esto una LAN y tiene utilidad por si misma aunque esté
aislada, por ejemplo puede ser la red de control de una planta de fabricación industrial.
Coloquialmente muchas veces también llamamos simplemente «red» a cualquier inter-red y
también a la propia Internet.

[^1]: que pueden realizar tareas por si mismos

<!-- ## En este capítulo

Al terminar este capítulo el lector debería ser capaz de responder satisfactoriamente a
las siguientes cuestiones:

\begin{itemize}
- Qué es una red de computadores.

- Qué es y cuál es la utilidad de los modelos de referencia OSI}, TCP/IP} e
  híbrido.
\end{itemize} -->


## Tecnología Internet

Como en tantos otros campos, ocurre que no existe una sola tecnología «perfecta» para
resolver todos los problemas. En nuestro caso, no hay una tecnología universal para
implementar una LAN, hay cientos. Por tanto, el problema clave que resuelve Internet (en
concreto IP [^2]), es interconectar redes heterogéneas ---con tecnologías potencialmente
incompatibles.

[^2]: Por supuesto no es el único modo, pero es el que abordamos en este texto.

IP, que significa literalmente **protocolo de inter-red**, lo logra mediante tres elementos:

- Un protocolo y un formato de mensaje universal (el protocolo y el paquete IP)
que se debe utilizar en todo aquel computador y dispositivo de interconexión (*router*)
que se quiera integrar en la inter-red, independientemente de su tecnología LAN. No
hablamos de substituir «su protocolo» por IP sino de que lo encapsulen (ver FIXME).

- Un esquema de direccionamiento global (las direcciones IP). Para que un
computador tenga la capacidad de enviar paquetes IP a cualquier otro ---en cualquier
parte--- debe disponer de una dirección IP adecuada.

- Un dispositivo capaz de reenviar paquetes IP entre redes dos o más redes y
hacerlos llegar a su destino. Hablamos de los routers o pasarelas IP
(*gateways*).


Esto resuelve un problema importante: llevar paquetes de datos desde un computador a
cualquier otro, solo conociendo la dirección IP del destino, sin importar dónde esté
o la tecnología que utilice para conectarse a **su** red.

Pero hay muchos otros problemas...

Son **las aplicaciones** las que realmente necesitan compartir información. Las
aplicaciones que utilizan la red (la inmensa mayoría hoy día) requieren un modo de enviar
datos de su dominio específico a otra aplicación, o dicho con más precisión, a otro
componente de la misma aplicación que se está ejecutando en otro computador. Llamamos a
esto «aplicaciones distribuidas».

La red, o más concretamente, el sistema operativo [^3], debe ofrecer una forma de que dos
procesos ejecutándose en computadores cualesquiera puedan «direccionarse» el uno al otro,
es decir, que puedan identificar unívocamente a otro proceso que se ejecuta en un
computador remoto accesible a través de la red [^4]. Esto se logra mediante
la combinación de dos datos: la dirección IP, que identifica el computador remoto, y el
puerto, que identifica un proceso dentro de ese computador.

[^3]: Y más concretamente aún, el subsistema de red del SO.
[^4]: El direccionamiento de procesos dentro de un computador se denomina «multiplexación».

Además, muchas aplicaciones necesitan garantías de que estos mensajes llegan correctamente
a su destino, sin cambios (respetando la integridad), sin partes ausentes (omisiones),
recibidos en el mismo orden en el que se enviaron, asegurando la privacidad, sin saturar
al receptor y evitando congestionar la red.

La mayoría de estos problemas los resuelven los **protocolos de transporte**. En el
caso de Internet estos protocolos son:

TCP
: Proporciona un flujo (*stream*) de datos entre dos procesos de forma fiable y
ordenada.

UDP
: Ofrece un servicio de entrega de datagramas (mensajes independientes) entre dos
procesos, pero sin ninguna garantía.

TLS
: Sin entrar en detalle, ofrece mecanismos para cifrado de mensajes y permite asegurar
la legitimidad del proceso remoto.

Estos tres protocolos son genéricos puesto que se pueden aplicar sobre cualquier carga
útil (*payload*), es decir, son independientes del contenido de los mensajes que
las aplicaciones necesitan enviar.

El formato específico de los datos que utiliza cada aplicación también está definido por
protocolos ---llamados **protocolos de aplicación**-- aunque debemos entender el concepto
«aplicación» de un sentido muy amplio. Por ejemplo, todo el software relacionado con la
web utilizan el protocolo de aplicación HTTP. Al contrario de lo que sucede con los
protocolos de inter-red y transporte, hay miles de protocolos de aplicación, la mayoría de
ellos privativos y secretos. Sin embargo, hay unos cuantos muy importantes que son
públicos, bien documentados y de uso común. Algunos de estos son DNS,
SMTP/IMAP/POP, FTP, SSH o el ya mencionado HTTP.


## Pila de protocolos

Como vemos, hay varios problemas bastante diferentes a resolver para conseguir nuestro
objetivo: que dos procesos puedan intercambiar mensajes. Y también vemos que hay varios
tipos de protocolos ---red, transporte, aplicación, etc.--- que abordan distintos
problemas a distintos niveles.

Para manejar más cómodamente esos problemas y sus soluciones, el estudio, diseño,
especificación e implementación de todo lo relacionado con las redes, se suele organizar
todo ello en capas. Por eso, los distintos protocolos, correspondientes a cada
una de las capas forman una **pila de protocolos** (*protocol stack*). Se llama
así porque está formada por un conjunto de protocolos «apilados» siguiendo las directrices
del modelo correspondiente. Es sencillo entender que todo esto en realidad no es más que
una conveniencia de abstracción para facilitar su organización y comprensión.


(sec:OSI)=
## Modelo OSI

El modelo de referencia OSI ---definido por la ISO--- está pensado para
aplicarse a cualquier tecnología de comunicaciones. El modelo describe las interfaces,
protocolos y servicios que proporciona cada una de las siete capas que lo componen:
aplicación, presentación, sesión, transporte, red, enlace y física. Como se ha dicho, cada
capa se centra en resolver un conjunto de problemas específicos. Cada capa ofrece
servicios a la capa inmediatamente superior y demanda servicios de la inmediatamente
inferior. De ese modo se consigue aislar y desacoplar sus funciones simplificando cada
elemento, haciéndolo reemplazable.

A continuación se explica brevemente el objetivo de cada capa:

1. **Física**.
Define las características eléctricas, mecánicas y temporales requeridas en una
tecnología de comunicación de datos particular. Ejemplo: específica las dimensiones de los
conectores, el voltaje que puede haber en cada pin y su significado, el tamaño y forma de
las antenas, las frecuencias que utiliza un emisor, etc.

1. **Enlace**.
Se ocupa del intercambio de mensajes entre nodos vecinos, (directamente conectados).
Cuando se usa un medio de difusión, es decir, varios nodos comparten un medio físico,
suele proporcionar un sistema de *direccionamiento físico*.

1. **Red**.
: Proporciona soporte para comunicaciones *extremo a extremo*, es decir, que puede
implicar dispositivos intermediarios. Permite enviar mensajes individuales de tamaño
variable y define un sistema de *direccionamiento lógico*. Una de sus funciones más
importantes en la capacidad de interconectar redes de tecnología distinta

1. **Transporte**.
: Proporciona un canal de comunicación libre de errores entre formando inter-redes.
procesos o usuarios finales. Incluye un mecanismo de multiplexación y un sistema de
direccionamiento de procesos.

1. **Sesión**.
: Permite crear sesiones entre hosts remotos y se ocupa de la sincronización.

1. **Presentación**.
: Define la representación canónica de los datos (reglas de codificación) y su semántica
  asociada.

1. **Aplicación**.
: Incluye protocolos específicos de cada aplicación.



## Modelo TCP/IP

El modelo de referencia TCP/IP se definió años después de las primeras implementaciones y
trata de formalizar y estandarizar para garantizar interoperabilidad entre los distintos
fabricantes. Este modelo define únicamente cuatro capas:

1. **Host a red**.
Asume que existen los mecanismos necesarios para conseguir que un paquete IP pueda ser
enviado desde un computador a sus vecinos, es decir, otros computadores conectados al
mismo enlace. En realidad no aborda la problemática específica que ello implica,
simplemente da por hecho que es un problema resuelto.

1. **Inter-red**.
Proporciona los mecanismos de interconexión de redes y
encaminamiento de paquetes. Define el protocolo IP, que proporciona un servicio de
entrega sin conexión.

1. **Trasporte**. Define dos protocolos de transporte: TCP, que proporciona un
servicio confiable y orientado a conexión y UDP, que únicamente proporciona
multiplexación y detección muy básica de errores.

1. **Aplicación**.
Incluye los protocolos para los servicios comunes, tales como: DNS, SMTP, HTTP, FTP, etc.

Una aclaración necesaria es que las siglas TCP/IP (escritas así con la '/') no se refieren
exclusivamente al par de protocolos TCP e IP, sino a la pila completa que se muestra en la
figura y todas los implicaciones funcionales que conlleva.


## Modelo híbrido

Por último, el modelo híbrido es una mezcla de los modelos OSI y TCP/IP
eliminando «lo que sobra» (las capas de presentación y sesión son aplicables a
relativamente pocas aplicaciones) y añadiendo «lo que falta» (la capa de enlace es
decisiva para comprender el funcionamiento de la arquitectura de red).

La figura~\ref{fig:modelos-ref} muestra la correspondencia entre los tres modelos
anteriores:
%
\begin{figure}[htbp]
  \begin{center}
    \includegraphics[width=0.9\linewidth]{modelos-referencia.pdf}
  \end{center}
  \caption{Correspondencia entre los diferentes modelos de referencia}
  \hyperlabel{fig:modelos-ref}
\end{figure}


(sec:protos)=
## Protocolos

Todo protocolo define las pautas y normas específicas que deben aplicar las entidades
participantes para efectuar una comunicación correcta [^5]. Todo protocolo debe definir
tres aspectos clave: sintaxis, semántica y secuenciación, es decir, cuestiones como
formato y tamaño de los mensajes, los rangos de valores admisibles, el tipo y significado
de cada campo, condiciones de error, patrones válidos de intercambio de mensajes, etc.

[^5]: Similar a la acepción de la palabra «protocolo» que se aplica en las relaciones
diplomáticas o formales.

En los siguientes capítulos se abordan algunos de los protocolos más importantes de
Internet:

% \FIXME{Lista de protocolos con referencias a secciones}
