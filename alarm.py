import argparse
import psutil as ps
import requests as rq
import time

def flag_parse() -> tuple:
    """
    flag_parse function is used to set up parser for parsing command line flags and arguments
    and returns a tuple containing the api_url, memory threshold and time interval
    """
    parser = argparse.ArgumentParser(description="Take arguments needed to monitor memory consumption")
    parser.add_argument('api_url', type=str, help="Required argument for passing the api_url")
    parser.add_argument('mem_thresh', type=int, help="Required argument for limiting memory consumption in bytes")
    parser.add_argument('--interval', type=int, default=60,
                        help="Optional argument for passing the interval in seconds checking memory consumption. Default value is 60 seconds")

    args = parser.parse_args()
    return args.api_url, args.mem_thresh, args.interval


def alert(api_url: str, memory_threshold: int, interval: int ):
    """
    alert function takes three parameters, api_url, memory threshold, interval. It gets
    the memory in bytes used and compares if memory used is larger than memory threshold.
    If memory used is larger a post request is sent to the api_url of memory consumption
    and does the whole process after inputted time(seconds)
    """
    while True:
        # Get the current memory usage
        memory_usage = ps.virtual_memory().used

        if memory_usage > memory_threshold:
            # Memory usage exceeds the threshold, send an HTTP request to the API
            payload = {'message': f'Memory consumption exceeded threshold: {memory_usage} bytes'}
            headers = {'Content-Type': 'application/json'}

            try:
                response = rq.post(api_url, json=payload, headers=headers)

                if response.status_code == 200:
                    print("HTTP request sent successfully.")
                else:
                    print(f"Failed to send HTTP request. Status code: {response.status_code}")
            except rq.exceptions.RequestException as e:
                print(f"Failed to send HTTP request: {str(e)}")

        # Check memory usage every 60 seconds (adjust the interval as needed)
        time.sleep(interval)


if __name__  == '__main__':
    api_uri, mem_thresh, duration = flag_parse()
    alert(api_uri, mem_thresh, duration)
