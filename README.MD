Запуск Worker
```shell
$ celery -A config worker --loglevel INFO
```

Запуск периодических задач
```sh
$ celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```