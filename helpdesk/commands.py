from datetime import datetime, timezone

from .rules import DeskError, require_support, require_ticket_access
from .storage import add_history


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_account(connection, username):
    account = connection.execute(
        "SELECT username, organization, role FROM accounts WHERE username = ?",
        (username,),
    ).fetchone()
    if account is None:
        raise DeskError("Cuenta no encontrada.")
    return account


def get_ticket(connection, account, ticket_id):
    ticket = connection.execute(
        "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
    ).fetchone()
    require_ticket_access(account, ticket)
    return ticket


def list_tickets(connection, account):
    return connection.execute(
        """
        SELECT * FROM tickets
        WHERE organization = ? AND (? = 'support' OR author = ?)
        ORDER BY id
        """,
        (account["organization"], account["role"], account["username"]),
    ).fetchall()


def create_ticket(connection, account, title):
    title = title.strip()
    if not title:
        raise DeskError("El título es obligatorio.")

    with connection:
        cursor = connection.execute(
            """
            INSERT INTO tickets (organization, author, title, status)
            VALUES (?, ?, ?, 'OPEN')
            """,
            (account["organization"], account["username"], title),
        )
        ticket_id = cursor.lastrowid
        add_history(connection, ticket_id, "created", account["username"], utc_now())
    return ticket_id


def assign_ticket(connection, account, ticket_id, username):
    with connection:
        connection.execute("BEGIN IMMEDIATE")
        ticket = get_ticket(connection, account, ticket_id)
        require_support(account)
        assignee = get_account(connection, username)

        if (
            assignee["organization"] != account["organization"]
            or assignee["role"] != "support"
        ):
            raise DeskError("Elige una cuenta de soporte de tu organización.")
        if ticket["status"] == "CLOSED":
            raise DeskError("Un ticket cerrado no se puede asignar.")

        connection.execute(
            "UPDATE tickets SET status = 'ASSIGNED', assignee = ? WHERE id = ?",
            (username, ticket_id),
        )
        add_history(connection, ticket_id, "assigned", account["username"], utc_now())


def close_ticket(connection, account, ticket_id):
    with connection:
        connection.execute("BEGIN IMMEDIATE")
        ticket = get_ticket(connection, account, ticket_id)
        require_support(account)
        if ticket["status"] == "CLOSED":
            raise DeskError("El ticket ya está cerrado.")

        now = utc_now()
        connection.execute(
            "UPDATE tickets SET status = 'CLOSED', closed_at = ? WHERE id = ?",
            (now, ticket_id),
        )
        add_history(connection, ticket_id, "closed", account["username"], now)


def read_history(connection, account, ticket_id):
    get_ticket(connection, account, ticket_id)
    return connection.execute(
        """
        SELECT event, actor, happened_at FROM ticket_history
        WHERE ticket_id = ? ORDER BY id
        """,
        (ticket_id,),
    ).fetchall()
