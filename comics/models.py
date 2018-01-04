import datetime
import os

from django.core.validators import RegexValidator
from django.db import models
from multiselectfield import MultiSelectField
from solo.models import SingletonModel


YEAR_CHOICES = [(r, r) for r in range(1837, datetime.date.today().year + 1)]

# Comic read status
STATUS_CHOICES = (
    (0, 'Unread'),
    (1, 'Partially Read'),
    (2, 'Read'),
)

# Creator roles for an issue
ROLE_CHOICES = (
    ('artist', 'Artist'),
    ('colorist', 'Colorist'),
    ('cover', 'Cover'),
    ('editor', 'Editor'),
    ('inker', 'Inker'),
    ('journalist', 'Journalist'),
    ('letterer', 'Letterer'),
    ('other', 'Other'),
    ('penciler', 'Penciler'),
    ('production', 'Production'),
    ('writer', 'Writer'),
)


class Settings(SingletonModel):
    help_str = ('A 40-character key provided by ComicVine. '
                'This is used to retrieve metadata about your comics. '
                'You can create a ComicVine API Key at '
                '<a target=\"_blank\" href=\"http://comicvine.gamespot.com/api/\">'
                "ComicVine's API Page</a> "
                '(ComicVine account is required).')

    api_key = models.CharField(
        'ComicVine API Key',
        help_text=help_str,
        validators=[RegexValidator(
            regex='^.{40}$',
            message='Length must be 40 characters.',
            code='nomatch'
        )],
        max_length=40,
        blank=True
    )
    comics_directory = models.CharField('Comics Directory',
                                        help_text='Directory where comic archives are located.',
                                        max_length=350,
                                        blank=True)

    def __str__(self):
        return "Settings"


class Arc(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', unique=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200)
    name = models.CharField('Arc Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    image = models.FileField(upload_to='images/', blank=True)

    def image_name(self):
        return os.path.basename(self.image.name)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Team(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', unique=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200)
    name = models.CharField('Team Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    image = models.FileField(upload_to='images/', blank=True)
    thumb = models.FileField(upload_to='images/', blank=True)

    def image_name(self):
        return os.path.basename(self.image.name)

    def thumb_name(self):
        return os.path.basename(self.thumb.name)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Character(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', unique=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200)
    name = models.CharField('Character Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    image = models.FileField(upload_to='images/', blank=True)
    thumb = models.FileField(upload_to='images/', blank=True)

    def image_name(self):
        return os.path.basename(self.image.name)

    def thumb_name(self):
        return os.path.basename(self.thumb.name)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Creator(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', unique=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200)
    name = models.CharField('Creator Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    image = models.FileField(upload_to='images/', blank=True)
    thumb = models.FileField(upload_to='images/', blank=True)

    def image_name(self):
        return os.path.basename(self.image.name)

    def thumb_name(self):
        return os.path.basename(self.thumb.name)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Publisher(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', null=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200)
    name = models.CharField('Series Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    logo = models.FileField(upload_to='images/', blank=True)

    def logo_name(self):
        return os.path.basename(self.logo.name)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Series(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', unique=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200, blank=True)
    name = models.CharField('Series Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    sort_title = models.CharField('Sort Name', max_length=200)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, null=True, blank=True)
    year = models.PositiveSmallIntegerField(
        'year', choices=YEAR_CHOICES, default=datetime.datetime.now().year, blank=True)
    desc = models.TextField('Description', max_length=500, blank=True)

    def __str__(self):
        return self.name

    def issue_numerical_order_set(self):
        return self.issue_set.all().order_by('date', 'number')

    @property
    def issue_count(self):
        return self.issue_set.all().count()

    def unread_issue_count(self):
        return self.issue_set.exclude(status=2).count()

    class Meta:
        verbose_name_plural = "Series"
        ordering = ["sort_title"]


class Issue(models.Model):
    cvid = models.PositiveIntegerField('ComicVine ID', unique=True)
    cvurl = models.URLField('ComicVine URL', max_length=200, blank=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True)
    name = models.CharField('Issue Name', max_length=200, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    number = models.CharField('Issue Number', max_length=25)
    date = models.DateField('Cover Date', blank=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    arcs = models.ManyToManyField(Arc, blank=True)
    characters = models.ManyToManyField(Character, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    file = models.CharField('File Path', max_length=300)
    cover = models.FileField('Cover Image', upload_to='images/', blank=True)
    thumb = models.FileField(
        'Thumbnail Image', upload_to='images/', blank=True)
    status = models.PositiveSmallIntegerField(
        'Status', choices=STATUS_CHOICES, default=0, blank=True)
    leaf = models.PositiveSmallIntegerField(
        editable=False, default=1, blank=True)
    page_count = models.PositiveSmallIntegerField(
        editable=False, default=1, blank=True)
    mod_ts = models.DateTimeField()
    import_date = models.DateField('Date Imported',
                                   auto_now_add=True)

    def cover_name(self):
        return os.path.basename(self.cover.name)

    def thumb_name(self):
        return os.path.basename(self.thumb.name)

    def __str__(self):
        return self.series.name + ' #' + str(self.number)


class Roles(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    roles = MultiSelectField(choices=ROLE_CHOICES)

    def __str__(self):
        return self.issue.series.name + ' #' + str(self.issue.number) + ' - ' + self.creator.name

    class Meta:
        verbose_name_plural = "Roles"
