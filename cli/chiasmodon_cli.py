#!/usr/bin/python3

import os
import sys
import json
import argparse
from yaspin import yaspin
from pathlib import Path 
from pychiasmodon import Chiasmodon,Result,VERSION

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class ULIT:
    @staticmethod
    def rFile(file:Path) -> str:
        if not file.is_file():
            print(f'{Chiasmodon.T.RED}Not found {file} file.{Chiasmodon.T.RESET}')
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

class ChiasmodonCLI(Chiasmodon):
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
                       view_type:str,
                       ys:yaspin,
                    ) -> None:

        if view_type == list(self.VIEW_TYPE.keys())[0x0]:
            if ':http' in (beta.url or  ''):return 

            c = ''
            if beta.app_id:
                c+=f"{self.T.MAGENTA}> {self.T.YELLOW}App ID{self.T.RESET}: {self.T.CYAN}{beta.app_id}{self.T.RESET}\n"
                if beta.app_name:
                    c+=f"{self.T.MAGENTA}> {self.T.YELLOW}App name{self.T.RESET}: {self.T.CYAN}{beta.app_name}{self.T.RESET}\n"
            else:
                c+=f"{self.T.MAGENTA}> {self.T.YELLOW}URL{self.T.RESET}: {self.T.CYAN}{beta.url}{self.T.RESET}\n"
            
            c+=f"{self.T.MAGENTA}> {self.T.YELLOW}Username{self.T.RESET}: {self.T.GREEN}{beta.username}{self.T.RESET}\n" if beta.username else f"{self.T.MAGENTA}> {self.T.YELLOW}Email{self.T.RESET}: {self.T.GREEN}{beta.email}{self.T.RESET}\n"
            c+=f"{self.T.MAGENTA}> {self.T.YELLOW}Password{self.T.RESET}: {self.T.GREEN}{beta.password}{self.T.RESET}\n"
            c+=f"{self.T.MAGENTA}> {self.T.YELLOW}Country{self.T.RESET}: {self.T.RED if beta.country == 'Unknown' else self.T.CYAN}{beta.country}{self.T.RESET}\n"
            c+=f"{self.T.MAGENTA}> {self.T.YELLOW}Date{self.T.RESET}: {self.T.BLUE}{beta.date}{self.T.RESET}"
            self.print(c, ys)

            self.result.append(beta.save_format())

            self.print(f"{self.T.MAGENTA}+"*30 + self.T.RESET, ys)

        
        elif view_type in list(self.VIEW_TYPE.keys())[0x1:]:
            if ':http' in  (beta.url or '') :return
            
            if view_type in ['email','username', 'password']:
                self.print(f"{self.T.MAGENTA}> " +self.T.GREEN+beta+self.T.RESET, ys)
            if view_type in ['app', 'url']:
                self.print(f"{self.T.MAGENTA}> " +self.T.CYAN+beta+self.T.RESET, ys)
            if view_type in ['subdomain']:
                self.print(f"{self.T.MAGENTA}> " +self.T.BLUE+beta+self.T.RESET, ys)

            self.result.append(beta.save_format())
    
    def save_result(self) -> None:

        if self.options.output:
            if self.options.output_type == "text":
                ULIT.wFile(
                    self.options.output,
                    '\n'.join([':'.join(i) if type(i) == list else i for i in self.result]) 
                )
            
            if self.options.output_type == "csv":
                ULIT.wFile(
                    self.options.output,
                    '\n'.join([','.join(i) if type(i) == list else i for i in self.result]) 
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
                yaspin=yaspin,
            )
        
        if self.options.output and self.result:
            self.save_result()
            self.print(f'{self.T.MAGENTA}>{self.T.RESET}{self.T.YELLOW} Saved output to {self.T.RESET}: {self.T.GREEN}{self.options.output}{self.T.RESET}')

      
