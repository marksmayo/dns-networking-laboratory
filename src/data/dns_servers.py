"""
DNS Server Database and Discovery
"""

import requests
import dns.resolver
import socket
import threading
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class DNSServer:
    name: str
    ip: str
    location: str = ""
    provider: str = ""
    supports_doh: bool = False
    supports_dot: bool = False
    is_responsive: bool = False
    avg_response_time: float = 0.0

class DNSServerDatabase:
    """Manages the list of public DNS servers"""
    
    def __init__(self):
        self.servers = []
        self.load_default_servers()
    
    def load_default_servers(self):
        """Load a comprehensive list of public DNS servers"""
        default_servers = [
            # Google
            DNSServer("Google Primary", "8.8.8.8", "Global", "Google", True, True),
            DNSServer("Google Secondary", "8.8.4.4", "Global", "Google", True, True),
            
            # Cloudflare
            DNSServer("Cloudflare Primary", "1.1.1.1", "Global", "Cloudflare", True, True),
            DNSServer("Cloudflare Secondary", "1.0.0.1", "Global", "Cloudflare", True, True),
            DNSServer("Cloudflare Family", "1.1.1.3", "Global", "Cloudflare", True, True),
            
            # Quad9
            DNSServer("Quad9 Secure", "9.9.9.9", "Global", "Quad9", True, True),
            DNSServer("Quad9 Unsecured", "9.9.9.10", "Global", "Quad9", True, True),
            DNSServer("Quad9 ECS", "9.9.9.11", "Global", "Quad9", True, True),
            
            # OpenDNS
            DNSServer("OpenDNS Home", "208.67.222.222", "US", "OpenDNS", True, False),
            DNSServer("OpenDNS Family Shield", "208.67.222.123", "US", "OpenDNS", True, False),
            
            # AdGuard
            DNSServer("AdGuard Default", "94.140.14.14", "Global", "AdGuard", True, True),
            DNSServer("AdGuard Family", "94.140.14.15", "Global", "AdGuard", True, True),
            DNSServer("AdGuard Non-filtering", "94.140.14.140", "Global", "AdGuard", True, True),
            
            # Control D
            DNSServer("Control D Unfiltered", "76.76.19.19", "Global", "Control D", True, True),
            DNSServer("Control D Malware", "76.76.2.0", "Global", "Control D", True, True),
            
            # DNS.Watch
            DNSServer("DNS.Watch Primary", "84.200.69.80", "Germany", "DNS.Watch", False, False),
            DNSServer("DNS.Watch Secondary", "84.200.70.40", "Germany", "DNS.Watch", False, False),
            
            # Comodo Secure DNS
            DNSServer("Comodo Primary", "8.26.56.26", "US", "Comodo", False, False),
            DNSServer("Comodo Secondary", "8.20.247.20", "US", "Comodo", False, False),
            
            # Level3
            DNSServer("Level3 Primary", "4.2.2.1", "US", "Level3", False, False),
            DNSServer("Level3 Secondary", "4.2.2.2", "US", "Level3", False, False),
            DNSServer("Level3 Tertiary", "4.2.2.3", "US", "Level3", False, False),
            
            # Verisign
            DNSServer("Verisign Primary", "64.6.64.6", "US", "Verisign", False, False),
            DNSServer("Verisign Secondary", "64.6.65.6", "US", "Verisign", False, False),
            
            # NextDNS
            DNSServer("NextDNS Primary", "45.90.28.250", "Global", "NextDNS", True, True),
            DNSServer("NextDNS Secondary", "45.90.30.250", "Global", "NextDNS", True, True),
            
            # CleanBrowsing
            DNSServer("CleanBrowsing Security", "185.228.168.9", "Global", "CleanBrowsing", True, True),
            DNSServer("CleanBrowsing Adult", "185.228.168.10", "Global", "CleanBrowsing", True, True),
            DNSServer("CleanBrowsing Family", "185.228.168.168", "Global", "CleanBrowsing", True, True),
        ]
        
        self.servers = default_servers
    
    def discover_local_dns_servers(self) -> List[DNSServer]:
        """Discover local DNS servers from system configuration"""
        local_servers = []
        
        try:
            # Get system DNS servers
            resolver = dns.resolver.Resolver()
            for server in resolver.nameservers:
                local_servers.append(
                    DNSServer(f"System DNS {server}", server, "Local", "System")
                )
        except Exception:
            pass
        
        # Try common router addresses
        router_ips = ["192.168.1.1", "192.168.0.1", "10.0.0.1", "172.16.0.1"]
        for ip in router_ips:
            try:
                # Quick test if it responds to DNS queries
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [ip]
                resolver.timeout = 2
                resolver.lifetime = 2
                resolver.resolve("google.com", "A")
                local_servers.append(
                    DNSServer(f"Router {ip}", ip, "Local", "Router")
                )
            except Exception:
                pass
        
        return local_servers
    
    def test_server_responsiveness(self, server: DNSServer, timeout: float = 3.0) -> Tuple[bool, float]:
        """Test if a DNS server is responsive and measure response time"""
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [server.ip]
            resolver.timeout = timeout
            resolver.lifetime = timeout
            
            import time
            start_time = time.time()
            resolver.resolve("google.com", "A")
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            return True, response_time
        except Exception:
            return False, float('inf')
    
    def test_all_servers(self, progress_callback=None):
        """Test all servers for responsiveness in parallel"""
        results = {}
        threads = []
        
        def test_server(server):
            is_responsive, response_time = self.test_server_responsiveness(server)
            server.is_responsive = is_responsive
            server.avg_response_time = response_time
            results[server.ip] = (is_responsive, response_time)
            if progress_callback:
                progress_callback(server, is_responsive, response_time)
        
        # Add local servers
        local_servers = self.discover_local_dns_servers()
        self.servers.extend(local_servers)
        
        # Test all servers
        for server in self.servers:
            thread = threading.Thread(target=test_server, args=(server,))
            threads.append(thread)
            thread.start()
        
        # Wait for all tests to complete
        for thread in threads:
            thread.join()
        
        # Sort servers by response time (responsive servers first)
        self.servers.sort(key=lambda s: (not s.is_responsive, s.avg_response_time))
        
        return results
    
    def get_responsive_servers(self) -> List[DNSServer]:
        """Get only the responsive servers"""
        return [server for server in self.servers if server.is_responsive]
    
    def get_servers_by_provider(self, provider: str) -> List[DNSServer]:
        """Get servers by provider name"""
        return [server for server in self.servers if server.provider.lower() == provider.lower()]
    
    def export_server_list(self) -> List[Dict]:
        """Export server list as a list of dictionaries"""
        return [
            {
                "name": server.name,
                "ip": server.ip,
                "location": server.location,
                "provider": server.provider,
                "supports_doh": server.supports_doh,
                "supports_dot": server.supports_dot,
                "is_responsive": server.is_responsive,
                "avg_response_time": server.avg_response_time
            }
            for server in self.servers
        ]