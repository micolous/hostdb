from hdb import models
#from django.db.models import signals, get_apps, get_models
from django.dispatch import receiver

#@receiver(post_syncdb, sender=models)
def init_data(app, created_models, verbosity, **kwargs):
    if models.DHCPScope in created_models:
        zone = models.DHCPScope(
            zonename="Global",
        )
        zone.save()
