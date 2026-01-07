from config.apps.inventory.models.facility import Facility


ALLOWED_FACILITY_STATES = [
    "planificada",
    "en_proceso",
    "finalizada",
    "cancelada",
]


def soft_delete_facility(facility: Facility) -> None:
    """
    Desactiva lógicamente una instalación.
    """
    facility.is_active = False
    facility.save()


def change_facility_status(facility: Facility, new_status: str) -> None:
    """
    Cambia el estado de la instalación validando la transición.
    """
    if new_status not in ALLOWED_FACILITY_STATES:
        raise ValueError(f"Estado no permitido: {new_status}")

    facility.estado = new_status
    facility.save()
