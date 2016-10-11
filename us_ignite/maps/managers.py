from django.db import models


class LocationPublishedManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(LocationPublishedManager, self)
                .get_queryset(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))
