# NubiTest
A continuacion se detalla la forma de descargar y utilizar NubiTest, un modulo preparado para poder realizar encuestas, guardar usuarios, etc.

---
## Descarga
Para poder empezar, debemos clonar el repositorio:
```
git clone https://github.com/Agusmazzeo/NubiTest.git
```
Una vez descargado, tendremos un arbol de directorio asi:

    NubiTest
          |_ service/
          |_ application/
          |_ Nubi_test.postman_collection.json
          |_ README.md

En el directorio `Service` encontraremos todo lo relacionado al entorno de pruebas, siendo el `docker-compose.yml` para levantar la aplicacion.

Finalmente, en el directorio `application`, encontraremos lo relacionado a codigo:

    application
          |_ config/
          |_ src/
          |_ tests/
          |_ Dockerfile
          |_ requirements.txt
          |_ requirements-dev.txt
          |_ setup.py

---
## Deploy de la aplicacion
Habiendo descargado el directorio, procederemos a levantar la aplicacion, para lo cual simplemente deberemos ingresar al directorio `service` y ejecutar:
```
    docker-compose up -d
```
Este comando, comenzara el proceso de descarga de la imagen de `mongo:4.4.0`, `mongo-express` y el build de la imagen de `nubi-test`, para lo cual usara el Dockerfile ubicado en `application`.

Las versiones de Docker y Docker-Compose utilizadas son:
```
    Docker version 19.03.6, build 369ce74a3c

    docker-compose version 1.23.1, build b02f1306
```
---
---
## Uso de la aplicacion

Una vez levantada la aplicacion, verificar que no hubo ningun problema durante la creacion de los containers.

Utilizando `Postman` pueden descargar la coleccion con todos los endpoints necesarios para su uso.

Comenzaremos verificando la salud del sistema con el request `Get Alive`, el cual debería retornar esta respuesta:
```json
{
    "alive": true
}
```
A partir de ahora, se detallaran las funciones existentes y como utilizarlas:

---
### Crear una encuesta
Para esto usaremos el request `Create poll` el cual apunta al endpoint `/api/polls/create`. Los argumentos de una encuesta, deben seguir el siguiente formato:
```json
{
    "labels":{"Testing":"yes"},
    "questions":["Que dia es?", "Que tal?"],
    "possible_answers":[["Lunes","Martes","Miercoles","Jueves"],["Todo bien","Todo mal"]]
}
```
En `labels` indicaremos las etiquetas con las que marcamos la encuesta, y que posteriormente nos permitiran filtrar. Podemos agregar cuantos key-value consideremos.

En `questions` debemos ingresar una lista de preguntas.

En `possible_answers` debemos ingresar una lista de listas de respuestas, donde cada litas corresponde a las posibles respuestas de cada una de las preguntas.

En caso de crearse correctamente la encuesta, se devolvera el siguiente mensaje:

```json
{
    "result": "The poll was succesfully saved!",
    "success": true
}
```


#### Excepciones
 - No podran crearse mas de 4 respuestas por pregunta. De intentarlo, se devolvera el siguiente error:
  ```json
    {
        "result": "The questions list is either empty or there is a problem with answers length..",
        "success": false
    }
  ```

  - Debe estarse logueado con un usuario ya creado para poder crear encuestas. Caso contrario se devolvera el siguiente error:

  ```json
    {
        "result": "You must login before creating polls.",
        "success": false
    }
  ```

  ---
  ### Responder preguntas
  Para poder responder a las preguntas de las encuestas, deberemos primero tener el `id` de la encuesta que vamos a responder, para lo cual usaremos el request `Get all polls` para traernos todas las encuestas creadas:
  ```json
        {
            "result": [
                {
                    "author": "5f7fa370da5e80d824a9d762",
                    "date": "Thu, 08 Oct 2020 23:41:06 GMT",
                    "id": "5f7fa3925a124d98769d5ef0",
                    "labels": {
                        "Testing": "yes"
                    },
                    "possible_answers": [
                        [
                            "Lunes",
                            "Martes"
                        ],
                        [
                            "Todo bien",
                            "Todo mal"
                        ]
                    ],
                    "questions": [
                        "Que dia es?",
                        "Que tal?"
                    ],
                    "related_answers": [
                    ]
                }
            ],
            "success": true
        }
  ```

  Utilizando el `id` de la encuesta, podremos responder a la encuesta, utilizando el request `Create answer` el cual apunta al endpoint `/api/polls/answer/<id>` donde completaremos el `id` con el valor de la encuesta a responder.
  Enviaremos en el body el siguiente json:
  ```json
    {
        "answers":["Lunes","Si"]
    }
  ```

  En caso de responder con respuestas que no esten incluidas en las respuestas posibles o con mayor cantidad de respuestas que de preguntas, se devovlera el siguiente error:
  ```json
    {
        "result": "The answers list is either empty or its length doesnt fit with the poll questions list..",
        "success": false
    }
  ```
