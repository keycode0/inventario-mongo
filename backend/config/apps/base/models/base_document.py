from datetime import datetime, timezone
import mongoengine as me


class BaseDocument(me.Document):
    """

    Documento base para todos los modelos MongoEngine.
    Incluye campos comunes y se marca como abstracto.

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

