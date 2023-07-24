# ProxyChains Assistant

ProxyChains Config Builder
==========================

This script is a ProxyChains configuration builder that tests the functionality of proxies and generates a proxychains configuration file. It can be used to identify working proxies from a list of proxy addresses and customize the generated configuration file based on user preferences.

Usage
-----
To use the script, run the following command:

```
python pca-config-builder.py -f <input_file> -o <output_file> [options]
```


Arguments:
- `-f, --file`: File containing proxies, one per line (required).
- `-o, --output`: Output file for the generated proxychains configuration (required).

Options:
- `-s, --suppress`: Suppress all output.
- `-w, --workers`: Number of concurrent workers to use (default: 10).
- `-c, --chain-len`: Number of proxies to use in the proxy chain (default: 3).
- `-i, --ignore-cert`: Consider the proxy still good even if a certificate verification error is thrown.
- `-m, --max-list`: Maximum number of working proxies to include in the output file.
- `-v, --verbose`: Print verbose error messages.
- `-p, --proxy-type`: Type of proxy to test (default: socks5). Available options: http, https, socks4, socks5.
- `-u, --test-url`: URL to test the proxy against (default: https://ifconfig.me).

ProxyChains Configuration
-------------------------
The script generates a ProxyChains configuration file based on the tested proxies. The default configuration is a general ProxyChains configuration that can be modified by changing the source code or by editing the generated output file after running the script.

The generated configuration includes options such as `random_chain`, `chain_len`, `proxy_dns`, `remote_dns_subnet`, `tcp_read_time_out`, and `tcp_connect_time_out`. These options can be customized according to the user's preferences.

Functionality
-------------
The script reads the proxy addresses from the input file and tests each proxy by making a request to the specified test URL. If the response is successful (status code 200), the proxy is considered working and added to the generated ProxyChains configuration file. The script uses concurrent workers to test multiple proxies simultaneously, improving performance.

If the `--suppress` option is provided, all output will be suppressed. Otherwise, the script will print informational messages about each proxy being tested, including any errors encountered. The working proxies found will be printed at the end of the execution.

Additionally, the script supports advanced options such as specifying the number of concurrent workers, proxy chain length, and maximum number of working proxies to find. Verbose error messages can be printed with the `--verbose` option.

Note that the script uses a requests session with proxy configuration to make the test requests. It also suppresses warnings related to certificates not trusted.

Examples
--------
1. Test proxies from `input.txt` and generate a ProxyChains configuration file named `proxychains.conf`:
   ```
   python pca-config-builder.py -f input.txt -o proxychains.conf
   ```

2. Test proxies with verbose output and maximum 20 working proxies:
   ```
   python pca-config-builder.py -f input.txt -o proxychains.conf -v -m 20
   ```

3. Test HTTP proxies only:
   ```
   python pca-config-builder.py -f input.txt -o proxychains.conf -p http
   ```

4. Suppress all output and test proxies using socks4:
   ```
   python pca-config-builder.py -f input.txt -o proxychains.conf -s -p socks4
   ```

Customization
-------------
To customize the generated ProxyChains configuration, you have two options:

1. Modify the source code: Open the script in a text editor and modify the ProxyChains configuration options in the `config` list according to your preferences. Save the changes and run the script to generate the updated configuration file.

2. Edit the output file: After running the script and generating the initial ProxyChains configuration file, open the file in a text editor and make the desired changes. Save the changes and use the updated configuration file with ProxyChains.



Proxy Tester
--------------------
The second script serves as a companion to the ProxyChains configuration builder script. It is designed to test the functionality of proxies and identify working proxies from a list so you can just pipe it over to your ProxyChains config

Usage
-----
To use the script, run the following command:

```
python pca-tester.py -f <input_file> [options]
```

Arguments:
- `-f, --file`: File containing proxies, one per line (required).

Options:

- `-w, --workers`: Number of concurrent workers to use (default: 10).
- `-i, --ignore-cert`: Consider the proxy still good even if a certificate verification error is thrown.
- `-p, --proxy-type`: Type of proxy to test (default: socks5). Available options: http, https, socks4, socks5.
- `-u, --test-url`: URL to test the proxy against (default: https://ifconfig.me).
- `-o, --output-file`: Output file for working proxies.
- `-m, --max-list`: Maximum number of working proxies to find.
- `-v, --verbose`: Print verbose error messages.
- 
Functionality
-------------
The script reads a list of proxies from the input file and tests each proxy by making a request to the specified test URL. If the response is successful (status code 200), the proxy is considered working and its details (proxy type, IP, and port) are printed to standard output.

Additionally, the script provides several options to customize the testing process. You can specify the number of concurrent workers to use, the type of proxy to test (e.g., HTTP, HTTPS, SOCKS4, or SOCKS5), the test URL to use, an output file to store the working proxies, the maximum number of working proxies to find, and the verbosity level for error messages.

The script uses a threaded approach with concurrent workers, allowing for efficient testing of multiple proxies simultaneously. Proxy testing is performed asynchronously, improving performance.

Note that the script uses a requests session with proxy configuration to make the test requests. It also suppresses warnings related to certificates not trusted.

Examples
--------
1. Test proxies from `input.txt` and print working proxies to standard output:
   ```
   python pca-tester.py -f input.txt
   ```

2. Test proxies and save the working proxies to `output.txt`:
   ```
   python pca-tester.py -f input.txt -o output.txt
   ```

3. Test HTTPS proxies with verbose error messages:
   ```
   python pca-tester.py -f input.txt -p https -v
   ```

4. Test proxies and limit the number of working proxies to 20:
   ```
   python pca-tester.py -f input.txt -m 20
   ```

Customization
-------------
The script provides various options to customize the proxy testing process according to your needs. You can modify the number of concurrent workers, specify the proxy type to test, set a different test URL, choose an output file to store the working proxies, limit the maximum number of working proxies to find, and control the verbosity of error messages.

Feel free to adjust the script according to your requirements, such as modifying the default values or extending its functionality.

License
-------
This script is released under the MIT License. Feel free to modify and distribute it according to your needs.