---
### Consultas por label y por usuario
Es posible realizar consultas de encuestas que posean los labels indicados y que hayan sido creadas por los usuarios indicados.

Para esto, podremos utilizar los request `Get polls by label` y `Get polls by user`. 

Para las consultas por label, debemos hacerlo mediante un query string del tipo `/api/polls/labels?Testing=yes` donde indicaremos mediante key-values, la combinacion de labels que queresmos traer. Para este ejemplo, la respuesta sería de esta forma por encuesta encontrada:

```json
{
    "result": [
        {
            "author": "5f7fa66c4ef03b9cb84b968f",
            "date": "Thu, 08 Oct 2020 23:53:59 GMT",
            "id": "5f7fa69783bbd94509a0d7b8",
            "labels": {
                "Testing": "yes"
            },
            "possible_answers": [
                [
                    "Lunes",
                    "Martes",
                    "Miercoles",
                    "Jueves"
                ],
                [
                    "Todo bien",
                    "Todo mal"
                ]
            ],
            "questions": [
                "Que dia es?",
                "Que tal?"
            ],
            "related_answers": []
        }
    ],
    "success": true
}
```

De la misma manera, podremos realizar consultas por usuario, agregando el id del usuario al final del endpoint `/api/polls/user?id=5f7fa370da5e80d824a9d762` recibiendo respuestas del mismo formato de antes:

```json
{
    "result": [
        {
            "author": "5f7fa370da5e80d824a9d762",
            "date": "Thu, 08 Oct 2020 23:41:06 GMT",
            "id": "5f7fa3925a124d98769d5ef0",
            "labels": {
                "Testing": "yes"
            },
            "possible_answers": [
                [
                    "Lunes",
                    "Martes"
                ],
                [
                    "Todo bien",
                    "Todo mal"
                ]
            ],
            "questions": [
                "Que dia es?",
                "Que tal?"
            ],
            "related_answers": [
                "5f7faa58358f60ec6141cf28"
            ]
        }
    ],
    "success": true
}
```
---
### Creacion de usuarios

Para poder crear encuestas, primero hay que tener un usuario y estar logueado, para lo cual, haremos uso del request `Sign in user` que apunta al endpoint `/api/users/sign_in` al cual, enviandole el siguiente tipo de informacion el request:
```json
    {
        "username": "Agusmazzeo",
        "password": "1234",
        "user_data": {
            "age": 23,
            "complete_name": "Agustin"
        }
    }
```
Nos permitira crear un usuario, en caso de que no exista otro con el mismo username. El campo `user_data` es opcional.

Recibiremos una respuesta de esta forma:
```json
{
    "result": "The User was succesfully saved!",
    "success": true
}
```

---
### Login de usuarios

Habiendo creado el usuario, debemos loguearnos, para lo cual usaremos el request `Login user` que apunta al endpoint `/api/users/log_in` y que recbiendo el nombre de usuario y contraseña, nos dara el id de usuario para poder crear encuestas. Debemos enviar:

```json
{
    "username":"Agusmazzeo",
    "password":"1234"
}
```

Y en caso de loguearnos correctamente, recibiremos la respuesta correspondiente:

```json
{
    "result": "Welcome Agusmazzeo!",
    "success": true
}
```
