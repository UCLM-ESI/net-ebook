# sintáxis


## notas al pie

Por ejemplo [^1].

[^1]: y aquí va el texto de la nota.


## referencias cruzadas

markdown:
    (chap:nombre)=
    # sección

notebook:
    { : .chap:nombre }

- enlace:

    sec{chap:nombre}`título visible`
    [`título`](chap:nombre)


## acrónimos

*[SO]: Sistema Operativo


## Listado tipo "lista de definiciones"

Shell
: Una introducción extremadamente práctica al interprete de comandos.