if __name__ == "__main__":

    print(f"""
   🙂           🙂                 
  /|\\           /|\\               
  /\\            /\\                                                                                   
 \\___/        \\___/                 🔑
{Chiasmodon.T.BLUE}~^~^~^~^~^~^~^~^~^~^~^~^~{Chiasmodon.T.BLUE}~^~^~^~{Chiasmodon.T.GREEN}    {Chiasmodon.T.RESET}/|\\{Chiasmodon.T.GREEN}
|\\   {Chiasmodon.T.YELLOW}\\\\\\\\{Chiasmodon.T.GREEN}__     {Chiasmodon.T.MAGENTA}Chiasmodon{Chiasmodon.T.RESET} {Chiasmodon.T.RED}{VERSION}{Chiasmodon.T.GREEN}    {Chiasmodon.T.RESET}/\\{Chiasmodon.T.GREEN}
| \\_/    {Chiasmodon.T.RED}o{Chiasmodon.T.GREEN} \\    {Chiasmodon.T.CYAN}o{Chiasmodon.T.GREEN}                  {Chiasmodon.T.RESET}\\___/{Chiasmodon.T.GREEN}
> _   {Chiasmodon.T.YELLOW}(({Chiasmodon.T.GREEN} <_  {Chiasmodon.T.CYAN}oo{Chiasmodon.T.GREEN}        
| / \\__+___/        
|/     |/           

{Chiasmodon.T.MAGENTA}>{Chiasmodon.T.RESET} {Chiasmodon.T.YELLOW}Admin{Chiasmodon.T.RESET}: {Chiasmodon.T.GREEN}https://t.me/Chiasmod0n
{Chiasmodon.T.RESET}""")
    parser = argparse.ArgumentParser(description='Chiasmodon CLI',  formatter_class=argparse.RawTextHelpFormatter,)

    parser.add_argument('-d','--domain',        help='Search by domain.',type=str)
    parser.add_argument('-a','--app',           help='Search by google play applciton id.',type=str)
    parser.add_argument('-c','--cidr',          help='Search by CIDR.',type=str)
    parser.add_argument('-s','--asn',           help='Search by ASN.',type=str)
    parser.add_argument('-e','--email',         help='Search by email, only pro, only pro account.',type=str)
    parser.add_argument('-u','--username',      help='Search by username, only pro account.',type=str)
    parser.add_argument('-p','--password',      help='Search by password, only pro account.',type=str)

    parser.add_argument('-C','--country',       help='sort result by country code default is all', type=str, default='all')
    parser.add_argument('-vt','--view-type',    help='type view the result default is "cred".', choices=Chiasmodon.VIEW_TYPE, type=str, default='cred')
    parser.add_argument('-o','--output',        help='filename to save the result', type=str,)

    parser.add_argument('-ot','--output-type',  help='output format default is "text".', choices=['text', 'json', 'csv'], type=str, default='text')
    parser.add_argument('--init',               help='set the api token.',type=str)

    parser.add_argument('-A','--all',           help='view all result using "like",this option work only with (-d or --domain , -a or --app),default is False', action='store_true', default=False)
    parser.add_argument('-de','--domain-emails',help='only result for company domain, this option work only with -d or --domain, default is False',action='store_true', default=False)

    parser.add_argument('-T','--timeout',       help='request timeout default is 60.',type=int, default=60)
    parser.add_argument('-L','--limit',         help='limit results default is 10000.',type=int, default=100)

    parser.add_argument('-v','--version',         help='version.',action='store_true')
    #parser.add_argument('-D','--debug',         help='debug mode default is false.',action='store_true', default=False)
    
    parser.epilog  = f'''
Examples:

    # Search for target domain, you will see the result for only this "example.com" 
    {Path(sys.argv[0]).name} --domain example.com 
    
    # Search for target subdomains
    {Path(sys.argv[0]).name} --domain example.com --all 
    
    # Search for target domain, you will see the result for only this "example.com" on United States 
    {Path(sys.argv[0]).name} --domain example.com --country US 
    
    # search for target app id 
    {Path(sys.argv[0]).name} --app com.example 
    
    # Search for target asn
    {Path(sys.argv[0]).name} --asn AS123 --type-view cred

    # Search for target username
    {Path(sys.argv[0]).name} --username someone --country CA

    # Search for target password
    {Path(sys.argv[0]).name} --password example@123

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

    if not args.domain and not args.email and not args.app  and not args.cidr and not args.asn and not args.init and not args.username and not args.password:
        parser.print_help()
        sys.exit(0)
    
    root=ChiasmodonCLI(options=args)
    root.proc()