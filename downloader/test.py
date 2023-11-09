from error_logger import Logger

log = Logger()
log.open()
log.log("intuit_tid", "testing 1")
log.log("intuit_tid", "testing 2")
log.log("intuit_tid", "testing 3")
log.close()