import json
import datetime as dt
import os
import time as t
import atexit

TIME_SPEC = "seconds"
OUT_PATH = "../out"  # being lazy here. Should go into .env or config file


def dump_array(array, file, delim=""):
    """ Dumps an array to a given file in json format.
        Arguments:
            array: [object] -> array containing json serializable objects
            file: file descriptor to write to
            delim: str -> delimiter after the array has been dumped
    """
    for entry in array:
        json.dump(entry, file)
        file.write(delim)


def date_to_timestamp_millis(iso_date):
    """ Arguments:
            iso_date: str -> date as a iso string. E.g. 2022-12-01
    """
    date_to_ints = map(lambda x: int(x), iso_date.split("-"))
    with_time = [*date_to_ints, 0, 0, 0]
    return int(dt.datetime(*with_time, tzinfo=dt.timezone.utc).timestamp()) * 1000


def time_now_iso():
    return dt.datetime.now().isoformat(timespec=TIME_SPEC)


def time_now_iso_file_stamp():
    return time_now_iso().replace(":", "-").replace("T", "_")


def time_now_millis():
    return round(t.time() * 1000)


def init_json_array_file(symbol, suffix):
    file = open(os.path.join(OUT_PATH, f"{time_now_iso_file_stamp()}_{symbol}_{suffix}.json"), "a")
    file.write("[")

    def end_stream_write(f):
        f.write("]")
        f.close()

    atexit.register(end_stream_write, file)
    return file
