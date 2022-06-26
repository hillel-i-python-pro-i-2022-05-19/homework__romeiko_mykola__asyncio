class Crawler:
    def __init__(self, url: str = 'https://example.com', links_limit: int = 100, depth_level: int = 1, subdomain_allowed: bool = False):
        self.url = url
        self.links_limit = links_limit
        self.depth_level = depth_level
        self.subdomain_allowed = subdomain_allowed

    def run(self):
        ...