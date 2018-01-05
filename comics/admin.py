from django.contrib import admin

from .models import (Arc, Character, Creator,
                     Issue, Publisher, Series,
                     Team)


UNREAD = 0
READ = 2


def mark_as_read(modeladmin, request, queryset):
    queryset.update(status=READ)
mark_as_read.short_description = 'Mark as read'


def mark_as_unread(modeladmin, request, queryset):
    queryset.update(status=UNREAD)
mark_as_unread.short_description = 'Mark as unread'


@admin.register(Arc)
class ArcAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    # form view
    fieldsets = (
        (None, {'fields': ('cvid', 'cvurl', 'name',
                           'slug', 'desc', 'image', 'thumb')}),
        ('Related', {'fields': ('teams',)}),
    )
    filter_horizontal = ('teams',)


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    search_fields = ('series__name',)
    list_display = ('__str__', 'status')
    list_filter = ('import_date', 'date', 'status')
    date_hierarchy = 'date'
    actions = [mark_as_read, mark_as_unread]
    # form view
    fieldsets = (
        (None, {'fields': ('cvid', 'cvurl', 'series', 'name',
                           'slug', 'number', 'date', 'desc',
                           'cover', 'thumb', 'status')}),
        ('Related', {'fields': ('arcs', 'characters', 'teams')}),
    )
    filter_horizontal = ('arcs', 'characters', 'teams')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'issue_count')
    list_filter = ('publisher',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
