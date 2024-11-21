import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

# Configuración de Alembic
config = context.config

# Configuración de logging para Alembic
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    """Obtén la instancia del motor de base de datos desde Flask-SQLAlchemy."""
    try:
        # Compatible con Flask-SQLAlchemy <3 y Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # Compatible con Flask-SQLAlchemy >=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    """Obtén la URL del motor de base de datos."""
    try:
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


# Configura la URL de SQLAlchemy para Alembic
config.set_main_option('sqlalchemy.url', get_engine_url())

# Define los metadatos a usar para la generación automática
target_db = current_app.extensions['migrate'].db


def get_metadata():
    """Obtén los metadatos para la generación automática de migraciones."""
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """Ejecuta las migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta las migraciones en modo online."""

    # Callback para evitar migraciones vacías
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    # Configuración de argumentos adicionales
    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    # Obtén el motor de conexión
    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


# Selección entre modos offline y online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
