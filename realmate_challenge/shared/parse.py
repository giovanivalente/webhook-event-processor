from uuid import UUID

from realmate_challenge.shared.exception import RealmateAPIError


def parse_uuid(value: str) -> UUID:
    try:
        return UUID(value)
    except (ValueError, TypeError) as error:
        raise RealmateAPIError(detail='Invalid UUID format.') from error
