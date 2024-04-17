#!/usr/bin/python3
import setuptools
from distutils.core import setup
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='chiasmodon',
      version='1.1.1',
      description='Chiasmodon is an OSINT (Open Source Intelligence) tool designed to assist in the process of gathering information about a target domain. Its primary functionality revolves around searching for domain-related data, including domain emails, domain credentials (usernames and passwords), CIDRs (Classless Inter-Domain Routing), ASNs (Autonomous System Numbers), and subdomains..',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='chiasmod0n',
      keywords='intelligence osint credentials emails asn cidr bugbounty subdomains information-gathering intelligence-analysis reconnaissance attack-surface subdomain-enumeration reconnaissance-framework bugbounty-tool email-enumeration chiasmodon',
      url='https://github.com/chiasmod0n/chiasmodon',
      packages=['.'],
      scripts=['cli/chiasmodon_cli.py'],
      install_requires=['requests', 'yaspin', 'tldextract']
     ) 
