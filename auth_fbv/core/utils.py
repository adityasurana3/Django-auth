from core.permission_config import PERMISSION_CONFIG
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


def access_role(user, role):
    role_permission = PERMISSION_CONFIG.get(role, {})
    for model, permissions in role_permission.items():
        content_type = ContentType.objects.get_for_model(model=model)
        for perm_code in permissions:
            permission = Permission.objects.get(
                content_type=content_type, codename=f"{perm_code}_{model._meta.model_name}")
            user.user_permissions.add(permission)
 