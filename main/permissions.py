from django.core.exceptions import PermissionDenied
from .models import *


class CompletedTestMixin():

    def has_permission(self, **kwargs):
        print(self.request.GET, '++++++++++++++')
        completed_list = []
        completed_statistics = Statistics.objects.filter(user=self.request.user)
        for c in completed_statistics:
            completed_list.append(c.test.pk)
        return self.get_object().pk not in completed_list

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

# class UserIsOwnerMixin():
#
#     def has_permission(self):
#         return self.get_object().owner == self.request.user
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)
#
#
# class UserIsOwnerCheckMixin():
#
#     def has_permission(self):
#         obj = Check.objects.get(pk=self.kwargs['pk'])
#         return obj.owner == self.request.user
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)
#
#
# class UserIsOwnerStepMixin():
#
#     def has_permission(self):
#         return self.get_object().check_list.owner == self.request.user
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)
#
#
# class ChecksLimit():
#     def has_permission(self):
#         print('+++++++++++++++', self.request.user.checks.count())
#         return self.request.user.profile.max_checks > self.request.user.checks.count()
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_permission():
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)