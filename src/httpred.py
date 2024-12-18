from mitmproxy import http
import logging
from mitmproxy import http, ctx, flowfilter
import re
class Blocker:

    def load(self, loader):
        # Load default ignore hosts from a file
        default_ignore_hosts = self.load_ignore_hosts_from_file("ignore_hosts.txt")

        loader.add_option(
            name="block_global",
            typespec=bool,
            default=False,
            help="Disable block global option",
        )
        loader.add_option(
            name="tls_version_client_min",
            typespec=str,
            default="TLS1",
            help="Lower bound for TLS version negotiation",
        )

    def request(self, flow: http.HTTPFlow) -> None:
        logging.info("Inside request")
        logging.info(f"Request URL: {flow.request.pretty_url}")

        # Check if the request URL contains "amazon.com"
        if "amazon.com" in flow.request.pretty_url:
            logging.info("Blocking request to amazon.com and sending a blank response")

            # Create a blank response with a 200 status code
            flow.response = http.Response.make(
                200,  # Status code
                b"",  # Empty content
                {"Content-Type": "text/html"}  # Optional headers
            )
    def load_ignore_hosts_from_file(self, file_path):
        """
        Load ignore hosts from the specified file and return them as a space-separated string.
        """
        try:
            with open(file_path, "r") as file:
                domains = [line.strip() for line in file if line.strip()]
                ctx.log.info(f"Loaded ignore hosts from {file_path}: {domains}")
                self.ignore_hosts_patterns = [re.compile(pattern) for pattern in domains]
                return " ".join(domains)
        except FileNotFoundError:
            ctx.log.warning(f"Ignore hosts file not found: {file_path}. Using default patterns.")
            self.ignore_hosts_patterns = [re.compile(pattern) for pattern in ["icloud.com", "apple.com", "mzstatic.com"]]
            return "icloud.com apple.com mzstatic.com"
addons = [Blocker()]
