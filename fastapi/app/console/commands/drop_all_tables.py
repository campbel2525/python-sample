import typer
from sqlalchemy import MetaData, text

from app.helpers import env_helper
from config.settings import db, engine

app = typer.Typer()


@app.command()
def drop_all_tables():
    if not env_helper.is_local():
        typer.echo("ローカル環境以外では実行できません。")
        return

    db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

    metadata = MetaData()
    metadata.reflect(bind=engine)
    tables = metadata.tables
    for table in tables:
        db.execute(text(f"DROP TABLE IF EXISTS {table}"))

    db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    db.commit()


if __name__ == "__main__":
    app()
