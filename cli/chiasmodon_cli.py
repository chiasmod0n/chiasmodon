#!/usr/bin/python3

import os
import sys
import json
import argparse
import tldextract
from yaspin import yaspin
from pathlib import Path 
from pychiasmodon import Chiasmodon,Result,VERSION,VIEW_TYPE_LIST,T

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class ULIT:
    @staticmethod
    def rFile(file:Path) -> str:
        if not file.is_file():
            print(f'{T.RED}Not found {file} file.{T.RESET}')
            return

        with open(file, 'r') as f:
            return f.read()    

    @staticmethod
    def wFile(file:Path, data:str) -> str:
        with open(file, 'w') as f:
            f.write(data)

    @staticmethod
    def rFileToJson(file:Path) -> dict:
        return json.loads(ULIT.rFile(file=file))

    @staticmethod
    def wJsonToFile(file:Path, data:dict) -> dict:
        ULIT.wFile(
            file=file,
            data=json.dumps(data)
        )

    @staticmethod
    def get_root_domain(d:str) -> str:
        domain = d.split()[0]
        x = tldextract.extract(domain)
        if not x.suffix:
            return None

        return '{}.{}'.format(x.domain, x.suffix)

class Scan(Chiasmodon):
    def __init__(self, options:argparse.Namespace) -> None:        
        self.options :argparse.Namespace=options
        self.result :list = []
        conf_file :Path = Path(ROOT_DIR, 'conf.json')
        token:str = '' 
        
        if not conf_file.is_file():ULIT.wJsonToFile(conf_file, {})

        if self.options.init:
            token = self.options.init
            ULIT.wJsonToFile(conf_file, {'token':self.options.init})

        elif not conf_file.is_file():
            ULIT.wJsonToFile(conf_file, {})
            token = ''

        else:
            token = ULIT.rFileToJson(conf_file).get('token') or ''

        super().__init__(
            token=token,
            color=True,
            #debug=self.options.debug, 
            debug=True, 
            check_token=self.options.init,
        )

        if self.options.init:
            sys.exit()
        
        self.scan_mode = True

    def scan_callback(self,beta,ys):
        self.print(beta.print(), ys)

    def proc(self):
        if not self.options.domain:
            self.print(f"{T.RED}You can't run scan without company domain\nPlease use (-d or --domain) to scan the domain{T.RESET}")
            sys.exit(0)
        
        domain = ULIT.get_root_domain(self.options.domain)
        if not domain:
            self.print(f"{T.RED}Wrong domain{T.RESET}",)
            sys.exit(0)

        self.output_folder = Path(domain)
        self.output_folder.mkdir(exist_ok=True, parents=True)

        self.__scan(
            domain=domain,
        )


    def __scan(self, domain):
        print_output = f'{T.MAGENTA}>{T.RESET}{T.YELLOW} Saved output{T.RESET}: \n'

        output = {
            'related':[],
            'client-creds':[],
            'client-usernames':[],
            'client-passwords':[],
            'client-emails':[],
            'employe-creds':[],
            'employe-usernames':[],
            'employe-passwords':[],
            'employe-emails':[],
            'subdomains':[],
            'urls':[],
            'endpoints':[],
            'ports':[],
            # 'company-apps':[], # "soon"
            # 'company-asns':[], # "soon"

        }
        
        self.print(f"\nFind related companies for {T.GREEN+domain+T.RESET}",ys=False)
        related = self.search(
            method='domain',
            query=domain,
            country=self.options.country,
            view_type='subdomain',
            sort=True ,
            timeout=self.options.timeout,
            only_domain_emails=False,
            all=False,
            limit=1000000,
            callback_view_result=self.scan_callback,
            yaspin=yaspin,
            related=True,
        )

        output['related'] = [i.save_format() for i in related]

        if related:
            ULIT.wFile((self.output_folder / 'related.txt'), '\n'.join(output['related'])) 
            print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'related.txt')}{T.RESET}\n"

        if self.options.scan_clients.lower() == 'yes':
            self.print(f"\nFind client creds in {T.GREEN+'*.'+domain+T.RESET}")
            client_creds:list[Result] = self.search(
                method='domain',
                query=domain,
                country=self.options.country,
                view_type='cred',
                sort=True ,
                timeout=self.options.timeout,
                only_domain_emails=False,
                all=True,
                limit=1000000,
                callback_view_result=self.scan_callback,
                yaspin=yaspin
            )
            output['client-creds'] =[i.save_format() for i in client_creds]
        
            if client_creds:
                ULIT.wFile((self.output_folder / 'client-creds.txt'), '\n'.join([':'.join(i) for i in output['client-creds']]))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'client-creds.txt')}{T.RESET}\n"
                
                for i in client_creds:
                    output['client-usernames'].append(i.username) if i.username and not i.email  and '/' not in i.username and  i.username not in output['client-usernames']  else None
                    output['client-passwords'].append(i.password) if i.password and i.password not in output['client-passwords'] else None
                    output['client-emails'].append(i.email) if i.email  and i.email not in output['client-emails'] else None
                    output['subdomains'].append(i.domain) if i.domain and i.domain not in output['subdomains'] and i.domain != domain else None
                    output['urls'].append(i.url) if i.url and i.url not in output['urls'] else None
                    output['endpoints'].append(i.urlEndpoint) if i.urlEndpoint and i.urlEndpoint not in output['endpoints'] else None
                    output['ports'].append(i.urlPort) if i.urlPort and i.urlPort not in output['ports'] else None
                    
                ULIT.wFile((self.output_folder / 'client-usernames.txt'), '\n'.join(output['client-usernames']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'client-usernames.txt')}{T.RESET}\n"
                ULIT.wFile((self.output_folder / 'client-emails.txt'), '\n'.join(output['client-emails']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'client-emails.txt')}{T.RESET}\n"
                ULIT.wFile((self.output_folder / 'client-passwords.txt'), '\n'.join(output['client-passwords']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'client-passwords.txt')}{T.RESET}\n"
                ULIT.wFile((self.output_folder / 'endpoints.txt'), '\n'.join(output['endpoints']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'endpoints.txt')}{T.RESET}\n"
                ULIT.wFile((self.output_folder / 'ports.txt'), '\n'.join([f"{i}" for i in output['ports']]))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'ports.txt')}{T.RESET}\n"
                ULIT.wFile((self.output_folder / 'subdomains.txt'), '\n'.join(output['subdomains']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'subdomains.txt')}{T.RESET}\n"
                ULIT.wFile((self.output_folder / 'urls.txt'), '\n'.join([f"{i}" for i in output['urls']]))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'urls.txt')}{T.RESET}\n"


        if self.options.scan_employees.lower() == 'yes':
            self.print(f"\nFind employees creds for {T.GREEN+domain+T.RESET}")
            employe_creds = self.search(
                method='domain',
                query=domain,
                country=self.options.country,
                view_type='cred',
                sort=True ,
                timeout=self.options.timeout,
                only_domain_emails=True,
                all=False,
                limit=1000000,
                callback_view_result=self.scan_callback,
                yaspin=yaspin
            )
            output['employe-creds'] =[i.save_format() for i in employe_creds]

            if employe_creds:
                ULIT.wFile((self.output_folder / 'employe-creds.txt'), '\n'.join([':'.join(i) for i in output['employe-creds']]))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'employe-creds.txt')}{T.RESET}\n"
                for i in employe_creds:
                    output['employe-usernames'].append(i.username) if i.username and not i.email and '/' not in i.username and i.username not in output['employe-usernames']  else None
                    output['employe-passwords'].append(i.password) if i.password and i.password not in output['employe-passwords'] else None
                    output['employe-emails'].append(i.email) if i.email  and i.email not in output['employe-emails'] else None
                    
                ULIT.wFile((self.output_folder / 'employe-usernames.txt'), '\n'.join(output['employe-usernames']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'employe-usernames.txt')}{T.RESET}\n"
                ULIT.wFile((self.output_folder / 'employe-emails.txt'), '\n'.join(output['employe-emails']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'employe-emails.txt')}{T.RESET}\n"
                ULIT.wFile((self.output_folder / 'employe-passwords.txt'), '\n'.join(output['employe-passwords']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'employe-passwords.txt')}{T.RESET}\n"
            
        ULIT.wJsonToFile((self.output_folder / 'scan.json'), output)
        print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'scan.json')}{T.RESET}"

        self.print(print_output)
        
