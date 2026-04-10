from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment

# This class customizes how the Listing model appears in the admin panel
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'current_price', 'seller', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'description')
    list_editable = ('is_active',) # Allows you to toggle active status directly from the list!

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)