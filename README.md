
# Chiasmodon

[![asciicast](https://asciinema.org/a/QrEtBLFMQrjU1sjRjcgTdo41m.svg)](https://asciinema.org/a/QrEtBLFMQrjU1sjRjcgTdo41m)
<p align="center">
<img src="https://badge.fury.io/py/chiasmodon.svg" />
</p>
Chiasmodon is an OSINT tool that allows users to gather information from various sources and conduct targeted searches based on domains, Google Play applications, email addresses, IP addresses, organizations, URLs, and more. It provides comprehensive scanning capabilities, customizable output formats, and additional options for enhanced data analysis and customization.


## ✨Features

- [x] **🌐Domain**: Conduct targeted searches by specifying a domain name to gather relevant information related to the domain.
- [x] **🎮Google Play Application**: Search for information related to a specific application on the Google Play Store by providing the application ID.
- [x] **✉️Email, 👤Username, 🔒Password**: Conduct searches based on email, username, or password to identify potential security risks or compromised credentials.
- [x] **🔍 IP Address**: Perform searches using an IP address to gather information such as geolocation, associated domain names, and historical data.
- [x] **🌍 CIDR**: Search for information related to a specified CIDR (Classless Inter-Domain Routing) block, including IP range details and associated networks.
- [x] **🔢 ASN**: Retrieve information about an Autonomous System Number (ASN), including its owner, associated IP ranges, and network details.
- [x] **🔌 Port**: Search for information about a specific port number, including its common usage, associated services, and potential vulnerabilities.
- [x] **🌐 ISP**: Conduct searches based on an Internet Service Provider (ISP) name to gather information about the ISP, its services, and associated IP ranges.
- [x] **🏢 Organization (ORG)**: Search for information related to a specific organization or company, including its contact details, associated domains, and network infrastructure.
- [x] **🔗 URL Path**: Perform searches based on a specific URL path to gather information about the path, its content, and potential security risks.
- [x] **📞 Phone**: Conduct searches using a phone number to gather information such as the associated owner, location, and any available public records.
- [x] **🔍Scan**: Perform a comprehensive scan on a given company domain name in one click, including finding
  - Related companies.
  - App applications.
  - Ips (`Port, Org, Isp, Asn`).
  - Subdomains.
  - Client credentials (`Email, Username, Password`).
  - Employee credentials (`Email, Username, Password`)
  - URLs (`Domain/IP, Port, Endpoint`)

- [X] **🌍Country**: Sort and filter search results by country to gain insights into the geographic distribution of the identified information.
- [x] **📋Output Customization**: Choose the desired output format (text, JSON, or CSV) and specify the filename to save the search results.
- [x] **⚙️Additional Options**: The tool offers various additional options, such as viewing different result types (credentials, URLs, subdomains, emails, passwords, usernames, or applications), setting API tokens, specifying timeouts, limiting results, and more.

## 🚀Comming soon

- **🏢Company Name**: We understand the importance of comprehensive company research. In our upcoming release, you'll be able to search by company name and access a wide range of documents associated with that company. This feature will provide you with a convenient and efficient way to gather crucial information, such as legal documents, financial reports, and other relevant records.

- **👤Face (Photo)**: Visual data is a powerful tool, and we are excited to introduce our advanced facial recognition feature. With "Search by Face (Photo)," you can upload an image containing a face and leverage cutting-edge technology to identify and match individuals across various data sources. This will allow you to gather valuable information, such as social media profiles, online presence, and potential connections, all through the power of facial recognition.

## Why Chiasmodon name ?
Chiasmodon niger is a species of deep sea fish in the family Chiasmodontidae. It is known for its ability to **swallow fish larger than itself**. and so do we. 😉
![Chiasmodon background](https://journal.voca.network/wp-content/uploads/2017/10/DTR083_1200.png)

## 🔑 Subscription
Join us today and unlock the potential of our cutting-edge OSINT tool. Contact https://t.me/Chiasmod0n on Telegram to subscribe and start harnessing the power of Chiasmodon for your domain investigations.

## ⬇️Install
```bash
$ pip install chiasmodon
```
Only for linux 👇 
```bash
$ activate-global-python-argcomplete
```
## 💻Usage
Chiasmodon provides a flexible and user-friendly command-line interface and python library. Here are some examples to demonstrate its usage:


```
usage: chiasmodon_cli.py [-h]
                         [-m {cred.username,cred.password,cred.email,cred.phone,cred.email.domain,cred.country,domain,domain.all,ip,ip.asn,ip.isp,ip.org,ip.port,ip.country,app.id,app.name,app.domain,url.path,url.port}]
                         [-vt {full,cred,url,email,phone,password,username,app,domain,ip,related,subdomain}] [-s] [-sr SCAN_RELATED]
                         [-ss SCAN_SUBDOMAINS] [-sa SCAN_APPS] [-si SCAN_IPS] [-sc SCAN_CLIENTS] [-se SCAN_EMPLOYEES] [-o OUTPUT]
                         [-ot {text,json,csv}] [-t TIMEOUT] [-l LIMIT] [-nc] [-lv] [-lm] [--init INIT] [-v]
                         query

Chiasmodon CLI

positional arguments:
  query                 query argument

options:
  -h, --help            show this help message and exit
  -m {cred.username,cred.password,cred.email,cred.phone,cred.email.domain,cred.country,domain,domain.all,ip,ip.asn,ip.isp,ip.org,ip.port,ip.country,app.id,app.name,app.domain,url.path,url.port}, --method {cred.username,cred.password,cred.email,cred.phone,cred.email.domain,cred.country,domain,domain.all,ip,ip.asn,ip.isp,ip.org,ip.port,ip.country,app.id,app.name,app.domain,url.path,url.port}
                        method to search by it,default is "domain".
  -vt {full,cred,url,email,phone,password,username,app,domain,ip,related,subdomain}, --view-type {full,cred,url,email,phone,password,username,app,domain,ip,related,subdomain}
                        type view the result default is "full".
  -s, --scan            scan the company domain (Related company, Clients, Employees, Company ASNs, Company Apps).
  -sr SCAN_RELATED, --scan-related SCAN_RELATED
                        Run related scan, default is yes, Ex: -sr no
  -ss SCAN_SUBDOMAINS, --scan-subdomains SCAN_SUBDOMAINS
                        Run subdomains scan, default is yes, Ex: -ss no
  -sa SCAN_APPS, --scan-apps SCAN_APPS
                        Run App scan, default is yes, Ex: -sa no
  -si SCAN_IPS, --scan-ips SCAN_IPS
                        Run IPs scan, default is yes, Ex: -si no
  -sc SCAN_CLIENTS, --scan-clients SCAN_CLIENTS
                        Run clients scan, default is yes, Ex: -sc no
  -se SCAN_EMPLOYEES, --scan-employees SCAN_EMPLOYEES
                        Run employees scan, default is yes, Ex: -se no
  -o OUTPUT, --output OUTPUT
                        filename to save the result
  -ot {text,json,csv}, --output-type {text,json,csv}
                        output format default is "text".
  -t TIMEOUT, --timeout TIMEOUT
                        request timeout default is 360 sec.
  -l LIMIT, --limit LIMIT
                        limit results default is 10000.
  -nc, --no-color       show result without color.
  -lv, --list-view-type
                        list view type.
  -lm, --list-methods   list methods.
  --init INIT           set the api token.
  -v, --version         version.
```

Examples:
```
# Scan company by domain
chiasmodon_cli.py example.com --scan

# Search for target domain, you will see the result for only this "example.com" 
chiasmodon_cli.py example.com 
    
# Search in target and target subdomains
chiasmodon_cli.py example.com --method domain.all

# Search for target subdomains
chiasmodon_cli.py example.com --view-type subdomain
        
# Search for all creds in United States 
chiasmodon_cli.py US --method cred.country

# Search for related companies by domain
chiasmodon_cli.py example.com --view-type related

# search for target app id 
chiasmodon_cli.py com.discord --method app.id 
    
# search for target app domain 
chiasmodon_cli.py discord.com --method app.domain
    
# search for target app name 
chiasmodon_cli.py Discord --method app.name
    
# Search for ip asn
chiasmodon_cli.py AS123 --method ip.asn

# Search for cred username
chiasmodon_cli.py someone --method cred.username

# Search for cred password
chiasmodon_cli.py example@123 --method cred.password

# Search for url endpoint
chiasmodon_cli.py /wp-login.php --method url.path

# Search for ip
chiasmodon_cli.py 1.1.1.1 --method ip

# Search for cidr
chiasmodon_cli.py xx.xx.xx.0/24 --method ip

# Search for target creds by domain emsils
chiasmodon_cli.py example.com --method cred.email.domain

# Search for target email
chiasmodon_cli.py someone@example.com --method cred.email  

# search for multiple targets: 
chiasmodon_cli.py targets.txt --method domain  --output example-creds.txt 
```

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
- [🌐 Website](http://chiasmodon.online)
- [💬 Telegram](https://t.me/chiasmod0n)
- [🐦 X/Twitter](https://x.com/chiasmod0n)


## ⭐️Star History

<a href="https://star-history.com/#chiasmod0n/chiasmodon&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=chiasmod0n/chiasmodon&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=chiasmod0n/chiasmodon&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=chiasmod0n/chiasmodon&type=Date" />
 </picture>
</a>
