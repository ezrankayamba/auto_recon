import logging as log
log.basicConfig(
    level=log.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        log.FileHandler("logs/auto_recon.log"),
        log.StreamHandler()
    ]
)


def debug(msg=''):
    log.debug(msg)


def info(msg=''):
    log.info(msg)


def error(msg=''):
    log.error(msg)
