import typer

from app.helpers import env_helper
from database import seeders

app = typer.Typer()


@app.command()
def seeds():
    if not env_helper.is_local():
        typer.echo("ローカル環境以外では実行できません。")
        return

    seeders.UserSeeder().handle()


if __name__ == "__main__":
    app()
