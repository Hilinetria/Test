
1) Тестовое задание делалось на python 3.6. Нужно настроить venv, активировать его и установить нужные пакеты из Test/base/requirements.txt. Например:
    ```
    virtualenv venv --python=/usr/bin/python3
    source ./venv/bin/activate
    pip install -r requirements.txt
    ```

2) Приложение использует postgres, поэтому его нужно установить (использовалась 10 версия, но не обязательно). Далее накатить руками на postgres скрипт Test/base/app/base_init_db.sql и выполнить питоновский скрипт Test/base/app/init_db.py
3) Перейти в Test/base/app и запустить main.py. Приложение будет запушено на http://0.0.0.0:8080
4) К приложению приложен  "сервис" - Test/service/server.py, который настроен в конфиге для запуска. В конфиге Test/base/config/app.yaml нужно будет поменять путь path до "сервиса"  main в разделе services