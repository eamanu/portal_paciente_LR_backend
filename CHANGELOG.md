# CHANGELOG

## 1.4.0
* Agrego "/get-genders" endpoint
* Muchos fixes no registrados ;).

## 1.3.2
* Bug fixes.

## 1.3.1
* Fix dependencies.

## 1.3.0
* Agregado de dos campos nuevos en person para almacenar info de archivos subidos.
* Se agrega feature de validación de email. Este se realiza durante el upload de las imagenes
del DNI. Se crea el endpoint "/validate-email" que recibe el token generado para validar
el mail.
* Se agrega la feature de cambio de password. Para ello se utiliza el endpoint "/recover-password"
que solo retorna un ReponseOK, y no expone ningún resultado, si es que el mail no existe o es 
admin, o no está validado, para no tener un leak de información.
  * Se agrega el endpoint "/change-password" que recibe el token enviado al mail más la nueva
  contraseña.

## 1.2.0
* Cuando se crea la persona: retorna el id.
* Se agrega el id de persona en el login.
* Categorias: nuevo endpoint.
* Estados de personas: nuevo endpoint.
* Cuando se crea el mensaje: retorna el id.
* Agregar a mensajes un atributo que diga cuándo un mensaje se envió.

## 1.1.2
* Fix del request a HCE Get patient Data

## 1.1.1
* Se agrega endpoint "/version" para verificar la versión del backend.

## 1.1.0
* Se cambia los endpoints para el login:
  - "/login": es utilizado para loguear pacientes.
  - "/ogin-admin" es utilizado para loguear administradores.
* [Development] Bump ujson from 4.3.0 to 5.1.0.
* [Development] Create codeql-analysis.yml
* Fix de creación de personas y users.
* Se agrega que no se pueden crear personas con el mismo dni y mails, y usuarios con el mismo username.
* Se agrega/arregla los siguientes endpoints:
  - /createmessage
  - /updatemessage
  - /deletemessage
  - /sendmessage
  - /get-messages-by-person
  - /getmessage
  - /get-all-messages
  - /setmessageread
* [Development] Se agrega control de version

## 1.0.0
* Hasta dónde lo conocemos :-)
