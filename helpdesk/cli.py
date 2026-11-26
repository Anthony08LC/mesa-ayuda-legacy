import argparse
from contextlib import closing
import sqlite3
import sys

from . import commands
from .demo import seed
from .rules import DeskError
from .storage import connect


def configure_parser():
    parser = argparse.ArgumentParser(description="Mesa de ayuda del laboratorio")
    parser.add_argument("--db", default="demo.sqlite3", help="Archivo SQLite")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("init-demo", help="Carga datos ficticios")
    subcommands.add_parser("list", help="Lista los tickets visibles")
    create = subcommands.add_parser("create", help="Crea un ticket")
    create.add_argument("title")
    assign = subcommands.add_parser("assign", help="Asigna un ticket a soporte")
    assign.add_argument("ticket_id", type=int)
    assign.add_argument("assignee")
    close = subcommands.add_parser("close", help="Cierra un ticket")
    close.add_argument("ticket_id", type=int)
    history = subcommands.add_parser("history", help="Consulta el historial")
    history.add_argument("ticket_id", type=int)
    for name, subparser in subcommands.choices.items():
        if name != "init-demo":
            subparser.add_argument(
                "--actor", required=True, help="Cuenta ficticia de la sesión"
            )
    return parser


def execute(connection, args):
    if args.command == "init-demo":
        seed(connection)
        print("Datos de demostración disponibles.")
        return

    account = commands.get_account(connection, args.actor)
    if args.command == "list":
        for ticket in commands.list_tickets(connection, account):
            print(f'#{ticket["id"]} {ticket["status"]} {ticket["title"]}')
    elif args.command == "create":
        ticket_id = commands.create_ticket(connection, account, args.title)
        print(f"Ticket #{ticket_id} creado.")
    elif args.command == "assign":
        commands.assign_ticket(connection, account, args.ticket_id, args.assignee)
        print(f"Ticket #{args.ticket_id} asignado.")
    elif args.command == "close":
        commands.close_ticket(connection, account, args.ticket_id)
        print(f"Ticket #{args.ticket_id} cerrado.")
    elif args.command == "history":
        for entry in commands.read_history(connection, account, args.ticket_id):
            print(f'{entry["happened_at"]} | {entry["event"]} | {entry["actor"]}')


def main(argv=None):
    args = configure_parser().parse_args(argv)
    try:
        with closing(connect(args.db)) as connection:
            execute(connection, args)
    except DeskError as error:
        print(error, file=sys.stderr)
        return 1
    except sqlite3.Error:
        print(
            "No se pudo completar la operación en SQLite. Verifica el archivo y usa "
            "init-demo si necesitas preparar una base nueva.",
            file=sys.stderr,
        )
        return 1
    return 0
