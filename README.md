#Project1, WEB50
Web Programming with Python and JavaScript

En este proyecto se trata de construir un sitio web sobre reseñas de libros.
Se utilizó Python, Flask, PostgreSQL, HTML y CSS.

Para empezar, estuve basándome en el pset7 de CS50 (Finance) para ocupar la funcionalidad del @login_required y la plantilla layout, lo que me resultó más práctico a decir verdad, aunque no quedó como me lo imaginaba, se podría decir que estoy satisfecha.

Se disponen 7 plantillas cuyas funcionalidades son las siguientes:
- book.html: arroja la información del libro, como también la posibilidad de escribir una reseña y visualizar las que han hecho otros usuarios.
- error.html: sirve como una plantilla general para mandar errores de una manera más elegante, por así decirlo. 
- index.html: aquí es donde los usuarios podrán buscar los libros, ya sea por el ISBN, autor o título del libro.
- login.html y register.html disponen del formulario para que el usuario pueda loguearse.
- results.html: arroja una tabla con todos los posibles resultados que haya ingresado el usuario en la búsqueda.

En import.py se importan todos los libros que se habían puesto a disposición al momento de descargar la carpeta del proyecto en cuestión.

Finalmente, links.txt dispone de todo lo necesario para ingresar a la base de datos.
