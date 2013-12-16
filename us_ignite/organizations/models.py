from django.db import models
from django.core.urlresolvers import reverse

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager


class Organization(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="org", blank=True)
    members = models.ManyToManyField(
        'auth.User', blank=True, through='organizations.OrganizationMember')
    website = models.URLField(max_length=500, blank=True)
    tags = TaggableManager(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return self.name

    def is_published(self):
        return self.status == self.PUBLISHED

    def is_draft(self):
        return self.status == self.DRAFT

    def is_member(self, user):
        return True if self.members.filter(id__exact=user.id) else False

    def is_visible_by(self, user):
        return self.is_published() or self.is_member(user)

    def get_absolute_url(self):
        return reverse('organization_detail', args=[self.slug])

    def get_edit_url(self):
        return reverse('organization_edit', args=[self.slug])


class OrganizationMember(models.Model):
    user = models.ForeignKey('auth.User')
    organization = models.ForeignKey('organizations.Organization')
    created = CreationDateTimeField()

    class Meta:
        unique_together = ('user', 'organization')

    def __unicode__(self):
        return u'%s membership of %s' % (self.organization, self.user)