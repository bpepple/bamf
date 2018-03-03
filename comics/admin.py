from django.contrib import admin

from .models import (Arc, Character, Creator,
                     Issue, Publisher, Series,
                     Team, Roles)

from comics.tasks import (refresh_issue_task, refresh_series_task,
                          refresh_publisher_task, refresh_character_task,
                          refresh_creator_task, refresh_team_task,
                          refresh_arc_task)


UNREAD = 0
READ = 2


def create_msg(rows_updated):
    if rows_updated == 1:
        message_bit = "1 item was"
    else:
        message_bit = "%s items were" % rows_updated

    return message_bit


@admin.register(Arc)
class ArcAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    readonly_fields = ('cvid', 'cvurl')
    prepopulated_fields = {'slug': ('name',)}
    actions = ['refresh_arc_metadata']
    fieldsets = (
        (None, {
            'fields': ('cvid', 'cvurl', 'name', 'slug', 'desc', 'image')
        }),
    )

    def refresh_arc_metadata(self, request, queryset):
        rows_updated = 0
        for arc in queryset:
            success = refresh_arc_task(arc.cvid)
            if success:
                rows_updated += 1

        message_bit = create_msg(rows_updated)
        self.message_user(request, "%s successfully refreshed." % message_bit)
    refresh_arc_metadata.short_description = 'Refresh selected Story Arcs metadata'


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('cvid', 'cvurl')
    actions = ['refresh_character_metadata']
    # form view
    fieldsets = (
        (None, {'fields': ('cvid', 'cvurl', 'name',
                           'slug', 'desc', 'image')}),
        ('Related', {'fields': ('teams',)}),
    )
    filter_horizontal = ('teams',)

    def refresh_character_metadata(self, request, queryset):
        rows_updated = 0
        for character in queryset:
            success = refresh_character_task(character.cvid)
            if success:
                rows_updated += 1

        message_bit = create_msg(rows_updated)
        self.message_user(request, "%s successfully refreshed." % message_bit)
    refresh_character_metadata.short_description = 'Refresh selected Characters metadata'


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('cvid', 'cvurl')
    actions = ['refresh_creator_metadata']
    fieldsets = (
        (None, {
            'fields': ('cvid', 'cvurl', 'name', 'slug', 'desc', 'image')
        }),
    )

    def refresh_creator_metadata(self, request, queryset):
        rows_updated = 0
        for creator in queryset:
            success = refresh_creator_task(creator.cvid)
            if success:
                rows_updated += 1

        message_bit = create_msg(rows_updated)
        self.message_user(request, "%s successfully refreshed." % message_bit)
    refresh_creator_metadata.short_description = 'Refresh selected Creators metadata'


