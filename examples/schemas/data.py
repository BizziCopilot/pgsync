import json

import click
import sqlalchemy as sa
from schema import Child, Parent
from sqlalchemy.orm import sessionmaker

from pgsync.base import pg_engine, subtransactions
from pgsync.helper import teardown
from pgsync.utils import get_config


@click.command()
@click.option(
    "--config",
    "-c",
    help="Schema config",
    type=click.Path(exists=True),
)
def main(config):

    config: str = get_config(config)
    teardown(drop_db=False, config=config)
    documents = json.load(open(config))
    engine: sa.engine.Engine = pg_engine(
        database=documents[0].get("database", documents[0]["index"])
    )
    Session = sessionmaker(bind=engine, autoflush=True)
    session = Session()
    with subtransactions(session):
        session.add_all(
            [
                Parent(id=1, name="Parent A"),
                Parent(id=2, name="Parent B"),
                Parent(id=3, name="Parent C"),
            ]
        )
    with subtransactions(session):
        session.add_all(
            [
                Child(id=1, name="Child A Parent A", parent_id=1),
                Child(id=2, name="Child B Parent A", parent_id=2),
                Child(id=3, name="Child C Parent B", parent_id=3),
            ]
        )


if __name__ == "__main__":
    main()
