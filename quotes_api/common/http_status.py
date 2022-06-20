"""Custom Http Status Codes."""

from enum import Enum


class HttpStatus(Enum):
    """HttpStatus Mapper Enum."""

    CONTINUE_100 = 100
    SWITCHING_PROTOCOLS_101 = 101
    OK_200 = 200
    CREATED_201 = 201
    ACCEPTED_202 = 202
    NON_AUTHORITATIVE_INFORMATION_203 = 203
    NO_CONTENT_204 = 204
    RESET_CONTENT_205 = 205
    PARTIAL_CONTENT_206 = 206
    MULTIPLE_CHOICES_300 = 300
    MOVED_PERMANENTLY_301 = 301
    FOUND_302 = 302
    SEE_OTHER_303 = 303
    NOT_MODIFIED_304 = 304
    USE_PROXY_305 = 305
    RESERVED_306 = 306
    TEMPORARY_REDIRECT_307 = 307
    BAD_REQUEST_400 = 400
    UNAUTHORIZED_401 = 401
    PAYMENT_REQUIRED_402 = 402
    FORBIDDEN_403 = 403
    NOT_FOUND_404 = 404
    METHOD_NOT_ALLOWED_405 = 405
    NOT_ACCEPTABLE_406 = 406
    PROXY_AUTHENTICATION_REQUIRED_407 = 407
    REQUEST_TIMEOUT_408 = 408
    CONFLICT_409 = 409
    GONE_410 = 410
    LENGTH_REQUIRED_411 = 411
    PRECONDITION_FAILED_412 = 412
    REQUEST_ENTITY_TOO_LARGE_413 = 413
    REQUEST_URI_TOO_LONG_414 = 414
    UNSUPPORTED_MEDIA_TYPE_415 = 415
    REQUESTED_RANGE_NOT_SATISFIABLE_416 = 416
    EXPECTATION_FAILED_417 = 417
    PRECONDITION_REQUIRED_428 = 428
    TOO_MANY_REQUESTS_429 = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE_431 = 431
    UNAVAILABLE_FOR_LEGAL_REASONS_451 = 451
    INTERNAL_SERVER_ERROR_500 = 500
    NOT_IMPLEMENTED_501 = 501
    BAD_GATEWAY_502 = 502
    SERVICE_UNAVAILABLE_503 = 503
    GATEWAY_TIMEOUT_504 = 504
    HTTP_VERSION_NOT_SUPPORTED_505 = 505
    NETWORK_AUTHENTICATION_REQUIRED_511 = 511

    @staticmethod
    def is_informational(status_code):
        """Checks if status code is of type informational."""
        return 100 <= status_code.value <= 199

    @staticmethod
    def is_success(status_code):
        """Checks if status code is of type successful."""
        return 200 <= status_code.value <= 299

    @staticmethod
    def is_redirect(status_code):
        """Checks if status code is of redirection type."""
        return 300 <= status_code.value <= 399

    @staticmethod
    def is_client_error(status_code):
        """Checks if status code is of client error type."""
        return 400 <= status_code.value <= 499

    @staticmethod
    def is_server_error(status_code):
        """Checks if status code is of server error type."""
        return 500 <= status_code.value <= 599
