
# EdulA-Engine 

EdulA es un motor que permite procesar lenguaje natural para hacer distintas actividades educativas

## Ejecutar local

Clonar el repositorio 
```bash
  git clone https://github.com/Adrian-Aguilera/EdulA-Engine.git
```

Go to the project directory

```bash
  cd /EdulA-Engine
```


## Instalacion

Para poder instalar el proyecto, crearemos un .venv para instalar las dependencias

```bash
  python3 -m venv .venv
  .venv\Scripts\activate
```
una vez instalado y corriendo la terminal del .venv, instalar las dependencias corriendo

```bash
  pip install -r requirements.txt
```

## Deployment

Ejecutar servidor local

```bash
  python manage.py runserver
```

Ejecutar servidor local  con certificado ssl (recomendado)

```bash
  python manage.py runsslserver
```

## Informacion Adicional

Crear una aplicacion con django

```bash
  python manage.py startapp {name_app}
```

Crear migraciones del proyecto

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Crear usuario administrador
```bash
  python manage.py createsuperuser
```

## Json general chat:
```yaml
{
    "type_engine": {
        "EngineChat": true
    },
    "mesage": "{mensaje}"
}
```
## Json av chat:
```yaml
{
    "id_users": "TDS10052302",
    "type_engine": {
        "EngineAV": true
    },
    "id_message": "m01tds10052302",
    "user_message": "de que institucion eres?",
    "history_chat": {
        "system_response":"",
        "user_response": ""
    }
}
```

## Herramientas

**Lenguaje:** python
**FrameWork** Django restFramework


## Modulos
**ControllerrApp:** controlador que contiene todo el codigo principal

**LModel:** Modulo de conexion con IA

## Feedback

Abreviaturas de nombres de los distintos modulos:

`EngineAV: virtual assistant`

`EngineChat: Chat Engine`

## Estructura:
**Modules:** Modulos para usarse en App principal

**TModel:** Modulos de prueba que sirven para probar nuevas funcionalidades

**EduLA:** Proyecto principal de Django RestFramework

**EduApp:** Aplicacion principal de Django


