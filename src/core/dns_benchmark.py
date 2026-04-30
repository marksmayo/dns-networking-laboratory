"""
DNS Benchmarking Engine
Implements comprehensive DNS performance testing similar to GRC DNS Benchmark
"""

import time
import threading
import random
import statistics
from typing import List, Dict, Callable, Optional, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import dns.resolver
import dns.rdatatype
from src.data.dns_servers import DNSServer

@dataclass
class BenchmarkResult:
    """Individual DNS query result"""
    server_ip: str
    domain: str
    query_type: str
    response_time: float  # in milliseconds
    success: bool
    cached: bool = False
    error_message: str = ""

@dataclass
class ServerStatistics:
    """Comprehensive statistics for a DNS server"""
    server: DNSServer
    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    avg_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    percentile_50: float = 0.0
    percentile_90: float = 0.0
    percentile_95: float = 0.0
    percentile_99: float = 0.0
    cached_avg: float = 0.0
    uncached_avg: float = 0.0
    dot_com_avg: float = 0.0
    reliability_score: float = 0.0
    response_times: List[float] = field(default_factory=list)

class DNSBenchmarkEngine:
    """Advanced DNS benchmarking engine"""
    
    def __init__(self):
        self.is_running = False
        self.results: List[BenchmarkResult] = []
        self.server_stats: Dict[str, ServerStatistics] = {}
        self.progress_callback: Optional[Callable] = None
        self.test_domains = self._load_test_domains()
        self.dot_com_domains = self._load_dot_com_domains()
        
    def _load_test_domains(self) -> List[str]:
        """Load diverse test domains for comprehensive testing"""
        return [
            # Popular websites - reduced list
            "google.com", "facebook.com", "youtube.com", "amazon.com", "wikipedia.org",
            "github.com", "microsoft.com", "apple.com", "cloudflare.com", "reddit.com"
        ]
    
    def _load_dot_com_domains(self) -> List[str]:
        """Load .com domains for specific .com testing"""
        return [
            "google.com", "amazon.com", "microsoft.com", "github.com", "cloudflare.com"
        ]
    
    def perform_dns_query(self, server_ip: str, domain: str, query_type: str = "A", 
                         timeout: float = 5.0, cached: bool = False) -> BenchmarkResult:
        """Perform a single DNS query and measure response time"""
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [server_ip]
            resolver.timeout = timeout
            resolver.lifetime = timeout
            
            # Disable caching for uncached tests
            if not cached:
                resolver.cache = None
            
            start_time = time.perf_counter()
            
            # Perform the query
            if query_type == "A":
                result = resolver.resolve(domain, dns.rdatatype.A)
            elif query_type == "AAAA":
                result = resolver.resolve(domain, dns.rdatatype.AAAA)
            elif query_type == "MX":
                result = resolver.resolve(domain, dns.rdatatype.MX)
            elif query_type == "NS":
                result = resolver.resolve(domain, dns.rdatatype.NS)
            else:
                result = resolver.resolve(domain, dns.rdatatype.A)
            
            response_time = (time.perf_counter() - start_time) * 1000  # Convert to ms
            
            return BenchmarkResult(
                server_ip=server_ip,
                domain=domain,
                query_type=query_type,
                response_time=response_time,
                success=True,
                cached=cached
            )
            
        except Exception as e:
            return BenchmarkResult(
                server_ip=server_ip,
                domain=domain,
                query_type=query_type,
                response_time=float('inf'),
                success=False,
                cached=cached,
                error_message=str(e)
            )
    
    def run_comprehensive_benchmark(self, servers: List[DNSServer], 
                                  num_iterations: int = 10,
                                  max_workers: int = 10,
                                  progress_callback: Optional[Callable] = None):
        """Run comprehensive benchmark testing"""
        self.is_running = True
        self.results.clear()
        self.server_stats.clear()
        self.progress_callback = progress_callback
        
        total_tests = len(servers) * (len(self.test_domains) + len(self.dot_com_domains)) * num_iterations * 2  # x2 for cached/uncached
        completed_tests = 0
        
        # Initialize server statistics
        for server in servers:
            self.server_stats[server.ip] = ServerStatistics(server=server)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for server in servers:
                if not self.is_running:
                    break
                
                # Test regular domains (cached and uncached)
                for domain in self.test_domains:
                    for iteration in range(num_iterations):
                        if not self.is_running:
                            break
                        
                        # Uncached test
                        future = executor.submit(
                            self.perform_dns_query, 
                            server.ip, domain, "A", 2.0, False
                        )
                        futures.append(future)
                        
                        # Cached test (after uncached)
                        future = executor.submit(
                            self.perform_dns_query, 
                            server.ip, domain, "A", 2.0, True
                        )
                        futures.append(future)
                
                # Test .com domains specifically
                for domain in self.dot_com_domains:
                    for iteration in range(num_iterations):
                        if not self.is_running:
                            break
                        
                        future = executor.submit(
                            self.perform_dns_query, 
                            server.ip, domain, "A", 2.0, False
                        )
                        futures.append(future)
            
            # Collect results as they complete
            for future in as_completed(futures):
                if not self.is_running:
                    break
                
                result = future.result()
                self.results.append(result)
                self._update_server_statistics(result)
                
                completed_tests += 1
                if self.progress_callback:
                    progress_percentage = (completed_tests / total_tests) * 100
                    self.progress_callback(progress_percentage, result)
        
        # Calculate final statistics
        self._calculate_final_statistics()
        self.is_running = False
    
    def _update_server_statistics(self, result: BenchmarkResult):
        """Update statistics for a server based on a single result"""
        if result.server_ip not in self.server_stats:
            return
        
        stats = self.server_stats[result.server_ip]
        stats.total_queries += 1
        
        if result.success:
            stats.successful_queries += 1
            stats.response_times.append(result.response_time)
            stats.min_response_time = min(stats.min_response_time, result.response_time)
            stats.max_response_time = max(stats.max_response_time, result.response_time)
        else:
            stats.failed_queries += 1
    
    def _calculate_final_statistics(self):
        """Calculate final statistics for all servers"""
        for server_ip, stats in self.server_stats.items():
            if not stats.response_times:
                continue
            
            # Basic statistics
            stats.avg_response_time = statistics.mean(stats.response_times)
            
            # Percentiles
            sorted_times = sorted(stats.response_times)
            n = len(sorted_times)
            
            if n > 0:
                stats.percentile_50 = sorted_times[int(n * 0.50)] if n > 1 else sorted_times[0]
                stats.percentile_90 = sorted_times[int(n * 0.90)] if n > 9 else sorted_times[-1]
                stats.percentile_95 = sorted_times[int(n * 0.95)] if n > 19 else sorted_times[-1]
                stats.percentile_99 = sorted_times[int(n * 0.99)] if n > 99 else sorted_times[-1]
            
            # Reliability score (percentage of successful queries)
            stats.reliability_score = (stats.successful_queries / stats.total_queries * 100) if stats.total_queries > 0 else 0
            
            # Cached vs uncached averages
            cached_results = [r.response_time for r in self.results 
                            if r.server_ip == server_ip and r.success and r.cached]
            uncached_results = [r.response_time for r in self.results 
                              if r.server_ip == server_ip and r.success and not r.cached]
            
            stats.cached_avg = statistics.mean(cached_results) if cached_results else 0
            stats.uncached_avg = statistics.mean(uncached_results) if uncached_results else 0
            
            # .com domain average
            dotcom_results = [r.response_time for r in self.results 
                            if r.server_ip == server_ip and r.success and r.domain.endswith('.com')]
            stats.dot_com_avg = statistics.mean(dotcom_results) if dotcom_results else 0
    
    def stop_benchmark(self):
        """Stop the running benchmark"""
        self.is_running = False
    
    def get_server_rankings(self, sort_by: str = "avg_response_time") -> List[ServerStatistics]:
        """Get servers ranked by specified metric"""
        stats_list = list(self.server_stats.values())
        
        if sort_by == "avg_response_time":
            return sorted(stats_list, key=lambda s: s.avg_response_time if s.response_times else float('inf'))
        elif sort_by == "reliability_score":
            return sorted(stats_list, key=lambda s: s.reliability_score, reverse=True)
        elif sort_by == "min_response_time":
            return sorted(stats_list, key=lambda s: s.min_response_time if s.response_times else float('inf'))
        elif sort_by == "dot_com_avg":
            return sorted(stats_list, key=lambda s: s.dot_com_avg if s.dot_com_avg > 0 else float('inf'))
        else:
            return stats_list
    
    def export_results(self) -> Dict:
        """Export comprehensive benchmark results"""
        return {
            "total_queries": len(self.results),
            "successful_queries": sum(1 for r in self.results if r.success),
            "failed_queries": sum(1 for r in self.results if not r.success),
            "server_statistics": {
                server_ip: {
                    "server_name": stats.server.name,
                    "total_queries": stats.total_queries,
                    "successful_queries": stats.successful_queries,
                    "failed_queries": stats.failed_queries,
                    "avg_response_time": stats.avg_response_time,
                    "min_response_time": stats.min_response_time,
                    "max_response_time": stats.max_response_time,
                    "percentile_50": stats.percentile_50,
                    "percentile_90": stats.percentile_90,
                    "percentile_95": stats.percentile_95,
                    "percentile_99": stats.percentile_99,
                    "cached_avg": stats.cached_avg,
                    "uncached_avg": stats.uncached_avg,
                    "dot_com_avg": stats.dot_com_avg,
                    "reliability_score": stats.reliability_score
                }
                for server_ip, stats in self.server_stats.items()
            },
            "raw_results": [
                {
                    "server_ip": r.server_ip,
                    "domain": r.domain,
                    "query_type": r.query_type,
                    "response_time": r.response_time,
                    "success": r.success,
                    "cached": r.cached,
                    "error_message": r.error_message
                }
                for r in self.results
            ]
        }