class CLI(Chiasmodon):
    def __init__(self, options:argparse.Namespace) -> None:

        self.options :argparse.Namespace=options
        self.result :list = []

        conf_file :Path = Path(ROOT_DIR, 'conf.json')
        token:str = '' 
        
        if not conf_file.is_file():ULIT.wJsonToFile(conf_file, {})

        if self.options.init:
            token = self.options.init
            ULIT.wJsonToFile(conf_file, {'token':self.options.init})

        elif not conf_file.is_file():
            ULIT.wJsonToFile(conf_file, {})
            token = ''

        else:
            token = ULIT.rFileToJson(conf_file).get('token') or ''

        super().__init__(
            token=token,
            color=True,
            #debug=self.options.debug, 
            debug=True, 
            check_token=self.options.init,
        )

        if self.options.init:
            sys.exit()

    def review_results(self,
                       beta:Result, 
                       ys=True,
                    ) -> None:

        self.print(beta.print(), ys=ys)
        self.result.append(beta.save_format())
    
    def save_result(self, view_type) -> None:

        if self.options.output:

            if self.options.output_type == "text":
                if self.result and view_type != 'cred':
                    self.result = list(set(self.result))
                    self.result.remove(None) if None in self.result else None
                
                ULIT.wFile(
                    self.options.output,
                    '\n'.join([':'.join(i) if type(i) == list else i for i in self.result]) 
                )

            if self.options.output_type == "csv":
                if self.result and view_type != 'cred':
                    self.result = list(set(self.result))
                    self.result.remove(None) if None in self.result else None
                
                ULIT.wFile(
                    self.options.output,
                    '\n'.join([','.join(['url/app_id','user/email', 'password', 'country', 'date'])]+[','.join(i) if type(i) == list else i for i in self.result])  if view_type == 'cred' else  '\n'.join([view_type]+[','.join(i) if type(i) == list else i for i in self.result]) 
                )

            if self.options.output_type == "json":
                ULIT.wJsonToFile(
                    self.options.output,
                    self.result
                )



    def proc(self):

        if self.options.email:
            query = ULIT.rFile(f).splitlines() if (f:=Path(self.options.email)).is_file() else [self.options.email.strip().lower()]
            method = 'email'

        if self.options.domain:
            query = ULIT.rFile(f).splitlines() if (f:=Path(self.options.domain)).is_file() else [self.options.domain.strip().lower()]
            method = 'domain'

        if self.options.asn:
            query = ULIT.rFile(f).splitlines() if (f:=Path(self.options.asn)).is_file() else [self.options.asn.strip().lower()]
            method = 'asn'

        if self.options.cidr:
            query = ULIT.rFile(f).splitlines() if (f:=Path(self.options.cidr)).is_file() else [self.options.cidr.strip()]
            method = 'cidr'
      
        if self.options.app:
            query = ULIT.rFile(f).splitlines() if (f:=Path(self.options.app)).is_file() else [self.options.app.strip().lower()]
            method='app'

        if self.options.username:
            query = ULIT.rFile(f).splitlines() if (f:=Path(self.options.username)).is_file() else [self.options.username.strip()]
            method ='username'

        if self.options.password:
            query = ULIT.rFile(f).splitlines() if (f:=Path(self.options.password)).is_file() else [self.options.password.strip()]
            method = 'password'

        if self.options.endpoint:
            query = ULIT.rFile(f).splitlines() if (f:=Path(self.options.endpoint)).is_file() else [self.options.endpoint.strip()]
            method = 'endpoint'
        
        for i in query:
            self.search(
                query=i,
                method=method,
                country=self.options.country,
                view_type=self.options.view_type,
                limit=self.options.limit,
                all=self.options.all,
                only_domain_emails=self.options.domain_emails,
                timeout=self.options.timeout,
                sort=True,
                callback_view_result=self.review_results,
                related=self.options.related,
                yaspin=yaspin,
            )

        if self.options.output and self.result:
            self.save_result(self.options.view_type)
            self.print(f'{T.MAGENTA}>{T.RESET}{T.YELLOW} Saved output to {T.RESET}: {T.GREEN}{self.options.output}{T.RESET}')

      
