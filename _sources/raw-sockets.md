% author: David Villa
(chap:raw-sockets)=
# Sockets RAW


Los sockets más usados con diferencia son los TCP seguidos de los UDP. Sin
embargo, hay muchos otros tipos de socket. Este capítulo es una introducción muy práctica
a los «sockets RAW» [^1].

[^1]: Concepto a veces traducido como «conector directo».

El término «raw» [^2] en informática suele hacer referencia al acceso de bajo nivel a un
recurso o dispositivo, o al menos con menor intervención  terceros (normalmente el sistema
  operativo). Este tipo de acceso directo tiene tres implicaciones principales:

[^2]: El adjetivo «raw» (crudo) se utiliza como contraposición a «cooked» (cocinado), que
    se emplea cuando se ofrece un acceso con algún preprocesamiento o asistencia en la
    gestión de un recurso o dispositivo.

- Mayor flexibilidad, al no estar limitado por las reglas o normas que impongan las
  capas de alto nivel que ofrece el sistema operativo.

- Acceso privilegiado, debido precisamente a que dichas posibilidades tienen un
  impacto directo sobre la seguridad del sistema y la privacidad de sus usuarios.

- Menos soporte, ya que son precisamente las capas del sistema operativo que se dejan
  a un lado las que simplifican el manejo del recurso. El «modo RAW» conlleva un nivel de
  abstracción mucho menor y por tanto, más complejidad técnica.

Estas tres cuestiones se pueden aplicar casi a cualquier cosa que permita un acceso «raw»,
sea un periférico USB, una consola o, como en este caso, un socket.

Con los sockets `AF_INET:SOCK_STREAM` o `AF_INET:SOCK_DGRAM` no es posible acceder (para
leer o escribir) a las cabeceras de ninguno de los protocolos de TCP/IP de la capa de
transporte o inferior, ya sea IP, ICMP, ARP, TCP, etc. Esos sockets únicamente permiten
indicar cuál será la carga útil de los segmentos TCP o UDP y solo indirectamente se
puede influir en algunos de los campos de sus cabeceras:  puerto origen y destino y poco
más [^3].

[^3]: a menos que acudamos a llamadas al sistema como `setsockopt`.

En raras situaciones se necesita ofrecer servicios que implican a protocolos de capas 2 y
3, o a las cabeceras de tramas, paquetes y segmentos, que normalmente quedan fuera de la
vista del programador. Algunos programas que sí lo necesitan pueden ser `ping`,
`traceroute`, `arping` o un *sniffer* cualquiera. Entonces ¿cómo se hacen estos programas?
La respuesta, como podrás adivinar, pasa por los sockets RAW.


## Acceso privilegiado

Como se decía un poco más arriba, el uso de un socket RAW requiere de los privilegios
correspondientes, concretamente, se requieren permisos de superusuario. Solo el `root` o
un programa ejecutado con sus privilegios [^4] tendrá permiso para crear sockets RAW.

[^4]: bit SUID

Si tu interfaz de red es una tarjeta Ethernet, únicamente las tramas broadcast, multicast
o que vayan dirigidas específicamente a su dirección MAC serán capturadas y entregadas al
subsistema de red. Sin embargo, si pretendes utilizar un socket RAW, es muy probable que
te interese recibir todo el tráfico que llegue a la interfaz de red de tu computador, y no
sólo el mencionado. Para lograr eso es necesario activar el «modo promiscuo» de la
NIC. Eso se puede lograr con el comando `ip`:

```console
# ip link set eth0 promisc on
```

O bien con `ifconfig`:

```console
# ifconfig eth0 promisc
```

De modo análogo se puede saber si una interfaz está en modo promiscuo con:

```console
$ ip link show eth0
2: eth0: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 1500 qdisc \
         pfifo_fast state UP qlen 1000
    link/ether 00:1b:c2:32:71:32 brd ff:ff:ff:ff:ff:ff
```

