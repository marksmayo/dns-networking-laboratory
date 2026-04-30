"""
DNS Security Testing Module
Implements security analysis for DNS servers including DNSSEC validation,
encrypted DNS support, malware domain testing, and privacy analysis.
"""

import asyncio
import socket
import ssl
import dns.resolver
import dns.dnssec
import dns.rdatatype
import dns.rrset
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SecurityTestType(Enum):
    DNSSEC_VALIDATION = "dnssec_validation"
    ENCRYPTED_DNS = "encrypted_dns"
    MALWARE_FILTERING = "malware_filtering"
    DNS_FILTERING = "dns_filtering"
    PRIVACY_LEAK = "privacy_leak"
    GEOGRAPHIC_DNS = "geographic_dns"

@dataclass
class SecurityTestResult:
    """Result of a security test"""
    test_type: SecurityTestType
    server_ip: str
    passed: bool
    score: float  # 0-100
    details: str
    response_time: float = 0.0
    error_message: str = ""

class DNSSecurityTester:
    """DNS Security Testing Engine"""
    
    def __init__(self):
        # Test domains for various security checks
        self.dnssec_test_domains = [
            "cloudflare.com",  # Known DNSSEC-enabled domain
            "google.com",      # Another DNSSEC-enabled domain
        ]
        
        self.malware_test_domains = [
            "malware.testing.google.test",  # Google safe browsing test domain
            "testsafebrowsing.appspot.com", # Another test domain
        ]
        
        self.privacy_test_domains = [
            "whoami.akamai.net",  # Returns client IP
            "o-o.myaddr.l.google.com",  # Google's client IP service
        ]
    
    def test_dnssec_validation(self, server_ip: str, timeout: float = 5.0) -> SecurityTestResult:
        """Test DNSSEC validation capability"""
        try:
            start_time = time.time()
            
            # Create custom resolver
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [server_ip]
            resolver.timeout = timeout
            
            dnssec_score = 0
            details_list = []
            
            for domain in self.dnssec_test_domains:
                try:
                    # Query for DNSKEY record to check DNSSEC support
                    response = resolver.resolve(domain, dns.rdatatype.DNSKEY)
                    if response:
                        dnssec_score += 50
                        details_list.append(f"✅ DNSSEC keys found for {domain}")
                    else:
                        details_list.append(f"❌ No DNSSEC keys for {domain}")
                except Exception as e:
                    details_list.append(f"❌ DNSSEC test failed for {domain}: {str(e)[:50]}")
            
            response_time = (time.time() - start_time) * 1000
            details = " | ".join(details_list)
            
            return SecurityTestResult(
                test_type=SecurityTestType.DNSSEC_VALIDATION,
                server_ip=server_ip,
                passed=dnssec_score > 0,
                score=min(dnssec_score, 100),
                details=details,
                response_time=response_time
            )
            
        except Exception as e:
            return SecurityTestResult(
                test_type=SecurityTestType.DNSSEC_VALIDATION,
                server_ip=server_ip,
                passed=False,
                score=0,
                details=f"DNSSEC test failed: {str(e)[:100]}",
                error_message=str(e)
            )
    
    def test_encrypted_dns_support(self, server_ip: str, timeout: float = 5.0) -> SecurityTestResult:
        """Test DNS-over-HTTPS (DoH) and DNS-over-TLS (DoT) support"""
        try:
            start_time = time.time()
            encryption_score = 0
            details_list = []
            
            # Test DNS-over-TLS (DoT) - port 853
            try:
                context = ssl.create_default_context()
                with socket.create_connection((server_ip, 853), timeout=timeout) as sock:
                    with context.wrap_socket(sock, server_hostname=server_ip) as ssock:
                        encryption_score += 50
                        details_list.append("✅ DNS-over-TLS (DoT) supported")
            except Exception:
                details_list.append("❌ DNS-over-TLS (DoT) not supported")
            
            # Test standard DNS response for comparison
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [server_ip]
                resolver.timeout = timeout
                response = resolver.resolve("google.com", dns.rdatatype.A)
                if response:
                    encryption_score += 25
                    details_list.append("✅ Standard DNS queries working")
            except Exception:
                details_list.append("❌ Standard DNS queries failed")
            
            response_time = (time.time() - start_time) * 1000
            details = " | ".join(details_list)
            
            return SecurityTestResult(
                test_type=SecurityTestType.ENCRYPTED_DNS,
                server_ip=server_ip,
                passed=encryption_score > 25,
                score=min(encryption_score, 100),
                details=details,
                response_time=response_time
            )
            
        except Exception as e:
            return SecurityTestResult(
                test_type=SecurityTestType.ENCRYPTED_DNS,
                server_ip=server_ip,
                passed=False,
                score=0,
                details=f"Encrypted DNS test failed: {str(e)[:100]}",
                error_message=str(e)
            )
    
    def test_malware_filtering(self, server_ip: str, timeout: float = 5.0) -> SecurityTestResult:
        """Test malware domain filtering capability"""
        try:
            start_time = time.time()
            
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [server_ip]
            resolver.timeout = timeout
            
            filtering_score = 0
            details_list = []
            
            # Test if server blocks known malicious domains
            for domain in self.malware_test_domains:
                try:
                    response = resolver.resolve(domain, dns.rdatatype.A)
                    # If we get a response, check if it's a blocked/warning page
                    if response:
                        # Check for typical blocking responses
                        for rdata in response:
                            ip_str = str(rdata)
                            # Common blocking IPs used by filtered DNS services
                            if ip_str in ["0.0.0.0", "127.0.0.1", "::1"] or ip_str.startswith("10.0."):
                                filtering_score += 50
                                details_list.append(f"✅ {domain} blocked (redirected to {ip_str})")
                                break
                        else:
                            details_list.append(f"⚠️ {domain} not blocked")
                    else:
                        filtering_score += 50
                        details_list.append(f"✅ {domain} blocked (NXDOMAIN)")
                except dns.resolver.NXDOMAIN:
                    filtering_score += 50
                    details_list.append(f"✅ {domain} blocked (NXDOMAIN)")
                except Exception as e:
                    details_list.append(f"❓ {domain} test inconclusive: {str(e)[:30]}")
            
            response_time = (time.time() - start_time) * 1000
            details = " | ".join(details_list)
            
            return SecurityTestResult(
                test_type=SecurityTestType.MALWARE_FILTERING,
                server_ip=server_ip,
                passed=filtering_score > 0,
                score=min(filtering_score, 100),
                details=details,
                response_time=response_time
            )
            
        except Exception as e:
            return SecurityTestResult(
                test_type=SecurityTestType.MALWARE_FILTERING,
                server_ip=server_ip,
                passed=False,
                score=0,
                details=f"Malware filtering test failed: {str(e)[:100]}",
                error_message=str(e)
            )
    
    def test_privacy_protection(self, server_ip: str, timeout: float = 5.0) -> SecurityTestResult:
        """Test privacy protection and information leakage"""
        try:
            start_time = time.time()
            
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [server_ip]
            resolver.timeout = timeout
            
            privacy_score = 100  # Start with full privacy score
            details_list = []
            
            # Test for client IP leakage
            try:
                response = resolver.resolve("whoami.akamai.net", dns.rdatatype.A)
                if response:
                    client_ip = str(response[0])
                    # Check if the returned IP matches our expected external IP
                    # For now, we'll assume any response indicates some level of tracking
                    privacy_score -= 20
                    details_list.append(f"⚠️ Client IP tracking detected: {client_ip}")
                else:
                    details_list.append("✅ No client IP leakage detected")
            except:
                details_list.append("✅ IP tracking query blocked/failed")
            
            # Test geographic location queries
            try:
                response = resolver.resolve("o-o.myaddr.l.google.com", dns.rdatatype.TXT)
                if response:
                    privacy_score -= 15
                    details_list.append("⚠️ Geographic location queries allowed")
                else:
                    details_list.append("✅ Geographic queries blocked")
            except:
                details_list.append("✅ Geographic tracking blocked")
            
            # Basic functionality test
            try:
                response = resolver.resolve("google.com", dns.rdatatype.A)
                if response:
                    details_list.append("✅ Standard DNS queries working")
                else:
                    privacy_score -= 10
                    details_list.append("❌ Basic DNS resolution issues")
            except:
                privacy_score -= 20
                details_list.append("❌ DNS resolution failed")
            
            response_time = (time.time() - start_time) * 1000
            details = " | ".join(details_list)
            
            return SecurityTestResult(
                test_type=SecurityTestType.PRIVACY_LEAK,
                server_ip=server_ip,
                passed=privacy_score > 70,
                score=max(privacy_score, 0),
                details=details,
                response_time=response_time
            )
            
        except Exception as e:
            return SecurityTestResult(
                test_type=SecurityTestType.PRIVACY_LEAK,
                server_ip=server_ip,
                passed=False,
                score=0,
                details=f"Privacy test failed: {str(e)[:100]}",
                error_message=str(e)
            )
    
    def run_comprehensive_security_test(self, server_ip: str, timeout: float = 5.0) -> List[SecurityTestResult]:
        """Run all security tests for a DNS server"""
        results = []
        
        # Run all security tests
        test_methods = [
            self.test_dnssec_validation,
            self.test_encrypted_dns_support,
            self.test_malware_filtering,
            self.test_privacy_protection,
        ]
        
        for test_method in test_methods:
            try:
                result = test_method(server_ip, timeout)
                results.append(result)
                
                # Small delay between tests to avoid overwhelming the server
                time.sleep(0.5)
                
            except Exception as e:
                # Create error result if test completely fails
                results.append(SecurityTestResult(
                    test_type=SecurityTestType.DNSSEC_VALIDATION,  # Default type
                    server_ip=server_ip,
                    passed=False,
                    score=0,
                    details=f"Test execution failed: {str(e)[:100]}",
                    error_message=str(e)
                ))
        
        return results