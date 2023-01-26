import sys

# run script from the src directory
sys.path.append("src")

import os
from typing import Optional

import typer
import uvicorn

# init typer
app = typer.Typer()


@app.command(name="dev", help="run development server", add_help_option=True)
def run_dev_server(
    port: Optional[int] = typer.Option(8000, help="app port number", envvar="PORT"),
    host: Optional[str] = typer.Option("localhost", help="app host", envvar="HOST"),
):
    uvicorn.run("main:app", host=host, port=port, log_level="debug", reload=True)


@app.command(name="prod", help="run production server", add_help_option=True)
def run_prod_server(
    port: Optional[int] = typer.Option(8000, help="app port number", envvar="PORT"),
    host: Optional[str] = typer.Option("0.0.0.0", help="app host", envvar="HOST"),
    workers: Optional[int] = typer.Option(None, help="multiple worker processes"),
):
    uvicorn.run("main:app", host=host, port=port, log_level="info", workers=workers)


@app.command(
    name="makemigrations",
    help="run autogenerate alembic revisions",
    add_help_option=True,
)
def make_migrations(name: Optional[str] = typer.Option(None, help="revision name")):
    command = "alembic revision --autogenerate"

    if name:
        command += f' -m "{name}"'

    os.system(command)


@app.command(name="migrate", help="run migrations", add_help_option=True)
def run_migrate():
    command = "alembic upgrade head"
    os.system(command)


@app.command(name="immigrate", help="undo last migration", add_help_option=True)
def run_migrate_back():
    command = "alembic downgrade -1"
    os.system(command)


@app.command(name="createsuperuser", help="create super user in database", add_help_option=True)
def create_super_user(
    email: Optional[str] = typer.Option(
        "admin@example.com", help="admin email / login name", prompt=True
    ),
    password: Optional[str] = typer.Option(
        "admin",
        help="admin password",
        prompt=True,
        hide_input=True,
    ),
):
    from db.session import SessionLocal
    from user.crud import user_crud
    from user.schemas import CreateUserSchema

    try:
        # create session
        session = SessionLocal()

        # create admin model
        admin_schema = CreateUserSchema(email=email, password=password)

        # insert admin into database
        try:
            user_crud.create_admin(session, obj_in=admin_schema)
        except Exception:
            raise Exception("super user with these parameters already exists")
    except Exception as e:
        print(f"Operation has failed: {e}")


if __name__ == "__main__":
    app()
