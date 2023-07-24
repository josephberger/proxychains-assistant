#!/usr/bin/env python3
import argparse
import requests
import concurrent.futures
import warnings
import re
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress warnings related to certificate not trusted
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='File containing proxies, one per line', required=True)
parser.add_argument('-w', '--workers', type=int, default=10, help='Number of concurrent workers to use, default is 10')
parser.add_argument('-i', '--ignore-cert', action='store_true', help='Consider the proxy still good even if a certificate verification error is thrown.')
parser.add_argument('-p', '--proxy-type', choices=['http', 'https', 'socks4', 'socks5'], default='socks5', help='Type of proxy to test (default: socks5)')
parser.add_argument('-u', '--test-url', default='https://ifconfig.me', help='URL to test the proxy against (default: https://ifconfig.me)')
parser.add_argument('-o', '--output-file', help='Output file for working proxies')
parser.add_argument('-m', '--max-list', type=int, default=None, help='Maximum number of working proxies to find')
parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose error messages')
args = parser.parse_args()

# Validate the test URL
if not re.match(r'^(https?://)?(?:[-\w.]|(?:%[\da-fA-F]{2}))+$', args.test_url):
    raise ValueError('Invalid test URL format')

working_proxies = []

# Read proxies from file
with open(args.file, 'r') as f:
    proxies = [line.strip() for line in f]

# Open output file in append mode
output_file = None
if args.output_file:
    output_file = open(args.output_file, 'a')

def test_proxy(proxy):
    # Set up the proxy URL for requests
    proxy_url = f"{args.proxy_type}://{proxy}"

    # Set up the requests session with the proxy
    session = requests.Session()
    session.proxies = {
        "http": proxy_url,
        "https": proxy_url
    }

    # Check if the maximum number of working proxies is reached
    if args.max_list and len(working_proxies) >= args.max_list:
        return

    try:
        # Make a request to the test URL to test the proxy
        response = session.get(args.test_url, timeout=5, verify=not args.ignore_cert)

        # If the response is successful, add the proxy to the working_proxies list
        if response.status_code == 200:
            working_proxy = f"{args.proxy_type} {proxy.replace(':',' ')}"
            print(working_proxy)
            if output_file:
                output_file.write(working_proxy + '\n')
            working_proxies.append(working_proxy)
    except requests.exceptions.Timeout:
        if args.verbose:
            print(f"[-] {proxy} timed out.", file=sys.stderr)
        pass
    except requests.exceptions.RequestException as e:
        if args.verbose:
            print(f"[-] {proxy} encountered an error: {str(e)}", file=sys.stderr)
        pass
    except Exception as e:
        if args.verbose:
            print(f"[-] {proxy} encountered an unexpected error: {str(e)}", file=sys.stderr)
        pass

with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
    # Submit a separate thread for each proxy to test
    futures = [executor.submit(test_proxy, proxy) for proxy in proxies]

    # Wait for all threads to finish
    concurrent.futures.wait(futures)

# Close the output file if it was opened
if output_file:
    output_file.close()