Y el equivalente con `ifconfig`:

```console
$ /sbin/ifconfig eth0
eth0      Link encap:Ethernet  HWaddr 00:1e:c9:34:7e:92
          inet addr:192.168.2.4  Bcast:192.168.2.255  Mask:255.255.255.0
          inet6 addr: fe80::21e:c9ff:fe34:7e92/64 Scope:Link
          UP BROADCAST RUNNING PROMISC MULTICAST  MTU:1500  Metric:1
          RX packets:160791 errors:0 dropped:0 overruns:0 frame:0
          TX packets:121923 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:177101459 (168.8 MiB)  TX bytes:18361567 (17.5 MiB)
          Memory:fdfe0000-fe000000
```

## Tipos

Lo primero a tener en cuenta es que hay dos tipos básicos de socket raw, y que la decisión
de cuál utilizar depende totalmente del objetivo y requisitos de la aplicación que se
desea:

Familia AF_PACKET
:  Los sockets raw de la familia AF_PACKET son los de más bajo   nivel y permiten leer y
escribir cabeceras de protocolos de cualquier capa.

Familia AF_INET
: Los sockets raw AF_INET delegan al sistema operativo la
  construcción de las cabeceras de enlace y permiten una manipulación «compartida» de las
  cabeceras de red.


En las próximas secciones veremos en detalle la utilidad y funcionamiento de ambas
familias.


## Sockets AF_PACKET:SOCK_RAW

Son los sockets raw más flexibles y de más bajo nivel, y representan la elección obligada
si el objetivo es crear un *sniffer* o algo parecido. Precisamente el siguiente
listado es un *sniffer* extremadamente básico que imprime por consola las tramas
Ethernet/WiFi completas recibidas por cualquier interfaz y portando cualquier protocolo.

```{literalinclude} ./code/raw/sniff-all.py
---
name: lst:raw:sniff-all
language: python
linenos:
caption: |
  Sniffer básico con AF_PACKET:SOCK_RAW ::
  [`raw/sniff-all.py`](https://raw.githubusercontent.com/UCLM-ARCO/net-book-code/master/raw/sniff-all.py)
---
```

Y a continuación se muestra cómo ejecutar este programa, y su salida:

```console
$ sudo ./sniff-all.py
--
(b'\xff\xff\xff\xff\xff\xff\xa8\x92,\xce\xcd\xb3\x08\x06\x00\x01\x08\x00\x06\x04\x00\x01\xa8\x92,
\xce\xcd\xb3\xac\x13\xb0O\x00\x00\x00\x00\x00\x00\xac\x13\xb0\x01', ('eth0', 2054, 1, 1, '\xa8\x92,
\xce\xcd\xb3'))
```

Haciendo modificaciones mínimas a este programa es posible filtrar el tráfico en dos
aspectos:

Tipo de trama
: Es decir, el código que identifica el protocolo encapsulado como carga
  útil [^5]. Para ello se utiliza el tercer campo del constructor de `socket`.

La interfaz de red
: Se logra vinculando el socket a una interfaz de red concreta por medio del método
  `bind()`.

[^5]: http://www.iana.org/assignments/ethernet-numbers

El uso de ambos «filtros» queda demostrado en el siguiente programa, llamado
`sniff-arp.py`. Sólo muestra menajes ARP recibidos por la interfaz que se
indique como argumento:

```{literalinclude} ./code/raw/sniff-arp.py
---
name: lst:raw:sniff-arp
language: python
linenos:
caption: |
  Sniffer AF_PACKET:SOCK_RAW filtrando ARP ::
  [`raw/sniff-arp.py`](https://raw.githubusercontent.com/UCLM-ARCO/net-book-code/master/raw/sraw/sniff-arp.py)
---
```

Y el programa en acción:

