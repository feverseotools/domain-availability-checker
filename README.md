# 🌐 Domain Availability Checker

## Description
Web tool to quickly and easily check domain availability.

## Features
- 📂 Upload .txt file with domains
- 🔍 Availability verification
- 📥 Download results in CSV

## How to Use
1. Prepare a .txt file with domains (one domain per line)
2. Upload the file to the application
3. View availability results
4. Download report in CSV

## Local Installation
```bash
pip install streamlit python-whois pandas
streamlit run app.py
```

## Domain File Example
```
google.com
example.org
available.net
```

## Deployment
Compatible with Streamlit Cloud and GitHub Codespaces

## Limitations
- Verification depends on WHOIS server response
- Some domains may require more time to verify

## License
[Specify License]
