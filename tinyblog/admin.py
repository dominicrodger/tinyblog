from django.contrib import admin
from tinyblog.models import Post, EmailSubscriber
from tinymce.widgets import TinyMCE

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created', 'emailed', )
    list_filter = ('emailed',)
    date_hierarchy = 'created'
    search_fields = ('title', 'text',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('emailed', )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('text_html','teaser_html',):
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
            ))
        return super(PostAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Post, PostAdmin)

class EmailSubscriberAdmin(admin.ModelAdmin):
    list_filter = ('confirmed', 'unsubscribed',)
    list_display = ('email', 'confirmed', 'subscribed', 'unsubscribed',)
    readonly_fields = ('uuid_first', 'uuid_second',)

admin.site.register(EmailSubscriber, EmailSubscriberAdmin)