```console
$ sudo ./sniff-arp.py wlan0
--
b'\xff\xff\xff\xff\xff\xffl>m\x84y\x1d\x08\x06\x00\x01\x08\x00\x06\x04\x00\x01l>m\x84y
\x1d\xa1C\x11<\x00\x00\x00\x00\x00\x00\xa1C\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00'
```

Si te fijas, es fácil identificar la cabecera Ethernet en esa secuencia de bytes. Aparecen
6 bytes `0xff`, que corresponden a la dirección broadcast de Ethernet; y más
adelante `0x0806`, que como hemos visto en el programa, corresponden al tipo de
payload ARP.

De este modo tan sencillo es posible realizar un *sniffer* completamente a medida de
las necesidades concretas. Pero todo esto sólo sirve para leer tramas. Ahora veremos cómo
enviar, lo que abre un interesante mundo de posibilidades.

Si quieres identificar el origen del paquete puedes utilizar el método `recvfrom()`
en lugar de `recv()`. En ese caso el valor de retorno es una tupla que incluye,
entre otras cosas, el nombre de la interfaz (p.ej «eth0») y la dirección MAC origen como
una secuencia de bytes.


### Construir y enviar tramas

El mismo socket creado en los ejemplos anteriores se puede utilizar para enviar
datos. Para sintetizar un paquete, es decir, construir cabeceras de acuerdo a las
especificaciones, se utiliza normalmente el módulo `struct` [^6].

[^6]: Consulte el capítulo {ref}`chap:codificacion` para más información sobre dicho
    módulo.

El siguiente listado envía una cabecera Ethernet cuyos campos son:

- Destino: FF:FF:FF:FF:FF:FF
- Origen: 00:01:02:03:04:05
- Protocolo: 0x0806 (ARP)


```{literalinclude} ./code/raw/send-wrong-eth.py
---
name: lst:raw:send-wrong-eth
language: python
linenos:
caption: |
  Enviando una trama Ethernet con AF_PACKET:SOCK_RAWW ::
  [`raw/send-wrong-eth.py`](https://raw.githubusercontent.com/UCLM-ARCO/net-book-code/master/raw/send-wrong-eth.py)
---
```

