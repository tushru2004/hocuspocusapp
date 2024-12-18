"""
Basic skeleton of a mitmproxy addon.

Run as follows: mitmproxy -s anatomy.py
"""
import re
import logging
from mitmproxy import ctx, http
import tldextract

class Counter:
    def __init__(self):
        self.num = 0
    IGNORE_HOSTS = ["apple.com", "icloud.com", "mzstatic.com"]

    def request(self, flow):
        self.num = self.num + 1
        logging.info("We've seen %d flows" % self.num)
        logging.info(f"Request URL: {flow.request.host}")
        full_host = flow.request.host
        extracted = tldextract.extract(full_host)
        base_domain = f"{extracted.domain}.{extracted.suffix}"
        logging.info(f"base domain {base_domain}")

        if base_domain in self.IGNORE_HOSTS:
            # Skip handling this request, effectively bypassing the proxy
            logging.info(f"Bypassing proxy for {base_domain}")
            # flow.response = http.HTTPResponse.make(
            #     200,  # You can specify a response code here
            #     b"Request bypassed",  # Optional message for the bypassed request
            #     {"Content-Type": "text/plain"}
            # )
            # Extract the base domain (like 'spotify.com' from 'open.spotify.com')
            # Create a response to bypass the proxy for the specified domains
            # Create a response to bypass the proxy for the specified domains
            response = http.Response.make(
                200,  # Status code
                b"Request bypassed",  # Response body
                {"Content-Type": "text/plain"}  # Response headers
            )
            return

    def load(self, loader):
        # Load default ignore hosts from a file
        #default_ignore_hosts = self.load_ignore_hosts_from_file("ignore_hosts.txt")

        # Load default ignore hosts from a file
        loader.add_option(
            name="block_global",
            typespec=bool,
            default=False,
            help="Disable block global option",
        )
    # def load_ignore_hosts_from_file(self, file_path):
    #     """
    #     Load ignore hosts from the specified file and return them as a space-separated string.
    #     """
    #     try:
    #         with open(file_path, "r") as file:
    #             domains = [line.strip() for line in file if line.strip()]
    #             ctx.log.info(f"Loaded ignore hosts from {file_path}: {domains}")
    #             self.ignore_hosts_patterns = [re.compile(pattern) for pattern in domains]
    #             return " ".join(domains)
    #     except FileNotFoundError:
    #         ctx.log.warning(f"Ignore hosts file not found: {file_path}. Using default patterns.")
    #         self.ignore_hosts_patterns = [re.compile(pattern) for pattern in ["icloud.com", "apple.com", "mzstatic.com"]]
    #         return "icloud.com apple.com mzstatic.com"
addons = [Counter()]