
# Chiasmodon

[![asciicast](https://asciinema.org/a/W3jCmEetvRT6JjrBVDyKtSfbg.svg)](https://asciinema.org/a/W3jCmEetvRT6JjrBVDyKtSfbg)
<p align="center">
<img src="https://badge.fury.io/py/chiasmodon.svg" />
</p>
Chiasmodon is an OSINT (Open Source Intelligence) tool designed to assist in the process of gathering information about target domain. Its primary functionality revolves around searching for domain-related data, including domain emails, domain credentials (usernames and passwords), CIDRs (Classless Inter-Domain Routing), ASNs (Autonomous System Numbers), and subdomains. the tool allows users to search by domain, CIDR, ASN, email, username, password, or Google Play application ID. 




## ✨Features

- [x] **🌐Domain**: Conduct targeted searches by specifying a domain name to gather relevant information related to the domain.
- [x] **🎮Google Play Application**: Search for information related to a specific application on the Google Play Store by providing the application ID.
- [x] **🔎CIDR and 🔢ASN**: Explore CIDR blocks and Autonomous System Numbers (ASNs) associated with the target domain to gain insights into network infrastructure and potential vulnerabilities.
- [x] **✉️Email, 👤Username, 🔒Password**: Conduct searches based on email, username, or password to identify potential security risks or compromised credentials.
- [X] **🌍Country**: Sort and filter search results by country to gain insights into the geographic distribution of the identified information.
- [x] **📋Output Customization**: Choose the desired output format (text, JSON, or CSV) and specify the filename to save the search results.
- [x] **⚙️Additional Options**: The tool offers various additional options, such as viewing different result types (credentials, URLs, subdomains, emails, passwords, usernames, or applications), setting API tokens, specifying timeouts, limiting results, and more.

## 🚀Comming soon

- **📱Phone**: Get ready to uncover even more valuable data by searching for information associated with phone numbers. Whether you're investigating a particular individual or looking for connections between phone numbers and other entities, this new feature will provide you with valuable insights.

- **🏢Company Name**: We understand the importance of comprehensive company research. In our upcoming release, you'll be able to search by company name and access a wide range of documents associated with that company. This feature will provide you with a convenient and efficient way to gather crucial information, such as legal documents, financial reports, and other relevant records.

- **👤Face (Photo)**: Visual data is a powerful tool, and we are excited to introduce our advanced facial recognition feature. With "Search by Face (Photo)," you can upload an image containing a face and leverage cutting-edge technology to identify and match individuals across various data sources. This will allow you to gather valuable information, such as social media profiles, online presence, and potential connections, all through the power of facial recognition.

## Why Chiasmodon name ?
Chiasmodon niger is a species of deep sea fish in the family Chiasmodontidae. It is known for its ability to **swallow fish larger than itself**. and so do we. 😉
![Chiasmodon background](https://journal.voca.network/wp-content/uploads/2017/10/DTR083_1200.png)

## 🔑 Subscription
Join us today and unlock the potential of our cutting-edge OSINT tool. Contact https://t.me/Chiasmod0n on Telegram to subscribe and start harnessing the power of Chiasmodon for your domain investigations.

## ⬇️Install
```bash
pip install chiasmodon
```
## 💻Usage
Chiasmodon provides a flexible and user-friendly command-line interface and python library. Here are some examples to demonstrate its usage:


```
usage: chiasmodon_cli.py [-h] [-d DOMAIN] [-a APP] [-c CIDR] [-s ASN] [-e EMAIL] [-u USERNAME] [-p PASSWORD] [-ep ENDPOINT] [-C COUNTRY]
                         [-vt {cred,url,subdomain,email,password,username,app,endpoint,port}] [-o OUTPUT] [-ot {text,json,csv}] [--init INIT] [-A] [-de] [-T TIMEOUT]
                         [-L LIMIT] [-v]

Chiasmodon CLI

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Search by domain.
  -a APP, --app APP     Search by google play applciton id.
  -c CIDR, --cidr CIDR  Search by CIDR.
  -s ASN, --asn ASN     Search by ASN.
  -e EMAIL, --email EMAIL
                        Search by email, only pro, only pro account.
  -u USERNAME, --username USERNAME
                        Search by username, only pro account.
  -p PASSWORD, --password PASSWORD
                        Search by password, only pro account.
  -ep ENDPOINT, --endpoint ENDPOINT
                        Search by url endpoint.
  -C COUNTRY, --country COUNTRY
                        sort result by country code default is all
  -vt {cred,url,subdomain,email,password,username,app,endpoint,port}, --view-type {cred,url,subdomain,email,password,username,app,endpoint,port}
                        type view the result default is "cred".
  -o OUTPUT, --output OUTPUT
                        filename to save the result
  -ot {text,json,csv}, --output-type {text,json,csv}
                        output format default is "text".
  --init INIT           set the api token.
  -A, --all             view all result using "like",this option work only with (-d or --domain , -a or --app),default is False
  -de, --domain-emails  only result for company domain, this option work only with -d or --domain, default is False
  -T TIMEOUT, --timeout TIMEOUT
                        request timeout default is 60.
  -L LIMIT, --limit LIMIT
                        limit results default is 10000.
  -v, --version         version.

Examples:

    # Search for target domain, you will see the result for only this "example.com"
    chiasmodon_cli.py --domain example.com

    # Search for target subdomains
    chiasmodon_cli.py --domain example.com --all

    # Search for target domain, you will see the result for only this "example.com" on United States
    chiasmodon_cli.py --domain example.com --country US

    # search for target app id
    chiasmodon_cli.py --app com.example

    # Search for target asn
    chiasmodon_cli.py --asn AS123 --type-view cred

    # Search for target username
    chiasmodon_cli.py --username someone --country CA

    # Search for target password
    chiasmodon_cli.py --password example@123

    # Search for target endpoint
    chiasmodon_cli.py --endpoint /wp-login.php

    # Search for target cidr
    chiasmodon_cli.py --cidr x.x.x.x/24

    # Search for target creds by domain emsils
    chiasmodon_cli.py --domain example.com --domain-emails
    chiasmodon_cli.py --domain example.com --domain-emails --output example-creds.json --output-type json
    chiasmodon_cli.py --domain example.com --domain-emails --view-type email --output example-emails.txt --output-type text

    # Search for target subdomain
    chiasmodon_cli.py --domain company.com --view-type subdomain

    # Search for target email
    chiasmodon_cli.py --email someone@example.com
    chiasmodon_cli.py --email someone@example.com --view-type url

    # search for multiple targets:
    chiasmodon_cli.py --domain targets.txt --output example-creds.txt
    chiasmodon_cli.py --domain targets.txt --view-type url --output example-urls.txt
```

***How to use pychiasmodon library***:
```python
from pychiasmodon import Chiasmodon as ch 
token = "PUT_HERE_YOUR_API_KEY"
obj = ch(token)
```
- **Search for target subdomains**:
    - *Command line*
        ```bash
        chiasmodon_cli.py --domain example.com --all
        ```
    - *Python*
        ```python
        result = obj.search('example.com',method='domain', all=True)
        
        for i in result:
            print(i)
        ```

- **Searching for target domain, you will see the result for only this "example.com"**:
    - *Command line*
        ```bash
        chiasmodon_cli.py --domain example.com
        ```
    - *Python*
        ```python
        result = obj.search('example.com',method='domain')
        
        for i in result:
            print(i)
        ```

- **Searching for target domain, you will see the result for only this "example.com" on United States**:
    - *Command line*
        ```bash
        chiasmodon_cli.py --domain example.com --country US
        ```
    - *Python*
        ```python
        result = obj.search('example.com',method='domain',country="US")
        
        for i in result:
            print(i)
        ```


- **Searching for target application ID on the Google Play Store**:
    - *Command line*
        ```bash
        chiasmodon_cli.py --app com.discord
        ```
    - *Python*
        ```python
        result = obj.search('com.example',method='app')

        for i in result:
            print(i)
        ```

- **Searching for target ASN**:
    - *Command line*
        ```bash
        chiasmodon_cli.py --asn AS123 --view-type cred
        ```
    - *Python*
        ```python
        result = obj.search('AS123',method='asn', view_type='cred')

        for i in result:
            print(i)
        ```


- **earching for target username**:
    - *Command line*
        ```bash
        chiasmodon_cli.py --username someone
        ```
    - *Python*
        ```python
        result = obj.search('someone',method='username')

        for i in result:
            print(i)
        ```

- **Searching for target password**:

    - *Command line*
        ```bash
        chiasmodon_cli.py --password example@123
        ```
    - *Python*
        ```python
        result = obj.search('example@123',method='password')

        for i in result:
            print(i)
        ```

- **Searching for target CIDR**:

    - *Command line*
        ```bash
        chiasmodon_cli.py --cidr x.x.x.x/24
        ```
    - *Python*
        ```python
        result = obj.search('x.x.x.x/24',method='cidr')

        for i in result:
            print(i)
        ```

- **Searching for target credentials by domain emails**:

    - *Command line*
        ```bash
        chiasmodon_cli.py --domain example.com --domain-emails
        ```
    - *Python*
        ```python
        result = obj.search('example.com',method='domain', only_domain_emails=True)

        for i in result:
            print(i)
        ```
- **All methods and view types**:

    | Methods | View Type   |
    |-----------------|-----------------|
    | --domain, --email, --cidr, --app, --asn, --username, --password | --view-type cred        |
    | --cidr, --asn, --email, --username, --password        | --view-type app |       
    | --domain, --email, --cidr, --asn, --username, --password | --view-type url      
    | --domain                                      |--view-type subdomain |
    | --domain, --cidr, --asn, --app                      |--view-type email     | 
    | --domain, --cidr, --app, --asn, --email, --password     |--view-type username  |
    | --domain, --cidr, --app, --asn, --email, --username     |--view-type password  |

Please note that these examples represent only a fraction of the available options and use cases. Refer to the documentation for more detailed instructions and explore the full range of features provided by Chiasmodon.


## 💬 Contributions and Feedback

Contributions and feedback are welcome! If you encounter any issues or have suggestions for improvements, please submit them to the Chiasmodon GitHub repository. Your input will help us enhance the tool and make it more effective for the OSINT community.

## 📜License

Chiasmodon is released under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](https://github.com/chiasmodon/LICENSE.txt) file for more details.

## ⚠️Disclaimer

Chiasmodon is intended for legal and authorized use only. Users are responsible for ensuring compliance with applicable laws and regulations when using the tool. The developers of Chiasmodon disclaim any responsibility for the misuse or illegal use of the tool.

## 📢Acknowledgments

Chiasmodon is the result of collaborative efforts from a dedicated team of contributors who believe in the power of OSINT. We would like to express our gratitude to the open-source community for their valuable contributions and support.

## 🔗Chiasmodon Links

- [🐍 Python Library](https://pypi.org/project/chiasmodon)
- [📱 Mobile (APK)](https://github.com/chiasmod0n/chiasmodon-mobile)
- [🌐 Website](https://chiasmodon.com)
- [💬 Telegram](https://t.me/chiasmod0n)
- [🐦 X/Twitter](https://x.com/chiasmod0n)


[![star time](https://starchart.cc/chiasmod0n/chiasmodon.svg?variant=adaptive)](https://starchart.cc/chiasmod0n/chiasmodon)

