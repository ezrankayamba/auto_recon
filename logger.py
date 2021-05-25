import logging as log
log.basicConfig(filename='auto_recon.log', encoding='utf-8', level=log.DEBUG)


def debug(msg=''):
    log.debug(msg)


def info(msg=''):
    log.info(msg)


def error(msg=''):
    log.error(msg)
