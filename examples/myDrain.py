import json
import logging
import os
import sys
from os.path import dirname
import csv
from tqdm import tqdm

from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig

persistence_type = "FILE"

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')

if persistence_type == "KAFKA":
    from drain3.kafka_persistence import KafkaPersistence

    persistence = KafkaPersistence("drain3_state", bootstrap_servers="localhost:9092")

elif persistence_type == "FILE":
    from drain3.file_persistence import pub

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

in_log_file = "/Users/poly/Downloads/Drain3-master/examples/pure_msgs.csv"
if not os.path.isfile(in_log_file):
    logger.info(f"File {in_log_file} does not exist!")
    exit(-1)

logger.info(f"Fetching file: {in_log_file}")
with open(in_log_file) as f:
    lines = f.readlines()

# Result path
path = "/Users/poly/Downloads/Drain3-master/examples/Parsed.csv"

# while True:
with open(in_log_file) as f:
    lines = f.readlines()

flag = True

with open(path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    for line in tqdm(lines, desc='Line Progress Bar'):
        line = line.rstrip()
        # Result has the Dic type
        result = template_miner.add_log_message(line)
        print(type(result))
        print("er", result)
        result_json = json.dumps(result)
        dic = json.loads(result_json)
        print("salma", dic)
        if flag:
            keys = list(dic.keys())
            print(keys)
            writer.writerow(keys)
            flag = False
        writer.writerow(list(dic.values()))
        break