if __name__ == "__main__":

    print(f"""
   🙂           🙂                 
  /|\\           /|\\               
  /\\            /\\                                                                                   
 \\___/        \\___/                 🔑
{T.BLUE}~^~^~^~^~^~^~^~^~^~^~^~^~{T.BLUE}~^~^~^~{T.GREEN}    {T.RESET}/|\\{T.GREEN}
|\\   {T.YELLOW}\\\\\\\\{T.GREEN}__     {T.MAGENTA}Chiasmodon{T.RESET} {T.RED}{VERSION}{T.GREEN}    {T.RESET}/\\{T.GREEN}
| \\_/    {T.RED}o{T.GREEN} \\    {T.CYAN}o{T.GREEN}                  {T.RESET}\\___/{T.GREEN}
> _   {T.YELLOW}(({T.GREEN} <_  {T.CYAN}oo{T.GREEN}        
| / \\__+___/        
|/     |/           

{T.MAGENTA}>{T.RESET} {T.YELLOW}Admin{T.RESET}: {T.GREEN}https://t.me/Chiasmod0n
{T.RESET}""")
    parser = argparse.ArgumentParser(description='Chiasmodon CLI',  formatter_class=argparse.RawTextHelpFormatter,)

    parser.add_argument('-d','--domain',        help='Search by domain.',type=str)
    parser.add_argument('-a','--app',           help='Search by google play applciton id.',type=str)
    parser.add_argument('-c','--cidr',          help='Search by CIDR.',type=str)
    parser.add_argument('-n','--asn',          help='Search by ASN.',type=str)
    parser.add_argument('-e','--email',         help='Search by email, only pro, only pro account.',type=str)
    parser.add_argument('-u','--username',      help='Search by username, only pro account.',type=str)
    parser.add_argument('-p','--password',      help='Search by password, only pro account.',type=str)
    parser.add_argument('-ep','--endpoint',     help='Search by url endpoint.',type=str)    
    parser.add_argument('-s','--scan',          help='scan the company domain (Related company, Clients, Employees, Company ASNs, Company Apps).',action='store_true', default=False)
    parser.add_argument('-sc','--scan-clients', help='Run clients scan, default is yes, Ex: -sc no',type=str, default='yes')
    parser.add_argument('-se','--scan-employees',help='Run employees scan, default is yes, Ex: -se no',type=str, default='yes')
    #parser.add_argument('-fs','--full-scan',    help='',action='store_true', default=False) # "soon" 
    parser.add_argument('-C','--country',       help='sort result by country code default is all', type=str, default='all')
    parser.add_argument('-A','--all',           help='view all result using "like",this option work only with (-d or --domain),default is False', action='store_true', default=False)
    parser.add_argument('-de','--domain-emails',help='only result for company "root" domain, this option work only with (-d or --domain), default is False',action='store_true', default=False)
    parser.add_argument('-r','--related',       help='Get related company domains,this option work only with (-d or --domain), default False',action='store_true', default=False)
    parser.add_argument('-o','--output',        help='filename to save the result', type=str,)
    parser.add_argument('-vt','--view-type',    help='type view the result default is "cred".', choices=VIEW_TYPE_LIST, type=str, default='cred')
    parser.add_argument('-ot','--output-type',  help='output format default is "text".', choices=['text', 'json', 'csv'], type=str, default='text')
    parser.add_argument('--init',               help='set the api token.',type=str)
    parser.add_argument('-T','--timeout',       help='request timeout default is 60.',type=int, default=60)
    parser.add_argument('-L','--limit',         help='limit results default is 10000.',type=int, default=10000)

    parser.add_argument('-v','--version',         help='version.',action='store_true')
    #parser.add_argument('-D','--debug',         help='debug mode default is false.',action='store_true', default=False)
    
    parser.epilog  = f'''
Examples:

    # Scan company by domain
    {Path(sys.argv[0]).name} --domain example.com --scan

    # Search for target domain, you will see the result for only this "example.com" 
    {Path(sys.argv[0]).name} --domain example.com 
    
    # Search for target subdomains
    {Path(sys.argv[0]).name} --domain example.com --all 
    
    # Search for target domain, you will see the result for only this "example.com" on United States 
    {Path(sys.argv[0]).name} --domain example.com --country US 

    # Search for related companies by domain
    {Path(sys.argv[0]).name} --domain example.com --related

    # search for target app id 
    {Path(sys.argv[0]).name} --app com.example 
    
    # Search for target asn
    {Path(sys.argv[0]).name} --asn AS123 --type-view cred

    # Search for target username
    {Path(sys.argv[0]).name} --username someone --country CA

    # Search for target password
    {Path(sys.argv[0]).name} --password example@123

    # Search for target endpoint
    {Path(sys.argv[0]).name} --endpoint /wp-login.php

    # Search for target cidr
    {Path(sys.argv[0]).name} --cidr x.x.x.x/24

    # Search for target creds by domain emsils
    {Path(sys.argv[0]).name} --domain example.com --domain-emails 
    {Path(sys.argv[0]).name} --domain example.com --domain-emails --output example-creds.json --output-type json
    {Path(sys.argv[0]).name} --domain example.com --domain-emails --view-type email --output example-emails.txt --output-type text
    
    # Search for target subdomain
    {Path(sys.argv[0]).name} --domain company.com --view-type subdomain
    
    # Search for target email
    {Path(sys.argv[0]).name} --email someone@example.com  
    {Path(sys.argv[0]).name} --email someone@example.com --view-type url 

    # search for multiple targets: 
    {Path(sys.argv[0]).name} --domain targets.txt --output example-creds.txt 
    {Path(sys.argv[0]).name} --domain targets.txt --view-type url --output example-urls.txt 
    '''
    args = parser.parse_args()
    if args.version:
        print(VERSION)
        sys.exit(0)

    if not args.scan and not args.domain and not args.email and not args.app  and not args.cidr and not args.asn and not args.init and not args.username and not args.password and not args.endpoint:
        parser.print_help()
        sys.exit(0)

    if args.scan:
        root=Scan(options=args)
        root.proc()

    else:
        root=CLI(options=args)
        root.proc()
