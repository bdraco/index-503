from pathlib import Path
from threading import Lock, Thread
from time import sleep

import pytest

from index_503.util import exclusive_lock, get_sha256_hash

from . import FIXTURES


def test_get_sha256_hash() -> None:
    metadata_path = FIXTURES.joinpath("METADATA")
    assert (
        get_sha256_hash(metadata_path)
        == "a448e2bbca19bfdb6cd8ed15aa59c05f04e010640d4404dd6c2c062be2336999"
    )


def test_exclusive_lock(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    thread_lock = Lock()

    class LockedRunner(Thread):
        def run(self):
            with exclusive_lock(tmp_path):
                assert thread_lock.acquire(False) is True
                sleep(0.1)
                thread_lock.release()

    thread_1 = LockedRunner()
    thread_2 = LockedRunner()
    thread_3 = LockedRunner()
    thread_1.start()
    thread_2.start()
    thread_3.start()

    assert "Another instance is running" in caplog.text

    thread_1.join()
    thread_2.join()
    thread_3.join()

    assert "Another instance finished, continuing" in caplog.text
