import os


class Settings:
    """
    Centralized runtime configuration.
    All behavior flags must live here.
    """

    ENABLE_SEED_V1: bool = (
        os.getenv("ENABLE_SEED_V1", "false").lower() == "true"
    )

    INIT_DB_ON_STARTUP: bool = (
        os.getenv("INIT_DB_ON_STARTUP", "true").lower() == "true"
    )


settings = Settings()
