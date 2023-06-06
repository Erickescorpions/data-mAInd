## Instrucciones

Para ejecutar el servidor backend deberas tener instalado virtualenv, para instalarlo:
```
pip install virtualenv
```

Despues de esto, necesitas estar en la carpeta back/
```
cd back
```

Dentro de la carpeta back/ deberas crear un entorno virtual:
```
virtualenv -p python3 env
```

Para instalar las dependencias es necesario iniciar el entorno virtual:
```
/env/scripts/activate
```

Para instalar las dependencias: 
```
pip install -r requirements.txt
```

## Ejecucion
Para ejecutar la aplicación, se tiene que ejecutar desde la carpeta principal del proyecto:
```
python app\app.py
```

Para desactivar el entorno virtual:
```
deactivate
```

Para probar la api puede utilizar software como **insomnia** o **postman**.