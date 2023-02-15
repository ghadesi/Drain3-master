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
import pathlib
from typing import TypeVar, Union

# .4&-^9)NJff@PwK
# pypi-AgEIcHlwaS5vcmcCJDI0NTRjMDQzLTJiYWItNGQ0MS1iYTQ1LTYyYmQxNGUzYjIyMAACKlszLCI1Mjg0YTQwNC03MzA5LTQ4YmItYTgyYS04MmM5M2RkMDdlOTciXQAABiBWJR2qVfWIk_9bd1q9hyFhZGMqMg9p4CyUpSWMcGNMdg

sys.modules['drain3']
importlib.reload(drain3)

from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
# import drain3

#---------------------------------------------------------------#
#                           Methods                             #
#---------------------------------------------------------------#

# Declare Drain type
Cluster = TypeVar('drain3.cluster.Cluster')


def store_clusters(path: Union[str, os.PathLike], clusters: Cluster) -> None:
    """Store the clusters into the csv file

    Args:
        path (Union[str, os.PathLike]): The path of the csv file
        clusters (Cluster): The Drain3 clusters
    """

    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=':')
        # Add the header
        writer.writerow(["Cluster_ID", "Size", "Template"])
        for cluster in clusters:
            writer.writerow([cluster.cluster_id, cluster.size, cluster.get_template()])


#---------------------------------------------------------------#
#                       Parameter settings                      #
#---------------------------------------------------------------#
persistence_type = "FILE"
# Input log file
in_log_file = "/Users/poly/Downloads/Drain3-master/examples/pure_msgs.csv"
in_log_file = "/Users/poly/Downloads/Drain3-master/examples/final_pure_text (1).csv"
# Result path
path = "/Users/poly/Downloads/Drain3-master/examples/Parsed.csv"

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')

config = TemplateMinerConfig()
config.load(dirname(__file__) + "/drain3.ini")

logger.info(f"Load config from {dirname(__file__) + '/drain3.ini'}")

config.profiling_enabled = True
template_miner = TemplateMiner(config=config)

if not os.path.isfile(in_log_file):
    logger.info(f"--- File {in_log_file} does not exist!")
    exit(-1)

# Fetting the log file
logger.info(f"--- Fetching file: {in_log_file}")
with open(in_log_file) as f:
    lines = f.readlines()

#---------------------------------------------------------------#
#                            Code                               #
#---------------------------------------------------------------#

start_time = time.time()
batch_start_time = start_time
line_count = 0
batch_size = 10000

# This flag is for adding the header of the csv file
header_flag = True

with open(path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    for line in tqdm(lines, desc='--- Processing:', position=0, leave=True, bar_format='{desc:}{percentage:3.0f}%|{bar:20}{r_bar}'):
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

print(f"--- Summary:")
drain_sorted_clusters = sorted(template_miner.drain.clusters, key=lambda it: it.size, reverse=True)

counter = 0
# The type of the cluster is <class 'drain3.cluster.Cluster'>
# (Referece: https://github.com/logpai/Drain3/blob/master/drain3/drain.py)
for cluster in drain_sorted_clusters:
    if cluster.size == 1:
        counter += 1
    # logger.info(cluster)
logger.info(f"We have {counter} clusters with size 1.")

store_clusters_path = dirname(__file__) + "/myResult/Clusters.csv"
store_clusters(store_clusters_path, drain_sorted_clusters)

logger.info(f"We store clusters inside the {store_clusters_path} file.")

# print("Prefix Tree:")
# template_miner.drain.print_tree()
# template_miner.profiler.report(0)
