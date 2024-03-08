import unittest


# All tests using the FastAPI test client should extend this class
class TestCaseFastAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Fixes 'ValueError: set_wakeup_fd only works in main thread' bug from asyncio,
        # don't remove must be done on every test file if run separately
        import sys
        import asyncio

        if sys.platform == "win32" and sys.version_info >= (3, 8, 0):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
