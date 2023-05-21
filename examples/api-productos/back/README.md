# API Productos 

## Instalacion

Es necesario tener instalado virtualenv, para esto: 
```
pip install virtualenv
```

Despues es necesario crear un entorno virtual:
```
virtualenv -p python3 env
```

Despues de este paso se necesita inciar el entorno virtual con el siguiente comando: 
```
/env/scripts/activate
```

Para instalar las dependencias dentro de este entorno virtual solo es necesario correr el siguiente comando: 
```
pip install -r requirements.txt
```
## Ejecución 

Para ejecutar la aplicación:
```
python app\app.py
```

Para desactivar el entorno virtual:
```
deactivate
```

Para probar la api puede utilizar software como **insomnia** o **postman**.