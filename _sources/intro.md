# Prefacio

Las redes de comunicaciones, y especialmente Internet, se han convertido en una parte
esencial de nuestras vidas. Internet ha cambiado radicalmente nuestra forma de comprar,
viajar, hacer negocios, relacionarnos... Se trata de un cambio mucho más importante que
la invención de la imprenta o la revolución industrial, supone un nuevo concepto de
comunicación, un medio de difusión de información y conocimiento que no tiene
precedentes. Y es precisamente la comunicación lo que nos convierte en seres sociales, en humanos. Las redes han cambiado lo que somos y cómo vivimos, y nada parece indicar que se trate de una moda pasajera.

Todo ello es motivo suficiente para que cualquier persona (y en particular cualquier
técnico) se interese por el funcionamiento de las redes de computadores. Pocas cosas hoy
en día influyen tanto en nuestra vida cotidiana. Entender cómo es y cómo funciona la red
ayuda a tomar conciencia de sus posibilidades y oportunidades, pero también de sus
debilidades y riesgos.

Este libro es una introducción muy práctica a las redes de computadores, concretamente a
las basadas en la tecnología TCP/IP y por extensión a Internet. El enfoque que hemos
seguido en este libro es un tanto particular. Se basa en dos tecnologías muy concretas:

- El sistema operativo GNU.
- El lenguaje de programación Python.


## GNU

GNU es un sistema operativo estilo POSIX concebido y desarrollado bajo el concepto de
software libre. Esto tiene dos implicaciones muy importantes:

- GNU incorpora todas las ventajas prácticas y técnicas de la tradición de la
  familia de sistemas UNIX. La tecnología base de Internet fue desarrollada sobre
  UNIX}, concretamente BSD. Se podría decir que Internet forma parte del
  ADN de UNIX. GNU es heredero de todo ese legado.

- GNU está disponible para cualquier persona, en cualquier parte, sin ninguna
  limitación. Es *software libre* en estado puro, ideal para toda persona que quiera
  estudiar el funcionamiento de un sistema completo y productivo con todo detalle. Es
  tecnología *social* de la que aprender y con la que enseñar, que se puede
  compartir, mejorar y, por supuesto, crear industria y riqueza. La comunidad de usuarios de *GNU* y todas sus distribuciones derivadas también es uno de sus puntos
  fuertes.

El entorno de trabajo y herramientas que se refieren en el presente texto corresponden al sistema operativo Debian GNU/Linux [^1]. Por simplicidad y para un máximo
aprovechamiento te aconsejamos instalar esta distribución en tu computador porque este
será el entorno que se asume cuando se habla de configuración o comandos de sistema. Por
supuesto, es posible usar cualquiera de las abundantes distribuciones basadas en \ac{GNU} puede ser perfectamente válida para la realización de los ejemplos y ejercicios prácticos propuestos. También se asume que tu computador cuenta al menos con una interfaz de red Ethernet o WiFi convenientemente configurada y que proporciona acceso a Internet sin restricciones relevantes.

[^1]: https://www.debian.org


## Python

Python es un lenguaje de programación interpretado, dinámico y orientado a objetos. A
pesar de ser un lenguaje muy completo y potente, su aprendizaje resulta sorprendentemente sencillo. Permite, incluso a un programador novato, ser productivo en muy poco tiempo, en comparación con otros lenguajes como Java, C++, C#, etc.

La librería estándar de Python respeta los nombres y conceptos básicos del API de
programación de C de POSIX lo que resulta muy útil para encontrar documentación y
sobre todo facilita la *traducción* entre ambos lenguajes. Es muy útil como lenguaje
de prototipado rápido, incluso aunque la versión final de la aplicación se vaya a
implementar en otro lenguaje.

Python también es software libre, lo que significa que está disponible para cualquiera en cualquier plataforma. Está respaldado por una gran comunidad de usuarios y desarrolladores y suele ser fácil encontrar ayuda incluso en temas muy específicos.


## Contenido de los capítulos


Shell
: Una introducción extremadamente práctica al interprete de comandos.

Conectividad
: Herramientas (y sus fundamentos) para la comprobación de conectividad de red de un
computador.


## Ejercicios

A lo largo del texto se proponen ejercicios, identificados en la forma «[E`n`]», siendo
`n` un número creciente. La realización de estos ejercicios, normalmente muy prácticos, es importante para una adecuada asimilación de los conceptos y manejo de las herramientas.


## Sobre los ejemplos

Todos los ejemplos que aparecen en este documento (y algunos otros) están disponibles para descarga a través del repositorio git en https://github.com/UCLM-ARCO/net-book-code.git.
Aunque es posible descargar estos ficheros individualmente o como un archivo comprimido,
se aconseja utilizar el sistema de control de versiones
[git](https://git-scm.com).

Si encuentra alguna errata u omisión es los programas de ejemplo, por favor, utilice la
herramienta de [gestión de incidencias](https://github.com/UCLM-ARCO/net-book-code/issues)(*issue tracker*) accesible desde para notificarlo a sus autores.


## Sobre este documento

Este documento está tipografiado con jupyter-book en un sistema Debian GNU/Linux. Las
figuras y la mayoría de los diagramas están realizados con `inkscape`.

Los fuentes de este documento también se encuentran en un repositorio git
https://github.com/UCLM-ESI/net-book. Si quiere colaborar activamente en su desarrollo o
mejora póngase en contacto con los autores.

Al igual que los ejemplos, también existe una herramienta de gestión de incidencias
(pública) en la que puede notificar problemas o errores de cualquier tipo que haya
detectado en el documento.


```{tableofcontents}
```
