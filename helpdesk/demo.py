from .storage import init_schema


def seed(connection):
    init_schema(connection)
    accounts = [
        ("alice", "acme", "requester"),
        ("bob", "acme", "requester"),
        ("sofia", "acme", "support"),
        ("ana", "otra", "support"),
    ]
    tickets = [
        (1, "acme", "alice", "La impresora dejó de responder", "OPEN", None, None),
        (2, "acme", "alice", "Revisar acceso al portal", "CLOSED", "sofia",
         "2025-03-02T10:00:00+00:00"),
        (3, "otra", "ana", "Consultar estado de una solicitud", "OPEN", None, None),
    ]
    history = [
        (1, 1, "created", "alice", "2025-03-01T10:00:00+00:00"),
        (2, 2, "created", "alice", "2025-03-01T11:00:00+00:00"),
        (3, 2, "assigned", "sofia", "2025-03-01T11:15:00+00:00"),
        (4, 2, "closed", "sofia", "2025-03-02T10:00:00+00:00"),
        (5, 3, "created", "ana", "2025-03-01T11:00:00+00:00"),
    ]

    with connection:
        connection.executemany(
            "INSERT OR IGNORE INTO accounts VALUES (?, ?, ?)", accounts
        )
        connection.executemany(
            "INSERT OR IGNORE INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?)", tickets
        )
        connection.executemany(
            "INSERT OR IGNORE INTO ticket_history VALUES (?, ?, ?, ?, ?)", history
        )
