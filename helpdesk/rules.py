class DeskError(Exception):
    """Error de negocio que puede mostrarse en la terminal."""


def require_support(account):
    if account["role"] != "support":
        raise DeskError("Se requiere una cuenta de soporte.")


def require_ticket_access(account, ticket):
    if ticket is None or ticket["organization"] != account["organization"]:
        raise DeskError("Ticket no encontrado.")
    if account["role"] != "support" and account["username"] != ticket["author"]:
        raise DeskError("No tienes permiso para este ticket.")
