from django.contrib import admin

from .models import (Arc, Character, Creator,
                     Issue, Publisher, Series,
                     Team)


UNREAD = 0
READ = 2


def create_issue_msg(rows_updated):
    if rows_updated == 1:
        message_bit = "1 issue was"
    else:
        message_bit = "%s issues were" % rows_updated

    return message_bit


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
    list_display = ('__str__', 'status', 'import_date')
    list_filter = ('import_date', 'date', 'status')
    date_hierarchy = 'date'
    actions = ['mark_as_read', 'mark_as_unread']
    # form view
    fieldsets = (
        (None, {'fields': ('cvid', 'cvurl', 'series', 'name',
                           'slug', 'number', 'date', 'desc',
                           'cover', 'thumb', 'status')}),
        ('Related', {'fields': ('arcs', 'characters', 'teams')}),
    )
    filter_horizontal = ('arcs', 'characters', 'teams')

    def mark_as_read(self, request, queryset):
        rows_updated = queryset.update(status=READ)
        message_bit = create_issue_msg(rows_updated)
        self.message_user(
            request, "%s successfully marked as read." % message_bit)
    mark_as_read.short_description = 'Mark selected issues as read'

    def mark_as_unread(self, request, queryset):
        rows_updated = queryset.update(status=UNREAD)
        message_bit = create_issue_msg(rows_updated)
        self.message_user(
            request, "%s successfully marked as unread." % message_bit)
    mark_as_unread.short_description = 'Mark selected issues as unread'


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'series_count',)


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'year', 'issue_count')
    list_filter = ('publisher',)
    actions = ['mark_as_read', 'mark_as_unread']
    prepopulated_fields = {'slug': ('name',)}

    def mark_as_read(self, request, queryset):
        issues_count = 0
        for i in range(queryset.count()):
            issues_updated = Issue.objects.filter(
                series=queryset[i]).update(status=READ)
            issues_count += issues_updated
        message_bit = create_issue_msg(issues_count)
        self.message_user(
            request, "%s successfully marked as read." % message_bit)
    mark_as_read.short_description = 'Mark selected series as read'

    def mark_as_unread(self, request, queryset):
        issues_count = 0
        for i in range(queryset.count()):
            issues_updated = Issue.objects.filter(
                series=queryset[i]).update(status=UNREAD)
            issues_count += issues_updated
        message_bit = create_issue_msg(issues_count)
        self.message_user(
            request, "%s successfully marked as unread." % message_bit)
    mark_as_unread.short_description = 'Mark selected series as unread'


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
