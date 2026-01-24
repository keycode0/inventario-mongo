from datetime import datetime, timezone
import mongoengine as me


class BaseDocument(me.Document):
    """
    Documento base para todos los modelos MongoEngine.
    Incluye auditoría básica y soft delete.
    """

    created_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    is_active = me.BooleanField(default=True)

    meta = {
        "abstract": True
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Soft delete por defecto.
        """
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
        return super().save()