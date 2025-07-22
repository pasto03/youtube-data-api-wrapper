from dataclasses import dataclass
from googleapiclient.errors import HttpError
from typing import Optional

@dataclass
class HttpErrorContainer:
    """
    A container of HttpError for easier access to error
    """
    code: int = None
    message: Optional[str] = None
    domain: Optional[str] = None
    reason: Optional[str] = None
    location: Optional[str] = None
    locationType: Optional[str] = None
    uri: Optional[str] = None
    error: Optional[HttpError] = None

    @classmethod
    def from_http_error(cls, error: HttpError) -> "HttpErrorContainer":
        details = error.error_details[0] if error.error_details else {}
        return cls(
            code=error.status_code,
            message=details.get("message"),
            domain=details.get("domain"),
            reason=details.get("reason"),
            location=details.get("location"),
            locationType=details.get("locationType"),
            uri=getattr(error, "uri", None),
            error=error,
        )