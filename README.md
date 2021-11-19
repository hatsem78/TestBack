# TestBack


Crear un virtualenv 
python3 -m venv env
source env/bin/activate


## Crear las migraciones correspondietes

    python mamage.py makemigrations

    python magnae.py migrate
    
    
## Crear un super usuario

    python manage.py createsuperuser 
    
    Email address: admin@admin.com
    
    Password: ******
    
    Password(again): ******
    
## Correr TestBack

    runserver 0.0.0.0:8010
    
    
Se puede utilizar los endpoind del archivo test_back.postman_collection.json, se implemento seguridad jwt