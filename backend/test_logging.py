from commons.logger import logger
import logging

# Initialize logger
log = logger("test_logger")


def test_logs():
    import uuid

    run_id = str(uuid.uuid4())
    print(f"Testing logs with Run ID: {run_id}...")
    log.debug(f"[{run_id}] This is a DEBUG message")
    log.info(f"[{run_id}] This is an INFO message")
    log.warning(f"[{run_id}] This is a WARNING message")
    log.error(f"[{run_id}] This is an ERROR message")
    log.critical(f"[{run_id}] This is a CRITICAL message")
    print("Log test complete. Check logs/debug.log")


if __name__ == "__main__":
    test_logs()
