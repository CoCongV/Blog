from celery import Celery
from flask import current_app


# class FlaskCelery(object):
#     def __init__(self):
#         super(FlaskCelery, self).__init__()
#
#     def init_app(self, app):
#         self.celery = Celery(app.import_name)
#         self.celery.conf.update(app.config)
#         TaskBase = self.celery.Task
#
#         class ContextTask(TaskBase):
#             abstract = True
#
#             def __call__(self, *args, **kwargs):
#                 with app.app_context():
#                     return TaskBase.__call__(self, *args, *kwargs)
#         self.celery.Task = ContextTask


def make_celery():
    app = current_app._get_current_object()
    celery = Celery(app.import_name)
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery