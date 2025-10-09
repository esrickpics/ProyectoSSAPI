
DATABASEDES = DATABASESDESARROLLO = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'PALDACADB',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASEPROD = DATABASESPRODUCCION = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ssapmcco_PALDACADB',
        'USER': 'ssapmcco_admin',
        'PASSWORD': 'AdminPaldaca',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}