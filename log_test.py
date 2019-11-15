import logging as log

# NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                handlers={log.FileHandler(filename='test.log', mode='a', encoding='utf-8')})

log.debug('-----调试信息[debug]-----')
log.info('-----有用的信息[info]-----')
log.warning('-----警告信息[warning]-----')
log.error('-----错误信息[error]-----')
log.critical('-----严重错误信息[critical]-----')
