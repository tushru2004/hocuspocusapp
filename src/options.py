import re
import logging
from mitmproxy import http, ctx, flowfilter

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AddHeader:
    filter: flowfilter.TFilter

    def __init__(self):
        self.num = 0
        self.ignore_hosts_patterns = []

    def configure(self, updated):
        if "flowfilter" in updated:
            self.filter = flowfilter.parse(".")

    def load(self, loader):
        # Load default ignore hosts from a file
        default_ignore_hosts = self.load_ignore_hosts_from_file("ignore_hosts.txt")

        loader.add_option(
            name="addheader",
            typespec=bool,
            default=False,
            help="Add a count header to responses",
        )
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
        loader.add_option(
            name="ignore_hosts",
            typespec=str,
            default=default_ignore_hosts,
            help="Ignore hosts for SSL interception. Provide space-separated patterns.",
        )
        loader.add_option(
            name="console_eventlog_verbosity",
            typespec=str,
            default="debug",
            help="Set the verbosity of console event logs.",
        )
        loader.add_option("flowfilter", str, "", "Check that flow matches filter.")

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

    def request(self, flow: http.HTTPFlow) -> None:
        """
        Log the request URL and modify the request if needed.
        """
        logging.info("Inside request")  # Logs at INFO level
        logging.info(f"Request URL: {flow.request.pretty_url}")  # Logs the URL
        ctx.log.info("Inside request")
        ctx.log.info(f"Request URL: {flow.request.pretty_url}")

        # Optionally modify the request if needed
        if flow.request.pretty_url == "https://www.jet.com":
            flow.response = http.Response.make(
                200,  # Status code
                b"Hello World",  # Content
                {"Content-Type": "text/html"},  # Headers
            )

    def response(self, flow: http.HTTPFlow) -> None:
        """
        Log and process the response if it matches the filter.
        """
        if flowfilter.match(self.filter, flow):
            logging.info("Flow matches filter:")
            logging.info(flow)

# Register the addon
addons = [AddHeader()]
