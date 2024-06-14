from django.contrib import admin

from . models import Order,OrderdItem

# Register your models & filtering Admin sites....
class OrderAdmin(admin.ModelAdmin):
    list_filter = [
        "owner",
        "order_status",
        "created_at",
    ]

    search_fields = (
        "owner",
        "id",
    )

admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderdItem)

