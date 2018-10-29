import os
import logging
from multiprocessing import Pool

from sink.sink import DataSink

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(threadName)s: %(message)s")

endpoint = os.environ['ENDPOINT']
reducer_spawner_endpoint = os.environ['REDUCER_SPAWNER_ENDPOINT']
collector_endpoint = os.environ['COLLECTOR_ENDPOINT']


def decode_result(result):
    player, points = result.decode().split("#")
    return player, int(points)


def collect_fun(results):
    '''
    Takes a list of pairs (player_name, overall_points) and returns a list of the 10 players with most points achieved.
    '''
    pool = Pool()
    decoded_results = pool.map(decode_result, results)
    decoded_results.sort(key=lambda x: -x[1])
    return decoded_results[:10]


def main():
    logger = logging.getLogger("Sink")
    logger.debug("Start")
    sink = DataSink(endpoint, collector_endpoint)
    sink.start(reducer_spawner_endpoint, collect_fun)
    logger.debug("End")


if __name__ == "__main__":
    main()