Si capturas esa trama con {wireshark` o `tshark` verás que aparece con un
«malformed packet», y con razón: es sólo una cabecera ¡no tiene carga útil!

```console
$ tshark -a duration:7 -n -f arp
Capturing on 'wlan0'
    1 0.000000000 00:01:02:03:04:05 → ff:ff:ff:ff:ff:ff ARP 14 [Malformed Packet]
```

Y eso lógicamente contradice todas las normas del protocolo Ethernet. Resumiendo, este
programa no sirve para nada, sólo para que veas que se puede construir y enviar lo que
quieras a la red, incluso aunque sea un completo sinsentido.


### Implementando un `arping`

Aunque hay muchas variantes, el programa `arping` envía una petición ARP
Request y espera la respuesta correspondiente. En esta sección veremos una implementación
que sirve para ilustrar el uso de los sockets raw de la familia `AF_PACKET`

#### Generando mensajes

El programa necesita enviar mensajes ARP Request, que irán encapsulados en tramas
Ethernet. Una forma de implementar esta tarea (llamada a veces «sintetizar paquetes») y
aprovechar la POO es escribir una clase por cada tipo de mensaje. Por tanto, la clase
para generar el mensaje ARP Request es algo tan sencillo como esto:

```python
class Ether:
    def __init__(self, hwsrc, hwdst):
        self.hwsrc = hwsrc
        self.hwdst = hwdst
        self.payload = None

    def set_payload(self, payload):
        self.payload = payload
        payload.frame = self

    def serialize(self):
        retval = struct.pack("!6s6sh", self.hwdst, self.hwsrc,
                             self.payload.proto) + self.payload.serialize()

        return retval + (60-len(retval)) * "\x00"
```

Lo único a destacar de la clase `Ether` es el método `serialize()` que se encarga de
generar la representación binaria de los datos que corresponden a la cabecera,
concretamente dirección MAC destino, MAC origen, protocolo (el que indique el payload) y a
continuación el payload propiamente dicho. Esos datos se empaquetan en binario gracias a
`struct.pack()` [^7] indicando que se trata de 2 secuencias de 6 bytes (`6s6s`) y un
entero de 16 bits (`h`). La última línea de ese método calcula y concatena el relleno
(*padding*) necesario para que la trama alcance el tamaño mínimo necesario de 60 bytes.

[^7]: Ver http://docs.python.org/library/struct.html\#format-characters

La clase para generar mensajes ARP Request es incluso más sencilla:

```python
class ArpRequest:
    proto = ETH_P_ARP

    def __init__(self, psrc, pdst):
        self.psrc = socket.inet_aton(psrc)
        self.pdst = socket.inet_aton(pdst)
        self.frame = None

    def serialize(self):
        return struct.pack("!HHbbH6s4s6s4s", 0x1, 0x0800, 6, 4, 1,
                           self.frame.hwsrc, self.psrc, "\x00",  self.pdst)
```

#### Leyendo mensajes

La otra funcionalidad importante del programa es reconocer los mensajes que se obtendrán
como respuesta si todo va bien. Se trata de discretizar el valor de cada campo
representándolo en un formato adecuado. Esa tarea se suele llamar «disección de
paquetes». Como en el caso anterior, una buena forma de hacer esto es delegar el
reconocimiento (*parsing*) de cada tipo de mensaje en una clase específica. Hace
falta una clase para reconocer tramas Ethernet y otra para reconocer mensajes ARP Reply.

La clase para reconocer tramas Ethernet puede ser algo tan sencillo como esto:

```python
class EtherDissector:
    def __init__(self, frame):
        try:
            (self.hwdst,
            self.hwsrc,
            self.proto) = struct.unpack("!6s6sh", frame[:14])
        except struct.error:
            raise DissectionError

        self.payload = frame[14:]
```

El constructor acepta por parámetro una secuencia de bytes, es decir, la trama tal como se
lee del socket. Los valores que «desempaqueta» con `struct` y que estarán
accesibles como atributos públicos son: dirección MAC destino, MAC origen, protocolo y
payload.

El disector del mensaje ARP Reply, llamado `ArpReplyDissector`, es también muy
sencillo:

```python
class ArpReplyDissector:
    def __init__(self, msg):
        self.msg = msg

        if struct.unpack("!H", self.msg[6:8])[0] != ARP_REPLY:
            raise DissectionError

        try:
            (self.hwsrc, self.psrc,
            self.hwdst, self.pdst) = struct.unpack("!6s4s6s4s", msg[8:28])
        except struct.error:
            raise DissectionError
```

El constructor de la clase acepta por parámetro una secuencia de bytes, que corresponden
con la carga útil de una trama. Como antes, los valores de todos los campos quedan
disponibles como atributos de la instancia. Si algún campo o formato no corresponde, el
constructor lanza la excepción `DissectionError`.


#### Programa principal

Solo queda escribir la función principal, la que realmente crea, lee y escribe en el
socket. Aparece en el siguiente listado:

```python
def main(ipsrc, ipdst, iface):
    print("Request: Who has {0}? Tell {1}".format(ipdst, ipsrc))

    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
                         socket.htons(ETH_P_ARP))
    sock.bind((iface, ETH_P_ARP))

    frame = Ether(sock.getsockname()[-1], BROADCAST)
    frame.set_payload(ArpRequest(ipsrc, ipdst))

    sock.send(frame.serialize())

    while 1:
        eth = EtherDissector(sock.recv(2048))

        try:
            arp_reply = ArpReplyDissector(eth.payload)
            if arp_reply.hwdst == frame.hwsrc:
                print("Reply:   {0} is at {1}".format(
                      ipdst, display_mac(arp_reply.hwsrc)))
                break
        except DissectionError:
            print(".")
