from rest_framework import permissions


class IsAccessDeleteStockIn(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            if obj.is_init == True:
                return True

            if obj.is_calculate == False:
                return True

            itemins = obj.stockinitemin.filter(is_init=False).exists()

            if itemins:
                return False

        return True


class IsAccessDeleteStockOut(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            if obj.is_init == True:
                return True

            if obj.is_calculate == False:
                return True

            itemouts = obj.stockoutitemout.filter(is_init=False).exists()

            if itemouts:
                return False

        return True
