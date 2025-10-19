from datetime import datetime, timezone

def license_is_valid(license_obj):
    if not license_obj:
        return False, 'no_license'
    if not license_obj.is_active:
        return False, 'inactive'
    if license_obj.expires_at:
        now = datetime.now(timezone.utc)
        if license_obj.expires_at < now:
            return False, 'expired'
    return True, 'ok'
