import typer

from fmconfig.utils import get_graphics_path


app = typer.Typer()


@app.command()
def path() -> None:
    """Print the graphics path."""
    path = get_graphics_path()
    typer.echo(path)


if __name__ == "__main__":
    app()
