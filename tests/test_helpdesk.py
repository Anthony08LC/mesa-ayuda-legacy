from contextlib import closing
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest


class HelpdeskCLITest(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.database = str(Path(workspace.name) / "helpdesk.sqlite3")
        self.assertEqual(self.run_cli("init-demo").returncode, 0)

    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, "-m", "helpdesk", "--db", self.database, *arguments],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )

    def ticket_state(self, ticket_id):
        with closing(sqlite3.connect(self.database)) as connection:
            return connection.execute(
                "SELECT status, assignee, closed_at FROM tickets WHERE id = ?",
                (ticket_id,),
            ).fetchone()

    def test_requester_lists_own_tickets(self):
        result = self.run_cli("list", "--actor", "alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("#1 OPEN", result.stdout)
        self.assertIn("#2 CLOSED", result.stdout)
        self.assertNotIn("#3", result.stdout)

    def test_support_can_close_and_audit_ticket(self):
        result = self.run_cli("close", "1", "--actor", "sofia")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.ticket_state(1)[0], "CLOSED")
        self.assertIsNotNone(self.ticket_state(1)[2])
        history = self.run_cli("history", "1", "--actor", "alice")
        self.assertEqual(history.returncode, 0, history.stderr)
        self.assertIn("closed | sofia", history.stdout)

    def test_cross_organization_access_is_denied(self):
        result = self.run_cli("history", "1", "--actor", "ana")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Ticket no encontrado.", result.stderr)

    def test_requester_cannot_close_ticket(self):
        result = self.run_cli("close", "1", "--actor", "alice")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Se requiere una cuenta de soporte.", result.stderr)
        self.assertEqual(self.ticket_state(1)[0], "OPEN")

    def test_create_and_assign_ticket(self):
        result = self.run_cli("create", "Revisar correo", "--actor", "alice")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ticket #4 creado.", result.stdout)
        result = self.run_cli("assign", "4", "sofia", "--actor", "sofia")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.ticket_state(4), ("ASSIGNED", "sofia", None))
        history = self.run_cli("history", "4", "--actor", "alice")
        self.assertEqual(history.returncode, 0, history.stderr)
        self.assertIn("created | alice", history.stdout)
        self.assertIn("assigned | sofia", history.stdout)
