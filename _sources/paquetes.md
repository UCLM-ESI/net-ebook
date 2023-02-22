# Paquetes

Muchas distribuciones de GNU/Linux utilizan paquetes para distribuir sus programas. Un
paquete no es más que una colección de ficheros (normalmente comprimidos) estructurados
para ser colocados en rutas concretas dentro del sistema de ficheros cuando se instalan.

En Debian GNU/Linux o Ubuntu, estos paquetes son ficheros con extensión `.deb`.
Si descargas uno de estos ficheros directamente, puedes instalarlo con el comando `dpkg`:

```shell
david@amy:~$ ls
gedit_3.38.1-1_amd64.deb
david@amy:~$ sudo dpkg -i gedit_3.38.1-1_amd64.deb
(Leyendo la base de datos ... 497325 ficheros o directorios instalados actualmente.)
Preparando para desempaquetar gedit_3.38.1-1_amd64.deb ...
Desempaquetando gedit (3.38.1-1) sobre (3.38.1-1) ...
Configurando gedit (3.38.1-1) ...
```

Una carácteristica muy importante de estos paquetes es que tienen *dependencias*, es
decir, para que el programa que instalas pueda funcionar necesita que otros paquetes
concretos estén instalados previamente. Puedes ver las dependencias (y otra mucha información)
sobre un paquete con:

```shell
david@amy:~$ apt-cache show gedit
Package: gedit
Version: 3.38.1-1
Installed-Size: 1738
Maintainer: Debian GNOME Maintainers <pkg-gnome-maintainers@lists.alioth.debian.org>
Architecture: amd64
Depends: gedit-common (<< 3.39), gedit-common (>= 3.38), gir1.2-glib-2.0, gir1.2-gtk-3.0
(>= 3.22), gir1.2-gtksource-4, gir1.2-pango-1.0, gir1.2-peas-1.0,
gsettings-desktop-schemas, iso-codes, python3-gi (>= 3.0), python3-gi-cairo (>= 3.0),
[...]
```

Como se puede ver, para muchos de ellos se indica que deben corresponder a cierta versión.
En ese ejemplo, puedes ver que se requiere una versión del paquete `python3-gi`
que sea mayor o igual a la 3.0.

Obviamente encontrar, descargar e instalar manualmente (con `dpkg`) todos esos paquetes (y
sus respectivas dependencias) es una tarea terriblemente pesada. Afortunadamente hay otro
modo de hacerlo.

El programa `apt` (o `apt-get`) puede determinar automática y recursivamente las
dependencias de un paquete, descargarlos e instalarlos en el orden correcto.

```shell
david@amy:~$ sudo apt install gedit
Leyendo lista de paquetes... Hecho
Creando árbol de dependencias... Hecho
Leyendo la información de estado... Hecho
Se instalarán los siguientes paquetes adicionales:
  gedit-common gir1.2-gtksource-4 libamtk-5-0 libamtk-5-common libtepl-5-0
Paquetes sugeridos:
  gedit-plugins
Se instalarán los siguientes paquetes NUEVOS:
  gedit gedit-common gir1.2-gtksource-4 libamtk-5-0 libamtk-5-common libtepl-5-0
0 actualizados, 6 nuevos se instalarán, 0 para eliminar y 172 no actualizados.
Se necesita descargar 59,0 kB/2.146 kB de archivos.
Se utilizarán 15,5 MB de espacio de disco adicional después de esta operación.
¿Desea continuar? [S/n]
```


## Repositorios de paquetes

La pregunta obvia es «¿Cómo sabe `apt` de dónde descargar todos esos paquetes?». Las
distribuciones proporcionan servidores (normalmente web o FTP) dónde dejan publicamente accesibles
los ficheros `.deb`. Por ejemplo, en el caso de Debian en
https://ftp.debian.org/debian/, del cual existen cientos de «copias espejo»
(*mirrors*), normalmente una por país, como https://ftp.es.debian.org/debian/.

