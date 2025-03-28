import streamlit as st
import whois
import pandas as pd

def check_domain_availability(domain):
    """
    Checks domain availability.
    Returns True if available, False if registered.
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

def main():
    st.set_page_config(
        page_title="Domain Availability Checker",
        page_icon="🌐",
        layout="wide"
    )
    
    st.title('🔍 Domain Availability Checker')
    
    # Section to upload text file
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
                availability = check_domain_availability(domain)
                results.append({
                    'Domain': domain,
                    'Availability': 'Available' if availability else 'Registered'
                })
                # Update progress bar
                progress_bar.progress((i + 1) / len(domains))
            
            # Create DataFrame to display results
            df = pd.DataFrame(results)
            
            # Color results
            def color_availability(val):
                return 'background-color: green' if val == 'Available' else 'background-color: red'
            
            styled_df = df.style.applymap(color_availability, subset=['Availability'])
            st.dataframe(styled_df)
            
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
    
    # Alternative section to enter domains manually
    st.header('✍️ Check Domains Manually')
    manual_domains = st.text_area('Enter domains (one per line)')
    
    if st.button('Check Manual Domains'):
        if manual_domains:
            domains = [domain.strip() for domain in manual_domains.split('\n') if domain.strip()]
            
            results = []
            progress_bar = st.progress(0)
            for i, domain in enumerate(domains):
                availability = check_domain_availability(domain)
                results.append({
                    'Domain': domain,
                    'Availability': 'Available' if availability else 'Registered'
                })
                # Update progress bar
                progress_bar.progress((i + 1) / len(domains))
            
            # Create and display DataFrame
            df = pd.DataFrame(results)
            
            # Color results
            def color_availability(val):
                return 'background-color: green' if val == 'Available' else 'background-color: red'
            
            styled_df = df.style.applymap(color_availability, subset=['Availability'])
            st.dataframe(styled_df)
            
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
    - Download results in CSV
    
    **Note:** Verification depends on WHOIS server response.
    """)

if __name__ == '__main__':
    main()
