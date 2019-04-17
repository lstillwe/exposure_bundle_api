from swagger_server.models import settings

class Databases(object):
    def __init__(self):
        for database in settings.INSTALLED_DATABASES:
            module = "swagger_server.models." + database
            print(module)
            froml = "models." + database
            setattr(self, database, __import__(module, fromlist=[froml,]))