En estos repositorios, los paquetes se organizan en «releases» (o versiones) [^9] . En el
caso de Debian, estas «releases» tienen un número de versión y un nombre asociado. Por
ejemplo, Debian 10 lleva el nombre «buster».

[^9]: https://www.debian.org/releases/

De este modo, si queremos instalar (o actualizar) a una *release*, debemos indicárselo a
`apt` mediante el fichero `/etc/apt/sources.list`:

```text
deb http://deb.debian.org/debian/ buster main contrib non-free
```

Esta línea en concreto dice que queremos poder instalar paquetes oficiales mantenidos por
Debian (*main*), contribuciones de terceros (*contrib*) y software con licencias no
libres (*non-free*).

Este fichero puede contener muchos repositorios, y también se pueden crear otros ficheros
con extensión `.list` dentro del directorio `/etc/apt/sources.list.d` que tienen el
mismo tipo de contenido.

Para saber qué paquetes (y versiones) están disponibles en los repositorios configurados,
`apt` debe descargar una especie de índices que se encuentran allí mismo. Para eso
debemos ejecutar:

```shell
david@amy:~$ sudo apt update
```

Esto debemos hacerlo regularmente [^10] porque el contenido de los repositorios cambia
y regulamente se añaden nuevos paquetes o versiones.

[^10]: De hecho las distribuciones actuales tienen sistemas que lo hacen de forma
    autómática.

En concreto en Debian hay siempre tres versiones activas:

stable
: Es la última versión publicada y su contenido no debería cambiar. Esta
corresponde con «buster» en el momento de escribir este documento.

testing
: Contiene los paquetes que se están preparando para una futura versión
estable y por tanto, cambia continuamente. En este momento se denomina «bullseye» y ese
será el nombre que tendrá la siguiente versión estable.

unstable
: Que tiene paquetes recién incorporados, experimentales o que tienen algunos
problemas importantes para ser incluidos en una futura versión. Esta versión siempre se
llama «sid».

Por cuestiones de seguridad es importante que se puedan actualizar paquetes en los que se
han descubierto vulnerabilidades o problemas graves, incluso aunque correspondan a una
versión estable. Por eso, es conveniente tener los siguientes repositorios en el fichero
`/etc/apt/sources.list`:

```text
deb http://security.debian.org/debian-security buster/updates main
deb http://deb.debian.org/debian/ buster-updates main
```

Todo esto significa que los repositorios configurados determinan qué paquetes (y qué
versiones) podemos instalar. Si queremos tener un sistema completamente actualizado, es
decir, con las ultimas versiones de todos los paquetes disponibles en esos repositorios
podemos ejecutar:

```shell
david@amy:~$ sudo apt upgrade
```

Si incorporamos repositorios de versiones nuevas y queremos actualizarnos a ellos,
tendremos que ejecutar:

```shell
david@amy:~$ sudo apt dist-upgrade
```

Esto hará que la versión de nuestro sistema operativo corresponda con la versión del
repositorio más actual. Eso lo podemos ver con:

```shell
david@amy:~$ lsb_release -a
No LSB modules are available.
Distributor ID:	Debian
Description:	Debian GNU/Linux bullseye/sid
Release:	10.8
Codename:	buster
```

También podemos saber qué versiones de un determinado paquete tenemos disponibles en los
repositorios configurados y en cuál de ellos están:

```shell
david@amy:~$ apt-cache policy openconnect
openconnect:
  Instalados: (ninguno)
  Candidato:  8.02-1+deb10u1
  Tabla de versión:
     8.10-2+b1 650
        650 http://deb.debian.org/debian testing/main amd64 Packages
        600 http://deb.debian.org/debian sid/main amd64 Packages
     8.02-1+deb10u1 700
        700 http://deb.debian.org/debian buster/main amd64 Packages
        700 http://security.debian.org/debian-security buster/updates/main amd64 Packages
```

Esto significa, que no podremos instalar versiones de los paquetes que no estén en los
repositorios configurados. La solución puede ser añadir un repositorio más reciente que sí
lo contenga, pero teniendo cuidado porque las nuevas versiones de las dependencias podrían
afectar a otros paquetes.
