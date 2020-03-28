from rest_framework import permissions


class IsAccessDeleteCustomer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            stockins = obj.supplierstockout.filter(is_init=False).exists()
            if stockins:
                return False

        return True


class IsAccessDeleteSupplier(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            stocks = obj.supplierstockin.filter(is_init=False).exists()
            if stocks:
                return False

        return True
