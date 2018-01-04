from django.contrib import admin

from .models import (Arc, Character, Creator,
                     Issue, Publisher, Series,
                     Team)


@admin.register(Arc)
class ArcAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
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
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_filter = ('import_date', 'date', 'status')
    date_hierarchy = 'date'
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
    list_display = ('name', 'issue_count')
    list_filter = ('publisher',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
