import typer
import uvicorn
from typing import Optional

app = typer.Typer()


@app.command(name="dev", help="run development server", add_help_option=True)
def run_dev_server(
    port: Optional[int] = typer.Option(8000, help="app port number", envvar="PORT"),
    host: Optional[str] = typer.Option("localhost", help="app host", envvar="HOST"),
):
    uvicorn.run("src.main:app", host=host, port=port, log_level="debug", reload=True)


@app.command(name="prod", help="run production server", add_help_option=True)
def run_prod_server(
    port: Optional[int] = typer.Option(8000, help="app port number", envvar="PORT"),
    host: Optional[str] = typer.Option("0.0.0.0", help="app host", envvar="HOST"),
    workers: Optional[int] = typer.Option(None, help="multiple worker processes"),
):
    uvicorn.run("src.main:app", host=host, port=port, log_level="info", workers=workers)


def run():
    app()


if __name__ == "__main__":
    run()
