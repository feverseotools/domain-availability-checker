import streamlit as st
import whois
import pandas as pd
import urllib.parse
import re

class DomainTLDs:
    """
    Manage supported Top-Level Domains (TLDs)
    """
    SUPPORTED_TLDS = [
        # Generic TLDs
        '.com', '.org', '.net', '.io', '.co', 
        
        # Country Code TLDs (ccTLDs)
        '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.ar', '.at', '.au', 
        '.ba', '.be', '.bg', '.bo', '.br', '.bw', '.by', '.bz', '.ca', 
        '.cl', '.cn', '.co', '.cr', '.cu', '.cv', '.cz', 
        '.de', '.dk', '.do', '.dz', 
        '.ec', '.ee', '.eg', '.es', 
        '.fi', '.fr', 
        '.ge', '.gh', '.gr', '.gt', 
        '.hk', '.hn', '.ht', '.hu', 
        '.id', '.ie', '.il', '.in', '.iq', '.ir', '.is', '.it', 
        '.jp', 
        '.ke', '.kr', '.kw', '.ky', 
        '.lb', '.li', '.lt', '.lu', '.lv', 
        '.ma', '.mc', '.md', '.me', '.mg', '.mk', '.mm', '.mn', 
        '.mx', '.my', 
        '.na', '.ng', '.ni', '.nl', '.no', '.nz', 
        '.pa', '.pe', '.ph', '.pk', '.pl', '.pt', '.py', 
        '.qa', 
        '.ro', '.rs', '.ru', '.rw', 
        '.sa', '.sc', '.se', '.sg', '.sv', '.sy', 
        '.th', '.tn', '.tr', 
        '.ua', '.ug', '.uk', '.us', '.uy', '.uz', 
        '.ve', '.vn', 
        '.za'
    ]

class DomainRegistrars:
    """
    Class to manage domain registrar links and pricing
    """
    REGISTRARS = {
        'default': {
            'GoDaddy': "https://www.godaddy.com/es-es/domainsearch/find?domainToCheck=",
            'Gandi': "https://shop.gandi.net/en/domain/suggest?search="
        },
        'tld_specific': {
            # You can add specific links for TLDs if needed
            # Example:
            # '.com.br': {
            #     'GoDaddy': "https://www.godaddy.com/es-es/domainsearch/find?domainToCheck=",
            #     'Gandi': "https://shop.gandi.net/en/domain/suggest?search="
            # }
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
            # Generic TLDs
            '.com': {'min': 10, 'max': 20},
            '.org': {'min': 8, 'max': 15},
            '.net': {'min': 9, 'max': 18},
            '.io': {'min': 30, 'max': 50},
            '.co': {'min': 20, 'max': 30},
            
            # Country Code TLDs (prices can vary widely)
            '.uk': {'min': 5, 'max': 15},
            '.us': {'min': 5, 'max': 15},
            '.ca': {'min': 10, 'max': 20},
            '.de': {'min': 5, 'max': 15},
            '.fr': {'min': 5, 'max': 15},
            '.jp': {'min': 10, 'max': 30},
            '.au': {'min': 10, 'max': 25},
            '.br': {'min': 10, 'max': 25},
            
            # Default fallback
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
    # First, validate TLD
    tld_match = re.search(r'\.[a-z]+$', domain.lower())
    if not tld_match or tld_match.group(0) not in DomainTLDs.SUPPORTED_TLDS:
        return None
    
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
    # Validate domain
    tld_match = re.search(r'\.[a-z]+

# Define color_availability function globally
def color_availability(val):
    """
    Color coding for domain availability
    """
    color_map = {
        'Available': 'background-color: green',
        'Registered': 'background-color: red',
        'Unsupported TLD': 'background-color: orange',
        'Error': 'background-color: gray'
    }
    return color_map.get(val, '')

def display_supported_tlds():
    """
    Create a sidebar section to display supported TLDs
    """
    with st.sidebar.expander("🌐 Supported TLDs"):
        # Split TLDs into columns for better readability
        cols = st.columns(4)
        
        # Group TLDs by first letter
        grouped_tlds = {}
        for tld in DomainTLDs.SUPPORTED_TLDS:
            first_letter = tld[1].upper()
            if first_letter not in grouped_tlds:
                grouped_tlds[first_letter] = []
            grouped_tlds[first_letter].append(tld)
        
        # Sort the letters
        sorted_letters = sorted(grouped_tlds.keys())
        
        # Display TLDs in a readable format
        for i, letter in enumerate(sorted_letters):
            with cols[i % 4]:
                st.markdown(f"**{letter}**")
                tld_list = sorted(grouped_tlds[letter])
                st.markdown("\n".join(tld_list))

def main():
    st.set_page_config(
        page_title="Domain Availability Checker",
        page_icon="🌐",
        layout="wide"
    )
    
    st.title('🔍 Domain Availability Checker')
    
    # Display supported TLDs in sidebar
    display_supported_tlds()
    
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
, domain.lower())
    if not tld_match or tld_match.group(0) not in DomainTLDs.SUPPORTED_TLDS:
        return {
            'Domain': domain,
            'Availability': 'Unsupported TLD',
            'GoDaddy Link': '-',
            'Gandi Link': '-',
            'Estimated Price': '-'
        }
    
    availability = check_domain_availability(domain)
    
    if availability is None:
        return {
            'Domain': domain,
            'Availability': 'Error',
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

# Define color_availability function globally
def color_availability(val):
    """
    Color coding for domain availability
    """
    color_map = {
        'Available': 'background-color: green',
        'Registered': 'background-color: red',
        'Unsupported TLD': 'background-color: orange',
        'Error': 'background-color: gray'
    }
    return color_map.get(val, '')

def display_supported_tlds():
    """
    Create a sidebar section to display supported TLDs
    """
    with st.sidebar.expander("🌐 Supported TLDs"):
        # Split TLDs into columns for better readability
        cols = st.columns(4)
        
        # Group TLDs by first letter
        grouped_tlds = {}
        for tld in DomainTLDs.SUPPORTED_TLDS:
            first_letter = tld[1].upper()
            if first_letter not in grouped_tlds:
                grouped_tlds[first_letter] = []
            grouped_tlds[first_letter].append(tld)
        
        # Sort the letters
        sorted_letters = sorted(grouped_tlds.keys())
        
        # Display TLDs in a readable format
        for i, letter in enumerate(sorted_letters):
            with cols[i % 4]:
                st.markdown(f"**{letter}**")
                tld_list = sorted(grouped_tlds[letter])
                st.markdown("\n".join(tld_list))

def main():
    st.set_page_config(
        page_title="Domain Availability Checker",
        page_icon="🌐",
        layout="wide"
    )
    
    st.title('🔍 Domain Availability Checker')
    
    # Display supported TLDs in sidebar
    display_supported_tlds()
    
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
