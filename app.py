import streamlit as st
import whois
import pandas as pd
import urllib.parse
import re
import socket
import requests

class DomainAvailabilityChecker:
    """
    Advanced domain availability checking
    """
    @staticmethod
    def check_whois(domain):
        """
        Check domain availability using WHOIS
        """
        try:
            domain_info = whois.whois(domain)
            # If domain information can be fully retrieved, it's likely registered
            return not (domain_info.domain_name and domain_info.creation_date)
        except whois.parser.PywhoisError:
            # If no information can be retrieved, the domain might be available
            return True
        except Exception:
            # Fallback to other methods if WHOIS fails
            return None

    @staticmethod
    def check_dns(domain):
        """
        Check if domain resolves to an IP address
        """
        try:
            socket.gethostbyname(domain)
            # If it resolves, domain is likely registered
            return False
        except socket.gaierror:
            # Domain doesn't resolve, might be available
            return True

    @staticmethod
    def check_http_head(domain):
        """
        Check if domain responds to HTTP HEAD request
        """
        try:
            # Prepend http:// to ensure proper URL
            url = f"http://{domain}"
            response = requests.head(url, timeout=3)
            # If it gets a response, domain is likely registered
            return False
        except (requests.ConnectionError, requests.Timeout):
            # No response suggests domain might be available
            return True

    @classmethod
    def check_domain_availability(cls, domain):
        """
        Comprehensive domain availability check
        """
        # Validate TLD
        tld_match = re.search(r'\.[a-z]+$', domain.lower())
        if not tld_match or tld_match.group(0) not in DomainTLDs.SUPPORTED_TLDS:
            return None

        # Multiple check methods
        checks = [
            cls.check_whois(domain),
            cls.check_dns(domain),
            cls.check_http_head(domain)
        ]

        # Determine availability
        # If any method suggests it's available, consider it available
        available_count = sum(1 for check in checks if check is True)
        registered_count = sum(1 for check in checks if check is False)

        if available_count > registered_count:
            return True
        elif registered_count > available_count:
            return False
        else:
            return None

# [Rest of the previous code remains the same, just replace the existing 
# check_domain_availability function with the method above]

def create_domain_info(domain):
    """
    Create comprehensive domain information
    """
    # Validate domain
    tld_match = re.search(r'\.[a-z]+$', domain.lower())
    if not tld_match or tld_match.group(0) not in DomainTLDs.SUPPORTED_TLDS:
        return {
            'Domain': domain,
            'Availability': 'Unsupported TLD',
            'GoDaddy Link': '-',
            'Gandi Link': '-',
            'Estimated Price': '-'
        }
    
    availability = DomainAvailabilityChecker.check_domain_availability(domain)
    
    if availability is None:
        return {
            'Domain': domain,
            'Availability': 'Uncertain',
            'GoDaddy Link': f'<a href="{DomainRegistrars.get_purchase_link(domain, "GoDaddy")}" target="_blank">Check on GoDaddy</a>',
            'Gandi Link': f'<a href="{DomainRegistrars.get_purchase_link(domain, "Gandi")}" target="_blank">Check on Gandi</a>',
            'Estimated Price': DomainPriceEstimator.estimate_price(domain)
        }
    
    return {
        'Domain': domain,
        'Availability': 'Available' if availability else 'Registered',
        'GoDaddy Link': f'<a href="{DomainRegistrars.get_purchase_link(domain, "GoDaddy")}" target="_blank">{"Buy" if availability else "Check"} on GoDaddy</a>',
        'Gandi Link': f'<a href="{DomainRegistrars.get_purchase_link(domain, "Gandi")}" target="_blank">{"Buy" if availability else "Check"} on Gandi</a>',
        'Estimated Price': DomainPriceEstimator.estimate_price(domain)
    }

# Update color_availability function
def color_availability(val):
    """
    Color coding for domain availability
    """
    color_map = {
        'Available': 'background-color: green',
        'Registered': 'background-color: red',
        'Unsupported TLD': 'background-color: orange',
        'Uncertain': 'background-color: gray'
    }
    return color_map.get(val, '')

# [Rest of the previous code remains the same]

# Requirements:
# pip install streamlit python-whois pandas requests
