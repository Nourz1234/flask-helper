from werkzeug.exceptions import HTTPException
from werkzeug.sansio.response import Response


class AppError(HTTPException):
    code = 500
    description = "Something went wrong."


class ValidationError(AppError):
    code = 400
    description = "Validation error."
    errors: dict[str, list[str]] = None

    def __init__(
        self,
        errors: dict[str, list[str]],
        description: str | None = None,
        response: Response | None = None,
    ) -> None:
        super().__init__(description, response)
        self.errors = errors
