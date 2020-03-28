from rest_framework import permissions


class IsAccessDeleteProduct(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            itemins = obj.productitemin.filter(is_init=False).exists()
            itemouts = obj.productitemout.filter(is_init=False).exists()
            stock_cards = obj.productstockcard.filter(is_init=False).exists()

            if itemins:
                return False

            if itemouts:
                return False

            if stock_cards:
                return False

        return True
