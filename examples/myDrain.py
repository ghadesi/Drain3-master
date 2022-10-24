import json
import logging
import os
import sys
from os.path import dirname
import csv
from tqdm import tqdm
import time

import importlib
import drain3


# .4&-^9)NJff@PwK
# pypi-AgEIcHlwaS5vcmcCJDI0NTRjMDQzLTJiYWItNGQ0MS1iYTQ1LTYyYmQxNGUzYjIyMAACKlszLCI1Mjg0YTQwNC03MzA5LTQ4YmItYTgyYS04MmM5M2RkMDdlOTciXQAABiBWJR2qVfWIk_9bd1q9hyFhZGMqMg9p4CyUpSWMcGNMdg

sys.modules['drain3']
importlib.reload(drain3)

from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
# import drain3

#---------------------------------------------------------------#
#                       Parameter settings                      #
#---------------------------------------------------------------#
persistence_type = "FILE"
# Input log file
in_log_file = "/Users/poly/Downloads/Drain3-master/examples/pure_msgs.csv"
# Result path
path = "/Users/poly/Downloads/Drain3-master/examples/Parsed.csv"

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')

if persistence_type == "KAFKA":
    from drain3.kafka_persistence import KafkaPersistence

    persistence = KafkaPersistence("drain3_state", bootstrap_servers="localhost:9092")

elif persistence_type == "FILE":
    from drain3.file_persistence import FilePersistence

    persistence = FilePersistence("drain3_state.txt")

elif persistence_type == "REDIS":
    from drain3.redis_persistence import RedisPersistence

    persistence = RedisPersistence(redis_host='', redis_port=25061, redis_db=0, redis_pass='', is_ssl=True, redis_key="drain3_state_key")

else:
    persistence = None

config = TemplateMinerConfig()
config.load(dirname(__file__) + "/drain3.ini")
config.profiling_enabled = True
template_miner = TemplateMiner(persistence, config=config)

if not os.path.isfile(in_log_file):
    logger.info(f"--- File {in_log_file} does not exist!")
    exit(-1)

# Fetting the log file
logger.info(f"--- Fetching file: {in_log_file}")
with open(in_log_file) as f:
    lines = f.readlines()

start_time = time.time()
batch_start_time = start_time
line_count = 0

# This flag is for adding the header of the csv file
header_flag = True

with open(path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    for line in tqdm(lines, desc='Processing:', position=0, leave=True):
        line = line.rstrip()
        result_dic = template_miner.add_log_message(line)
        line_count += 1
        if header_flag:
            keys = list(result_dic.keys())
            writer.writerow(keys)
            header_flag = False
        writer.writerow(list(result_dic.values()))

time_took = time.time() - start_time
rate = line_count / time_took
logger.info(
    f"--- Done processing file in {time_took:.2f} sec. Total of {line_count} lines, rate {rate:.1f} lines/sec, "
    f"{len(template_miner.drain.clusters)} clusters"
)
logger.info(f"--- Summary:")
template_miner.profiler.report(0)