class RolesInline(admin.TabularInline):
    model = Roles
    extra = 0


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    search_fields = ('series__name',)
    readonly_fields = ('file', 'cvid', 'cvurl', 'series', 'number')
    list_display = ('__str__', 'status', 'import_date')
    list_filter = ('import_date', 'date', 'status')
    date_hierarchy = 'date'
    actions = ['mark_as_read', 'mark_as_unread', 'refresh_issue_metadata']
    # form view
    fieldsets = (
        (None, {'fields': ('cvid', 'file', 'cvurl', 'series',
                           'name', 'slug', 'number', 'date',
                           'desc', 'cover', 'status')}),
        ('Related', {'fields': ('arcs', 'characters', 'teams')}),
    )
    filter_horizontal = ('arcs', 'characters', 'teams')
    inlines = [RolesInline]

    def mark_as_read(self, request, queryset):
        rows_updated = queryset.update(status=READ)
        message_bit = create_msg(rows_updated)
        self.message_user(
            request, "%s successfully marked as read." % message_bit)
    mark_as_read.short_description = 'Mark selected issues as read'

    def mark_as_unread(self, request, queryset):
        rows_updated = queryset.update(status=UNREAD)
        message_bit = create_msg(rows_updated)
        self.message_user(
            request, "%s successfully marked as unread." % message_bit)
    mark_as_unread.short_description = 'Mark selected issues as unread'

    def refresh_issue_metadata(self, request, queryset):
        rows_updated = 0
        for issue in queryset:
            success = refresh_issue_task(issue.cvid)
            if success:
                rows_updated += 1

        message_bit = create_msg(rows_updated)
        self.message_user(
            request, "%s metadata successfuly refreshed." % message_bit)
    refresh_issue_metadata.short_description = 'Refresh selected issues metadata'


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'series_count',)
    readonly_fields = ('cvid', 'cvurl')
    actions = ['refresh_publisher_metadata']
    fieldsets = (
        (None, {
            'fields': ('cvid', 'cvurl', 'name', 'slug', 'desc', 'logo')
        }),
    )

    def refresh_publisher_metadata(self, request, queryset):
        rows_updated = 0
        for publisher in queryset:
            success = refresh_publisher_task(publisher.cvid)
            if success:
                rows_updated += 1

        message_bit = create_msg(rows_updated)
        self.message_user(request, "%s successfully refreshed." % message_bit)
    refresh_publisher_metadata.short_description = 'Refresh selected Publishers metadata'


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'year', 'issue_count')
    list_filter = ('publisher',)
    readonly_fields = ('cvid', 'cvurl')
    actions = ['mark_as_read', 'mark_as_unread',
               'refresh_series_metadata',
               'refresh_series_issues_metadata']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('cvid', 'cvurl', 'name', 'slug', 'desc')
        }),
    )

    def mark_as_read(self, request, queryset):
        issues_count = 0
        for i in range(queryset.count()):
            issues_updated = Issue.objects.filter(
                series=queryset[i]).update(status=READ)
            issues_count += issues_updated
        message_bit = create_msg(issues_count)
        self.message_user(
            request, "%s successfully marked as read." % message_bit)
    mark_as_read.short_description = 'Mark selected Series as read'

    def mark_as_unread(self, request, queryset):
        issues_count = 0
        for i in range(queryset.count()):
            issues_updated = Issue.objects.filter(
                series=queryset[i]).update(status=UNREAD)
            issues_count += issues_updated
        message_bit = create_msg(issues_count)
        self.message_user(
            request, "%s successfully marked as unread." % message_bit)
    mark_as_unread.short_description = 'Mark selected Series as unread'

    def refresh_series_metadata(self, request, queryset):
        rows_updated = 0
        for series in queryset:
            success = refresh_series_task(series.cvid)
            if success:
                rows_updated += 1

        message_bit = create_msg(rows_updated)
        self.message_user(request, "%s successfully refreshed." % message_bit)
    refresh_series_metadata.short_description = 'Refresh selected Series metadata'

    def refresh_series_issues_metadata(self, request, queryset):
        issues_count = 0
        for i in range(queryset.count()):
            series = Issue.objects.filter(series=queryset[i])
            for num in range(series.count()):
                success = refresh_issue_task(series[num].cvid)
                if success:
                    issues_count += 1
        message_bit = create_msg(issues_count)
        self.message_user(
            request, "%s successfully updated." % message_bit)
    refresh_series_issues_metadata.short_description = 'Refresh selected Series issues metadata'


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('cvid', 'cvurl')
    actions = ['refresh_team_metadata']
    fieldsets = (
        (None, {
            'fields': ('cvid', 'cvurl', 'name', 'slug', 'desc', 'image')
        }),
    )

    def refresh_team_metadata(self, request, queryset):
        rows_updated = 0
        for team in queryset:
            success = refresh_team_task(team.cvid)
            if success:
                rows_updated += 1

        message_bit = create_msg(rows_updated)
        self.message_user(request, "%s successfully refreshed." % message_bit)
    refresh_team_metadata.short_description = 'Refresh selected Teams metadata'
