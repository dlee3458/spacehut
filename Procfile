web: daphne spacehut.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python3 manage.py runworker --settings=spacehut.settings -v2