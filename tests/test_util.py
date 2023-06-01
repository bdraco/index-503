from index_503.util import get_sha256_hash

from . import FIXTURES


def test_get_sha256_hash() -> None:
    metadata_path = FIXTURES.joinpath("METADATA")
    assert (
        get_sha256_hash(metadata_path)
        == "a448e2bbca19bfdb6cd8ed15aa59c05f04e010640d4404dd6c2c062be2336999"
    )
