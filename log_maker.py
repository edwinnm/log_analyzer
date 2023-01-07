import time
import logging

log_name = "./demo.log"
counter = 1
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.DEBUG)
while True:
    logging.info(' Raw data')
    if counter % 5 == 0:
        logging.info(' Other amazing log')
        time.sleep(10)
    # f.close()    
    time.sleep(1)
    counter = counter + 1


