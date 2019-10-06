from guardian.mixins import PermissionRequiredMixin

class PermissionRequiredModified(PermissionRequiredMixin):
    login_url = '/funcionarios'