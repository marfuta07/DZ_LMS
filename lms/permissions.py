from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    message = 'Доступ только для модераторов.'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()


class IsOwner(permissions.BasePermission):
    message = 'Вы не являетесь владельцем этого объекта.'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsNotModerator(permissions.BasePermission):
    message = 'Доступ запрещён для модераторов.'

    def has_permission(self, request, view):
        return not request.user.groups.filter(name='Модераторы').exists()