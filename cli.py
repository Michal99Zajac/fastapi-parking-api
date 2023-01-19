import typer
import sys
import uvicorn
from typing import Optional

# run script from the src directory
sys.path.append("src")

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


if __name__ == "__main__":
    app()
