from __future__ import with_statement

import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / 'app'))

from app.core.config import settings  # noqa: E402
from app.core.base import Base  # noqa: E402
import app.models  # noqa: F401, E402
from app.core.config import settings  # noqa: F401, E402


def get_sync_url() -> str:
    url = settings.database_url
    if url.startswith('sqlite+aiosqlite'):
        return url.replace('sqlite+aiosqlite', 'sqlite', 1)
    return url


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = get_sync_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration['sqlalchemy.url'] = get_sync_url()

    config.set_main_option('sqlalchemy.url', settings.database_url)

    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
