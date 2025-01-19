from celery import Celery

# Inicializa o aplicativo Celery
celery_app = Celery(
    "tasks",
    broker="pyamqp://guest:guest@rabbitmq:5672//",  # Endereço do broker RabbitMQ
    backend="rpc://"  # Backend para resultados
)

# Configurações adicionais do Celery (se necessário)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Importa o módulo que contém as tarefas
import src.controller.user_celery  # Certifique-se de que este caminho está correto
