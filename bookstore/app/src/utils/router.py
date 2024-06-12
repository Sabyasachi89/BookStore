from functools import lru_cache
from typing import Any, Callable
from fastapi import APIRouter as FastAPIRouter
from fastapi.types import DecoratedCallable
from app.src.config import Settings


class APIRouter(FastAPIRouter):
    """
    trailing slash support
    FYI: https://github.com/tiangolo/fastapi/issues/2060#issuecomment-770088270

    """

    def api_route(self, path: str, *, include_in_schema: bool = True,
                  **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """
        api_route()

        :param path                  :  path
        :param include_in_schema     :  include_in_schema
        :return                      : decorator
        """

        if path.endswith("/"):
            path = path[:-1]
        add_path = super().api_route(path, include_in_schema=include_in_schema, **kwargs)
        alternate_path = path + "/"
        add_alternate_path = super().api_route(
            alternate_path, include_in_schema=False, **kwargs)

        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            """
            decorator()
            :param func      : func

            :return          : add_path(func)
            """
            add_alternate_path(func)
            return add_path(func)

        return decorator


@lru_cache()
def get_settings():
    """
    get_setting()

    :return:  Settings()
    """
    return Settings()


settings = get_settings()
