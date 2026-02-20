
import logging

class MockLogging:
    def trace(self, msg):
        logging.debug(f"[TRACE] {msg}")
    def debug(self, msg):
        logging.debug(msg)
    def info(self, msg):
        logging.info(msg)
    def warning(self, msg):
        logging.warning(msg)
    def error(self, msg):
        logging.error(msg)
    def success(self, msg):
        logging.info(f"[SUCCESS] {msg}")

logging = MockLogging()
