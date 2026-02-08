# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\core.py\lifespan.py\database_lifespan_1d5caeeb7bea.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\lifespan\database_lifespan.py

"""

Database lifecycle provider implementation

"""

from typing import Any, Tuple

from fastapi import FastAPI

from core.component.database_connection_provider import DatabaseConnectionProvider

from core.di.decorators import component

from core.di.utils import get_bean_by_type

from core.observation.logger import get_logger

from .lifespan_interface import LifespanProvider

logger = get_logger(__name__)

# @component(name="database_lifespan_provider")


class DatabaseLifespanProvider(LifespanProvider):
    """Database lifecycle provider"""

    def __init__(self, name: str = "database", order: int = 10):
        """

        Initialize the database lifecycle provider

        Args:

            name (str): Provider name

            order (int): Execution order, database usually needs to start first

        """

        super().__init__(name, order)

        self._db_provider = None

    async def startup(self, app: FastAPI) -> Tuple[Any, Any, Any]:
        """

        Start database connection

        Args:

            app (FastAPI): FastAPI application instance

        Returns:

            Tuple[Any, Any, Any]: (connection_pool, checkpointer, db_provider)

        """

        logger.info("Initializing database connection...")

        try:
            # Get database connection provider

            self._db_provider = get_bean_by_type(DatabaseConnectionProvider)

            # Get connection pool and checkpointer

            pool, checkpointer = await self._db_provider.get_connection_and_checkpointer()

            # Store connection pool and checkpointer in app.state for business logic usage

            app.state.connection_pool = pool

            app.state.checkpointer = checkpointer

            app.state.db_provider = self._db_provider

            logger.info("Database connection initialization completed")

            # Return connection information

            return pool, checkpointer, self._db_provider

        except Exception as e:
            logger.error("Error during database initialization: %s", str(e))

            raise

    async def shutdown(self, app: FastAPI) -> None:
        """

        Close database connection

        Args:

            app (FastAPI): FastAPI application instance

        """

        logger.info("Closing database connection...")

        if self._db_provider:
            try:
                await self._db_provider.close()

                logger.info("Database connection closed successfully")

            except Exception as e:
                logger.error("Error while closing database connection: %s", str(e))

        # Clean up database-related attributes in app.state

        for attr in ["connection_pool", "checkpointer", "db_provider"]:
            if hasattr(app.state, attr):
                delattr(app.state, attr)
