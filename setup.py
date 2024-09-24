#!/usr/bin/python3
from distutils.core import setup
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='chiasmodon',
      version='3.0.2',
      description='Chiasmodon is an OSINT tool that allows users to gather information from various sources and conduct targeted searches based on domains, Google Play applications, email addresses, IP addresses, organizations, URLs, and more. It provides comprehensive scanning capabilities, customizable output formats, and additional options for enhanced data analysis and customization.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='chiasmod0n',
      keywords='intelligence osint credentials emails asn cidr bugbounty subdomains information-gathering intelligence-analysis reconnaissance attack-surface subdomain-enumeration reconnaissance-framework bugbounty-tool email-enumeration chiasmodon',
      url='https://github.com/chiasmod0n/chiasmodon',
      packages=['.'],
      scripts=['cli/chiasmodon_cli.py'],
      install_requires=['requests', 'yaspin', 'tldextract','argcomplete']
    ) 
