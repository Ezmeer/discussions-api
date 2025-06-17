from rest_framework.exceptions import ValidationError, PermissionDenied


class OwnerPermissionMixin:
    def assert_is_owner(self, obj, user_id_field, provided_user_id):
        actual_user_id = getattr(obj, user_id_field)
        if not provided_user_id:
            raise ValidationError({"user_id": "This field is required."})
        if str(actual_user_id) != str(provided_user_id):
            raise PermissionDenied("You are not allowed to perform this action.")
