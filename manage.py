import os
from typing import Any, Optional

import typer
import uvicorn

# init typer
app = typer.Typer()


@app.command(name="runserver", help="run server", add_help_option=True)
def run_dev_server(
    port: int = typer.Option(8000, help="app port number", envvar="PORT"),
    host: str = typer.Option("localhost", help="app host", envvar="HOST"),
    workers: Optional[int] = typer.Option(None, help="multiple worker processes"),
    dev: bool = typer.Option(False, help="run development server"),
) -> None:
    config: dict[str, Any] = {"host": host, "port": port, "log_level": "info", "workers": workers}

    if dev:
        config.update({"log_level": "debug", "reload": True, "workers": None})

    uvicorn.run("src.main:app", **config)  # type: ignore


@app.command(
    name="makemigrations",
    help="run autogenerate alembic revisions",
    add_help_option=True,
)
def make_migrations(
    name: Optional[str] = typer.Option(None, help="revision name"),
    auto_off: bool = typer.Option(False, help="turn off --autogenerate option"),
) -> None:
    command = "alembic revision"

    if not auto_off:
        command = " ".join([command, "--autogenerate"])

    if name:
        command = " ".join([command, f'-m "{name}"'])

    os.system(command)


@app.command(name="migrate", help="run migrations", add_help_option=True)
def run_migrate() -> None:
    command = "alembic upgrade head"
    os.system(command)


@app.command(name="revert", help="undo last migration", add_help_option=True)
def run_migrate_back() -> None:
    command = "alembic downgrade -1"
    os.system(command)


@app.command(name="lint", help="lint app")
def run_app_lint() -> None:
    print("{:.<64}\x1b[6;30;42mDone!\x1b[0m".format("mypy"))
    os.system("mypy .")
    print("{:.<64}\x1b[6;30;42mDone!\x1b[0m".format("flake8"))
    os.system("flake8")
    print("{:.<64}\x1b[6;30;42mDone!\x1b[0m".format("black"))
    os.system("black . --check")
    print("{:.<64}\x1b[6;30;42mDone!\x1b[0m".format("isort"))
    os.system("isort --check-only --color .")


@app.command(name="format", help="format app [autoflake,black,isort]")
def run_app_format() -> None:
    print("{:.<64}\x1b[6;30;42mDone!\x1b[0m".format("autoflake"))
    os.system(
        """
        autoflake \
        --remove-all-unused-imports \
        --remove-unused-variables \
        --in-place \
        --recursive \
        --exclude=__init__.py \
        ./src
        """
    )
    print("{:.<64}\x1b[6;30;42mDone!\x1b[0m".format("black"))
    os.system("black .")
    print("{:.<64}\x1b[6;30;42mDone!\x1b[0m".format("isort"))
    os.system("isort .")


@app.command(name="createsuperuser", help="create super user", add_help_option=True)
def create_super_user(
    email: str = typer.Option("admin@example.com", help="admin email / login name", prompt=True),
    password: str = typer.Option(
        "admin",
        help="admin password",
        prompt=True,
        hide_input=True,
    ),
) -> None:
    from sqlalchemy.orm import Session

    from src.db.session import SessionLocal
    from src.user.crud import user_crud
    from src.user.schemas import CreateUserSchema

    try:
        # create session
        session: Session = SessionLocal()

        # create admin model
        admin_schema = CreateUserSchema(email=email, password=password)

        # insert admin into database
        user_crud.create_admin(session, obj_in=admin_schema)
    except Exception as e:
        print(f"Operation has failed: {e}")


if __name__ == "__main__":
    app()
