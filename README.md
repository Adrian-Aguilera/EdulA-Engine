
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

Ejecutar servidor

```bash
  python manage.py runserver
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

## JSON Input:
```yaml
{
    "type_engine": {
        "EngineAV": false,
        "EngineChat": true
    },
    "mesage": "{mensaje}"
}

```


## Herramientas

**Lenguaje:** python


## Modulos


**ControllerrApp:** controlador que contiene todo el codigo principal

**DotEnv:** Modulo para cargar variables de entorno dinamicamente


## Feedback

Abreviaturas de nombres de los distintos modulos:

`EngineAV: virtual assistant`

`EngineChat: Chat Engine`

## Estructura:
**Modules:** Modulos para usarse en App principal

**TModel:** Modulos de prueba que sirven para probar nuevas funcionalidades

**App:** Archivo principal para ejecutar todo el programa

