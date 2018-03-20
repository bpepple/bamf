import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from solo.models import SingletonModel


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

    class Meta:
        verbose_name_plural = "Settings"


class Arc(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', unique=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200)
    name = models.CharField('Arc Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    image = models.ImageField(upload_to='images/arcs/',
                              max_length=150, blank=True)

    def get_absolute_url(self):
        return reverse('arc:detail', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Team(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', unique=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200)
    name = models.CharField('Team Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    image = models.ImageField(
        upload_to='images/teams/', max_length=150, blank=True)

    def get_absolute_url(self):
        return reverse('team:detail', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Character(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', unique=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200)
    name = models.CharField('Character Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    image = models.ImageField(
        upload_to='images/characters/', max_length=150, blank=True)

    def get_absolute_url(self):
        return reverse('character:detail', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Creator(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', unique=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200)
    name = models.CharField('Creator Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    image = models.ImageField(
        upload_to='images/creators/', max_length=150, blank=True)

    def get_absolute_url(self):
        return reverse('creator:detail', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Publisher(models.Model):
    cvid = models.PositiveIntegerField('Comic Vine ID', null=True)
    cvurl = models.URLField('Comic Vine URL', max_length=200)
    name = models.CharField('Series Name', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    logo = models.ImageField(
        upload_to='images/publishers/', max_length=150, blank=True)

    def get_absolute_url(self):
        return reverse('publisher:detail', args=[self.slug])

    def series_count(self):
        return self.series_set.all().count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Series(models.Model):
    YEAR_CHOICES = [(r, r)
                    for r in range(1837, datetime.date.today().year + 1)]

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

    def get_absolute_url(self):
        return reverse('series:detail', args=[self.slug])

    def __str__(self):
        return self.name

    @property
    def issue_count(self):
        return self.issue_set.all().count()

    @cached_property
    def unread_issue_count(self):
        if hasattr(self, '_prefetched_objects_cache') and 'issue' in self._prefetched_objects_cache:
            return len([x for x in self.issue_set.all() if x.status is not 2])
        return self.issue_set.exclude(status=2).count()

    class Meta:
        verbose_name_plural = "Series"
        ordering = ['sort_title', 'year']


class Issue(models.Model):
    STATUS_CHOICES = (
        (0, 'Unread'),
        (1, 'Partially Read'),
        (2, 'Read'),
    )

    cvid = models.PositiveIntegerField('ComicVine ID', unique=True)
    cvurl = models.URLField('ComicVine URL', max_length=200, blank=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True)
    name = models.CharField('Issue Name', max_length=350, blank=True)
    slug = models.SlugField(max_length=350, unique=True)
    number = models.CharField('Issue Number', max_length=25)
    date = models.DateField('Cover Date', blank=True)
    desc = models.TextField('Description', max_length=500, blank=True)
    arcs = models.ManyToManyField(Arc, blank=True)
    characters = models.ManyToManyField(Character, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    file = models.CharField('File Path', max_length=300)
    cover = models.ImageField(
        'Cover Image', upload_to='images/issues/', max_length=150, blank=True)
    status = models.PositiveSmallIntegerField(
        'Status', choices=STATUS_CHOICES, default=0, blank=True)
    leaf = models.PositiveSmallIntegerField(
        editable=False, default=1, blank=True)
    page_count = models.PositiveSmallIntegerField(
        editable=False, default=1, blank=True)
    mod_ts = models.DateTimeField()
    import_date = models.DateTimeField('Date Imported',
                                       auto_now_add=True)

    def get_absolute_url(self):
        return reverse('issue:detail', args=[self.slug])

    def __str__(self):
        return self.series.name + ' #' + str(self.number)

    class Meta:
        ordering = ['series__name', 'date', 'number']


class Role(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Roles(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    role = models.ManyToManyField(Role)

    def __str__(self):
        return self.issue.series.name + ' #' + str(self.issue.number) + ' - ' + self.creator.name

    class Meta:
        verbose_name_plural = "Roles"
        ordering = ['creator__name']
