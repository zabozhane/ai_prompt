import typer

from ai_context.cli.commands_init import init_command

app = typer.Typer(
    help="CLI-first AI context generation tool.",
    no_args_is_help=True,
)


@app.callback()
def app_callback() -> None:
    """Root command group for ai-context."""
    return None

app.command("init")(init_command)
