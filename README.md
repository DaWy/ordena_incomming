# Multimedia Tidy Tool

Aquesta eina te el proposit de ajudar a ordenar un directori d'arxius multimedia. Pot convertir fotos a una resolució mes reduida per tal de reduir espai. Pot fer el mateix amb els videos.

## Funcionament

L'Script recorre una estructura de directoris per tal de trobar arxius multimedia. Les extensions son les següents:

```
included_ext = ['.jpg', '.png', '.gif', '.tif', ]
video_ext = ['.mov', '.mpg', '.mp4', ]
```
> Es poden modificar, pero s'haura de comprobar si la comanda assignada del ffmpeg suporta el tipus de contenidor de video. El mateix per les extensions d'imatges.

Tenim 2 modes diferents:

1. convert (Convertir): Fa un recorregut per l'estructura nomes convertint els fitxers. La conversió implica reduir la seva mida. En el cas de les imatges, fa una proporció basada en una mida base o "basewith" que es pot modificar:

```	basewidth = 1600```

2. move (Moure): Fa el mateix recorregut per el directori incoming pero nomes mou els arxius a una ubicació. La ubicació base es pasa per parametre.

L'Script buscara si hi ha un arxiu 'content.txt' dins de la carpeta. Això es fa per facilitar la feina de moure els fitxers a la seva carpeta corresponent.
Es necessari, ja que sino els arxius van a petar a una carpeta dins del path dels arxius anomenada _NO_CONTENT. 

## Requisits

Necessites tenir instalat el següent:
* python2.7
* ffmpeg: Eina de comandes per conversió d'arxius multimedia
* pymediainfo

## Ús de l'script

Donar permisos d'execució:

``` chmod u+x ./OrdenaIncomming.py ```

Convertir tots els fitxers dins d'un directori:

``` ./OrdenaIncomming.py -mode convert -ip "<path dels arxius a ordenar>" -mp "<path on aniran ordenats>" ```