```

La función `main()` acepta las direcciones IP del host origen y destino, y la
interfaz de red (línea 1). Primero crea y vincula el socket a la interfaz solicitada
(lineas 4-6). A continuación crea una trama Ethernet con destino *broadcast* y
origen la MAC de la interfaz (línea 8), y le fija como payload una instancia de
`ArpRequest`. El método `send()` envía la trama en su formato binario (línea
11).

El bucle `while` espera la respuesta. En cada iteración se lee y disecciona una
trama (línea 14). Si esa trama contiene un mensaje ARP Reply, es decir, si
`ArpReplyDissector` no lanza la excepción `DissectionError`, se comprueba
además que esa sea la respuesta ARP que se espera y no otra (línea 18). Si es así se
imprime la dirección IP del destino y la dirección MAC asociada a esa IP, que es el
objetivo final del programa (líneas 19-20). Puedes encontrar una versión ampliada en el
fichero `raw/arping.py`.


## Sockets AF_INET:SOCK_RAW

A pesar de la flexibilidad y potencia de los sockets AF_PACKET, no siempre son la mejor
elección ya que el programador debe parsear y generar el contenido de todas las cabeceras.
Eso puede ser bastante engorroso cuando entra en juego el cálculo de checksums u otros
datos no tan directos.

Los sockets AF_INET:SOCK_RAW pueden ser una buena alternativa si solo te interesa
«tocar» las cabeceras de transporte, dejando al sistema operativo todo el trabajo
relacionado con las de enlace, y opcionalmente las de red.


### Capturando mensajes

El siguiente programa imprime por consola todos los paquetes IP que contengan un segmento
UDP:

```{literalinclude} ./code/raw/sniff-udp.py
---
name: lst:raw:sniff-all
language: python
linenos:
caption: |
  Sniffer de mensajes UDP con AF_INET:SOCK_RAW ::
  [`raw/sniff-udp.py`](https://raw.githubusercontent.com/UCLM-ARCO/net-book-code/master/raw/sniff-udp.py)
---
```

La función `getprotobyname()` devuelve el número de protocolo [^8] a partir de
su nombre (linea 4). Es interesante destacar que el resultado del método `recv()`
es el paquete IP completo, incluyendo cabecera (línea 7).

[^8]: http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xml

Como en el caso de los socket AF_PACKET puedes identificar el origen del paquete (su
dirección IP) sin tener que parsear la cabecera IP. Para lograrlo utiliza el método
`recvfrom()` en lugar de `recv()`. En ese caso el valor de retorno es una
tupla con la forma (datos, dirección), teniendo en cuenta que la dirección es su vez una
tupla `(IP, 0)`.


### Enviando

Para enviar datos sobre este tipo de socket debes utilizar el método `sendto()`
indicando la dirección destino. El {numref}`lst:raw:send-udp` envía envía un segmento
UDP «sintético», pero válido, que contiene el texto «hello Inet».

```{literalinclude} ./code/raw/send-udp.py
---
name: lst:raw:send-udp
language: python
linenos:
caption: |
  Sniffer básico con AF_PACKET:SOCK_RAW ::
  [`raw/send-udp.py`](https://raw.githubusercontent.com/UCLM-ARCO/net-book-code/master/raw/send-udp.py)
---
```

Puedes comprobar su funcionamiento ejecutando un servidor UDP en el puerto 2000
gracias a `ncat`. En un terminal ejecuta:

```console
$ ncat -l -p 2000
```

Y en otro terminal, pero en la misma máquina, ejecuta:

```console
$ ./send-udp.py
```

Si todo ha ido bien, en el primer terminal debería aparecer el texto «Hello Inet».

### IP_HDRINCL

Como has podido comprobar en el ejemplo anterior, es posible enviar un segmento sin tener
que construir la cabecera IP, únicamente la UDP. Sin embargo, puede haber ocasiones en las
que el programador necesite «tocar» también la cabecera IP. Eso se consigue con la opción
IP_HDRINCL.

La ventaja respecto al socket AF_PACKET es doble: no hay que molestarse con la cabecera
de enlace, y además el SO puede rellenar por nosotros algunos de los campos más
latosos si así queremos (poniendo ceros en ellos). Esos campos son:

- El checksum.
- La dirección IP origen.
- El identificador del mensaje.
- El campo de longitud total.

Esta opción, como la gran mayoría, debe fijarse explícitamente después de crear el socket
por medio del método `setsockopt()`, tal como se indica:

```python
sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
```

Esto resulta muy útil cuando quieres utilizar el socket para enviar distintos protocolos,
y por tanto necesitas tener acceso al campo *proto*. Para poder hacer eso ha de crearse
un socket de un *protocolo* especial identificado como `IPPROTO_RAW`:

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
```

Aunque tiene un pequeño inconveniente: no se puede leer de este tipo de socket, tendrás
que crear un socket adicional para poder leer los mensajes entrantes.


## Ejercicios
% Estos ejercicios tienen más sentido en el capítulo de métricas

A continuación se propone una lista de pequeñas herramientas de captura que pueden ser
utilizadas para análisis, monitorización y validación de tráfico, y detección de
anomalías. Los programas resultantes deberían funcionar correctamente al menos en una
plataforma GNU/Linux.


  Para una red Ethernet, escriba un programa que cuente el número de tramas que
  aparecen en el enlace con la granularidad temporal indicada como parámetro (en
  minutos) y lo imprima en consola tal como se indica. La primera columna es el tiempo en
  segundos del inicio del intervalo y la segunda en el número de tramas que han aparecido
  en la red en dicho intervalo:

```console
$ ./frame-count.py 2
Slot size: 120s
  0:  12
120:  14
240: 150
Capture time: 281.2s
```

  Para una red Ethernet, escriba un programa que cuente el número de paquetes de cada
  protocolo (níveles red y transporte) durante el tiempo que esté en ejecución. Ejemplo de
  uso:

```console
$ ./package-type-count.py
Capture time: 123.4s
ARP:  50
IP:  500
UDP:  80
TCP: 420
```

  Para una red Ethernet, escriba un programa que calcule una estadística del tamaño de
  las tramas (en bytes) que aparecen en la red, con la granularidad indicada en
  bytes. Ejemplo de uso:

```console
$ ./frame-sizes.py 300
Capture time: 120.2s
  46 - 300: 340
 301 - 600:  62
 601 - 900:  10
 901 -1200  140
1201 -1500: 970
```

   Para una red Ethernet, escriba un programa que calcule una estadística de la
  utilización y lo exprese como porcentaje de la capacidad del enlace. Debe realizarse con
  la granularidad indicada (en minutos). Ejemplo de uso:

```console
$ ./utilization.py 2
Slot size: 120s
  0:  22%
120:  35%
240:   2%
Capture time: 341.2s
```

  Para una red Ethernet, escriba un programa que calcule la utilización (tamaño total
  de tramas Ethernet) y el throughput (considerando payload de segmentos UDP y
  TCP). Ejemplo de uso:

```console
$ ./bandwidth.py
Capture time: 380.6s
Utilization:  1280 Kbps
Throughput:    992 Kpbs
```

  Escriba un programa que calcule el *tiempo medio de inactividad* (Average Idle
  Time) de un enlace durante el tiempo de ejecución del programa.

  Escriba un programa que mida la utilización que un host hace de un enlace (dada su
  dirección MAC) durante el tiempo de ejecución del programa.

  Escribe un programa que capture tramas Ethernet de una interfaz indicada como
  argumento e imprima por pantalla las direcciones origen y destino, el campo tipo y
  tamaño del payload de cada trama que reciba.

  Escribe un programa que capture paquetes IP de una interfaz de red indicada
  como argumento e imprima en pantalla el valor de los campos más importantes de la
  cabecera en un formato adecuado.
