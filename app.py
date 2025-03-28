import streamlit as st
import whois
import pandas as pd
import urllib.parse
import re

class DomainRegistrars:
    """
    Class to manage domain registrar links and pricing
    """
    REGISTRARS = {
        'default': {
            'GoDaddy': "https://www.godaddy.com/domains/search/domain/",
            'Gandi': "https://www.gandi.net/en/domain/search?domain="
        },
        'tld_specific': {
            '.com': {
                'GoDaddy': "https://www.godaddy.com/domains/search/domain/",
                'Gandi': "https://www.gandi.net/en/domain/search?domain="
            },
            '.org': {
                'GoDaddy': "https://www.godaddy.com/domains/search/domain/",
                'Gandi': "https://www.gandi.net/en/domain/create/org"
            },
            '.net': {
                'GoDaddy': "https://www.godaddy.com/domains/search/domain/",
                'Gandi': "https://www.gandi.net/en/domain/create/net"
            }
        }
    }

    @classmethod
    def get_purchase_link(cls, domain, registrar='Gandi'):
        """
        Generate purchase link for a domain
        """
        # Extract TLD
        tld_match = re.search(r'\.[a-z]+$', domain.lower())
        tld = tld_match.group(0) if tld_match else '.com'
        
        # Check TLD-specific registrar links
        if tld in cls.REGISTRARS['tld_specific']:
            registrar_links = cls.REGISTRARS['tld_specific'][tld]
            link = registrar_links.get(registrar, 
                   cls.REGISTRARS['default'][registrar])
        else:
            link = cls.REGISTRARS['default'][registrar]
        
        encoded_domain = urllib.parse.quote(domain)
        return f"{link}{encoded_domain}"

class DomainPriceEstimator:
    """
    Class to estimate domain prices
    Note: This is a mock implementation. In a real-world scenario, 
    you would use a paid API or scraping service.
    """
    @staticmethod
    def estimate_price(domain):
        """
        Estimate domain price based on TLD
        """
        # Basic price mapping
        tld_prices = {
            '.com': {'min': 10, 'max': 20},
            '.org': {'min': 8, 'max': 15},
            '.net': {'min': 9, 'max': 18},
            '.io': {'min': 30, 'max': 50},
            '.co': {'min': 20, 'max': 30},
            'default': {'min': 10, 'max': 20}
        }
        
        # Extract TLD
        tld_match = re.search(r'\.[a-z]+$', domain.lower())
        tld = tld_match.group(0) if tld_match else '.com'
        
        # Get price range
        price_range = tld_prices.get(tld, tld_prices['default'])
        return f"${price_range['min']} - ${price_range['max']}/year"

def check_domain_availability(domain):
    """
    Check domain availability using WHOIS
    """
    try:
        domain_info = whois.whois(domain)
        # If domain information can be retrieved, it's registered
        return False
    except whois.parser.PywhoisError:
        # If no information can be retrieved, the domain is available
        return True
    except Exception as e:
        # Handle other possible errors
        st.error(f"Error checking {domain}: {e}")
        return None

def create_domain_info(domain):
    """
    Create comprehensive domain information
    """
    availability = check_domain_availability(domain)
    
    if availability:
        return {
            'Domain': domain,
            'Availability': 'Available',
            'GoDaddy Link': f'<a href="{DomainRegistrars.get_purchase_link(domain, "GoDaddy")}" target="_blank">Buy on GoDaddy</a>',
            'Gandi Link': f'<a href="{DomainRegistrars.get_purchase_link(domain, "Gandi")}" target="_blank">Buy on Gandi</a>',
            'Estimated Price': DomainPriceEstimator.estimate_price(domain)
        }
    else:
        return {
            'Domain': domain,
            'Availability': 'Registered',
            'GoDaddy Link': '-',
            'Gandi Link': '-',
            'Estimated Price': '-'
        }

# Define color_availability function globally
def color_availability(val):
    """
    Color coding for domain availability
    """
    return 'background-color: green' if val == 'Available' else 'background-color: red'

def main():
    st.set_page_config(
        page_title="Domain Availability Checker",
        page_icon="🌐",
        layout="wide"
    )
    
    st.title('🔍 Domain Availability Checker')
    
    # File upload section
    st.header('📂 Upload Domain File')
    uploaded_file = st.file_uploader('Select a .txt file with domains', 
                                     type=['txt'], 
                                     help='Upload a text file with one domain per line')
    
    # Process domains from uploaded file
    if uploaded_file is not None:
        # Read file contents
        file_contents = uploaded_file.getvalue().decode('utf-8')
        domains = [domain.strip() for domain in file_contents.split('\n') if domain.strip()]
        
        if domains:
            # Check availability of each domain
            results = []
            progress_bar = st.progress(0)
            for i, domain in enumerate(domains):
                domain_info = create_domain_info(domain)
                results.append(domain_info)
                # Update progress bar
                progress_bar.progress((i + 1) / len(domains))
            
            # Create DataFrame to display results
            df = pd.DataFrame(results)
            
            # Use st.markdown to render HTML links
            st.markdown(
                df.style
                .applymap(color_availability, subset=['Availability'])
                .to_html(escape=False),
                unsafe_allow_html=True
            )
            
            # Option to download results
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV Results",
                data=csv,
                file_name='domain_results.csv',
                mime='text/csv'
            )
        else:
            st.warning('No domains found in the file')
    
    # Manual domain entry section
    st.header('✍️ Check Domains Manually')
    manual_domains = st.text_area('Enter domains (one per line)')
    
    if st.button('Check Manual Domains'):
        if manual_domains:
            domains = [domain.strip() for domain in manual_domains.split('\n') if domain.strip()]
            
            results = []
            progress_bar = st.progress(0)
            for i, domain in enumerate(domains):
                domain_info = create_domain_info(domain)
                results.append(domain_info)
                # Update progress bar
                progress_bar.progress((i + 1) / len(domains))
            
            # Create and display DataFrame
            df = pd.DataFrame(results)
            
            # Use st.markdown to render HTML links
            st.markdown(
                df.style
                .applymap(color_availability, subset=['Availability'])
                .to_html(escape=False),
                unsafe_allow_html=True
            )
            
            # Option to download results
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV Results",
                data=csv,
                file_name='domain_results.csv',
                mime='text/csv'
            )

    # Additional information
    st.sidebar.info("""
    ### 🌐 Domain Availability Checker
    - Upload a .txt file with domains
    - Check their availability
    - Get purchase links from multiple registrars
    - View estimated domain prices
    - Download results in CSV
    
    **Note:** 
    - Verification depends on WHOIS server response
    - Prices are estimated approximations
    """)

if __name__ == '__main__':
    main()

# Requirements:
# pip install streamlit python-whois pandas
