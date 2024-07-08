# Book Manager API

Este proyecto es una API de gestión de libros. A continuación se detallan los pasos necesarios para configurar y ejecutar el proyecto en tu máquina local.

## Requisitos

- Python 3.9.12
- pip 24.1.1
- virtualenv
- Docker Desktop instalado

## Pasos para Configurar y Ejecutar el Proyecto

### 1. Crear un Directorio

Primero, crea un nuevo directorio llamado `book_manager_reto` y muévete a ese directorio:

'mkdir book_manager_reto'
'cd book_manager_reto'

### 2. 2. Clonar el Proyecto

Clona el repositorio del proyecto desde GitHub:

'git clone https://github.com/Fabio244000/book-manager-api.git'

### 3. Moverse al Directorio del Proyecto

Muévete al directorio del proyecto clonado:

'cd book-manager-api'

### 4. Ejecutar Docker Desktop

Asegúrate de que Docker Desktop esté ejecutándose en tu máquina.

### 5. Construir los Contenedores

Construye los contenedores Docker para el proyecto:

'docker-compose build'

### 6. Levantar el Proyecto

Levanta el proyecto utilizando Docker Compose:

'docker-compose ps'

Para detener los contenedores, utiliza:

'docker-compose down'

# ¡Disfruta usando el Book Manager API!
