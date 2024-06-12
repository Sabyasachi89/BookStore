from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    class for Settings.

    """
    API_ORIGIN: str

    class Config(object):
        """class for config"""
        env_file = ".env"
        orm_mode = True
