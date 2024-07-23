#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK

import os
import sys
import argcomplete
import json
import argparse
import tldextract
from yaspin import yaspin
from pathlib import Path 
from pychiasmodon import Chiasmodon,Result,VERSION,VIEW_TYPE_LIST,T,_METHODS

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
            conf_file=conf_file,
            color=True if not self.options.no_color else False,
            debug=True, 
            check_token=self.options.init,
        )

        if self.options.init:
            sys.exit()
        
        self.scan_mode = True

    def scan_callback(self,beta,ys):
        self.print(beta.print(), ys)

    def proc(self):
        if not self.options.query:
            self.print(f"{T.RED}You can't run scan without company domain\nPlease use (-d or --domain) to scan the domain{T.RESET}")
            sys.exit(0)
        
        domain = ULIT.get_root_domain(self.options.query)
        if not domain:
            self.print(f"{T.RED}Wrong domain{T.RESET}",)
            sys.exit(0)

        self.output_folder = Path(domain)
        self.output_folder.mkdir(exist_ok=True, parents=True)

        self.__scan(
            domain=domain,
        )


    def __scan(self, domain):
        status = False

        print_output = f'{T.MAGENTA}>{T.RESET}{T.YELLOW} Saved output{T.RESET}: \n'
        output = {
            'related':[],
            'apps':[], 
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

        }
        
        if self.options.scan_related.lower() == 'yes':
            related = self.search(
                method='domain',
                query=domain,
                view_type='related',
                sort=True ,
                timeout=self.options.timeout,
                limit=1000000,
                callback_view_result=self.scan_callback,
                yaspin=yaspin,
                search_text=f'Find {T.GREEN+domain+T.RESET} related companies...',
                err_text=f'Not found related !'
            )


            if related:
                status = True
                output['related'] = [i.save_format() for i in related]
                ULIT.wFile((self.output_folder / 'related.txt'), '\n'.join(output['related'])) 
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'related.txt')}{T.RESET}\n"
            else:
                self.print(f'{T.RED}💥  Not found related !{T.RESET}')
            self.print(f'{T.MAGENTA}{"-"*30}{T.RESET}')
        if self.options.scan_subdomains.lower() == 'yes':
            subdomains = self.search(
                method='domain',
                query=domain,
                view_type='subdomain',
                sort=True ,
                timeout=self.options.timeout,
                limit=1000000,
                callback_view_result=self.scan_callback,
                yaspin=yaspin,
                search_text=f'Find {T.GREEN+domain+T.RESET} subdomains...',
                err_text=f'Not found subdomains !'
            )


            if subdomains:
                status = True
                output['subdomains'] = [i.save_format() for i in subdomains]
                ULIT.wFile((self.output_folder / 'subdomains.txt'), '\n'.join(output['subdomains'])) 
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'subdomains.txt')}{T.RESET}\n"
            self.print(f'{T.MAGENTA}{"-"*30}{T.RESET}')
            
        if self.options.scan_apps.lower() == 'yes':
            apps = self.search(
                method='app.domain',
                query=domain,
                view_type='app',
                sort=True ,
                timeout=self.options.timeout,
                limit=1000000,
                callback_view_result=self.scan_callback,
                yaspin=yaspin,
                search_text=f'Find {T.GREEN+domain+T.RESET} Apps...',
                err_text=f'Not found apps !'
            )


            if apps:
                status = True
                output['apps'] = [i.save_format() for i in apps]
                ULIT.wFile((self.output_folder / 'apps.txt'), '\n'.join(output['apps'])) 
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'apps.txt')}{T.RESET}\n"
            self.print(f'{T.MAGENTA}{"-"*30}{T.RESET}')
        if self.options.scan_ips.lower() == 'yes':
            ips = self.search(
                method='domain.all',
                query=domain,
                view_type='ip',
                sort=True ,
                timeout=self.options.timeout,
                limit=1000000,
                callback_view_result=self.scan_callback,
                yaspin=yaspin,
                search_text=f'Find {T.GREEN+domain+T.RESET} IPs...',
                err_text=f'Not found ips !'
            )


            if ips:
                status = True
                output['ips'] = [i.save_format() for i in ips]
                ULIT.wFile((self.output_folder / 'ips.txt'), '\n'.join(output['ips'])) 
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'ips.txt')}{T.RESET}\n"
                
            self.print(f'{T.MAGENTA}{"-"*30}{T.RESET}')
        if self.options.scan_clients.lower() == 'yes':
            client_creds:list[Result] = self.search(
                query=domain,
                method='domain.all',
                view_type='full',
                sort=True ,
                timeout=self.options.timeout,
                limit=1000000,
                callback_view_result=self.scan_callback,
                yaspin=yaspin,
                search_text=f'Find {T.GREEN+domain+T.RESET} client creds...',
                err_text=f'Not found clients !'
                
            )
        
            if client_creds:
                status = True
                output['client-creds'] =[i.save_format() for i in client_creds]
                ULIT.wFile((self.output_folder / 'client-creds.txt'), '\n'.join([':'.join(i) for i in output['client-creds']]))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'client-creds.txt')}{T.RESET}\n"
                
                for i in client_creds:
                    output['client-usernames'].append(i.credUsername) if i.credUsername and not i.credEmail  and '/' not in i.credUsername and  i.credUsername not in output['client-usernames']  else None
                    output['client-passwords'].append(i.credPassword) if i.credPassword and i.credPassword not in output['client-passwords'] else None
                    output['client-emails'].append(i.credEmail) if i.credEmail  and i.credEmail not in output['client-emails'] else None
                    output['subdomains'].append(i.domain) if i.domain and i.domain not in output['subdomains'] and i.domain != domain else None
                    output['urls'].append(i.url) if i.url and i.url not in output['urls'] else None
                    output['endpoints'].append(i.urlPath) if i.urlPath and i.urlPath not in output['endpoints'] else None
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


            self.print(f'{T.MAGENTA}{"-"*30}{T.RESET}')
        if self.options.scan_employees.lower() == 'yes':
            employe_creds = self.search(
                query=domain,
                method='cred.email.domain',
                view_type='full',
                sort=True,
                timeout=self.options.timeout,
                callback_view_result=self.scan_callback,
                limit=1000000,
                yaspin=yaspin,
                search_text=f'Find {T.GREEN+domain+T.RESET} employees creds...',
                err_text=f'Not found Employees!'
            )

            if employe_creds:
                status = True
                output['employe-creds'] =[i.save_format() for i in employe_creds]
                ULIT.wFile((self.output_folder / 'employe-creds.txt'), '\n'.join([':'.join(i) for i in output['employe-creds']]))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'employe-creds.txt')}{T.RESET}\n"
                for i in employe_creds:
                    output['employe-usernames'].append(i.credUsername) if i.credUsername and not i.credEmail and '/' not in i.credUsername and i.credUsername not in output['employe-usernames']  else None
                    output['employe-passwords'].append(i.credPassword) if i.credPassword and i.credPassword not in output['employe-passwords'] else None
                    output['employe-emails'].append(i.credEmail) if i.credEmail  and i.credEmail not in output['employe-emails'] else None
                    
                ULIT.wFile((self.output_folder / 'employe-usernames.txt'), '\n'.join(output['employe-usernames']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'employe-usernames.txt')}{T.RESET}\n"
                ULIT.wFile((self.output_folder / 'employe-emails.txt'), '\n'.join(output['employe-emails']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'employe-emails.txt')}{T.RESET}\n"
                ULIT.wFile((self.output_folder / 'employe-passwords.txt'), '\n'.join(output['employe-passwords']))
                print_output += f"\t{T.MAGENTA}-{T.RESET} {T.BLUE}{(self.output_folder / 'employe-passwords.txt')}{T.RESET}\n"
        

        if status:
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
            conf_file=conf_file,
            color=True if not self.options.no_color else False,
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

        if beta.save_format() not in self.result:
            self.print(beta.print(), ys=ys)
            self.result.append(beta.save_format())
        
    def save_result(self, view_type) -> None:

        if self.options.output:

            if self.options.output_type == "text":
                if self.result and view_type != 'cred':
                    self.result.remove(None) if None in self.result else None
                
                ULIT.wFile(
                    self.options.output,
                    '\n'.join([':'.join(i) if type(i) == list else i for i in self.result]) 
                )

            if self.options.output_type == "csv":
                if self.result and view_type != 'cred':
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

        query = ULIT.rFile(f).splitlines() if (f:=Path(self.options.query)).is_file() else [self.options.query.strip()] 


        for i in query:
            self.search(
                query=i,
                method=self.options.method,
                view_type=self.options.view_type,
                limit=self.options.limit,
                timeout=self.options.timeout,
                sort=True,
                yaspin=yaspin,
                callback_view_result=self.review_results,
            )

        if self.options.output and self.result:
            self.save_result(self.options.view_type)
            self.print(f'{T.MAGENTA}>{T.RESET}{T.YELLOW} Saved output to {T.RESET}: {T.GREEN}{self.options.output}{T.RESET}')

      
if __name__ == "__main__":

    if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
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

    if '-lm' not in sys.argv and '--list-methods' not in sys.argv and '-lv' not in sys.argv and '--list-view-type' not in sys.argv and '-v' not in sys.argv and '--version' not in sys.argv and '--init' not in sys.argv:
        parser.add_argument('query', type=str,      help='query argument')

    parser.add_argument('-m','--method',        help='method to search by it,default is "domain".', choices=_METHODS, type=str, default='domain')
    parser.add_argument('-vt','--view-type',    help='type view the result default is "full".', choices=VIEW_TYPE_LIST, type=str, default='full')
    parser.add_argument('-s','--scan',          help='scan the company domain (Related company, Clients, Employees, Company ASNs, Company Apps).',action='store_true')
    parser.add_argument('-sr','--scan-related', help='Run related scan, default is yes, Ex: -sr no',type=str, default='yes')
    parser.add_argument('-ss','--scan-subdomains', help='Run subdomains scan, default is yes, Ex: -ss no',type=str, default='yes')
    parser.add_argument('-sa','--scan-apps',    help='Run App scan, default is yes, Ex: -sa no',type=str, default='yes')
    parser.add_argument('-si','--scan-ips',     help='Run IPs scan, default is yes, Ex: -si no',type=str, default='yes')
    parser.add_argument('-sc','--scan-clients', help='Run clients scan, default is yes, Ex: -sc no',type=str, default='yes')
    parser.add_argument('-se','--scan-employees',help='Run employees scan, default is yes, Ex: -se no',type=str, default='yes')
    parser.add_argument('-o','--output',        help='filename to save the result', type=str,)
    parser.add_argument('-ot','--output-type',  help='output format default is "text".', choices=['text', 'json', 'csv'], type=str, default='text')
    parser.add_argument('-t','--timeout',       help='request timeout default is 360 sec.',type=int, default=360)
    parser.add_argument('-l','--limit',         help='limit results default is 10000.',type=int, default=10000)
    parser.add_argument('-nc','--no-color',     help='show result without color.',action='store_true')
    parser.add_argument('-lv','--list-view-type',help='list view type.',action='store_true')
    parser.add_argument('-lm','--list-methods',   help='list methods.',  action='store_true')
    parser.add_argument('--init',               help='set the api token.',type=str)

    parser.add_argument('-v','--version',         help='version.',action='store_true') 

    parser.epilog  = f'''
Examples:

    # Scan company by domain
    {Path(sys.argv[0]).name} example.com --scan

    # Search for target domain, you will see the result for only this "example.com" 
    {Path(sys.argv[0]).name} example.com 
    
    # Search in target and target subdomains
    {Path(sys.argv[0]).name} example.com --method domain.all

    # Search for target subdomains
    {Path(sys.argv[0]).name} example.com --view-type subdomain
        
    # Search for all creds in United States 
    {Path(sys.argv[0]).name} US --method cred.country

    # Search for related companies by domain
    {Path(sys.argv[0]).name} example.com --view-type related

    # search for target app id 
    {Path(sys.argv[0]).name} com.discord --method app.id 
    
    # search for target app domain 
    {Path(sys.argv[0]).name} discord.com --method app.domain
    
    # search for target app name 
    {Path(sys.argv[0]).name} Discord --method app.name
    
    # Search for ip asn
    {Path(sys.argv[0]).name} AS123 --method ip.asn

    # Search for cred username
    {Path(sys.argv[0]).name} someone --method cred.username

    # Search for cred password
    {Path(sys.argv[0]).name} example@123 --method cred.password

    # Search for url endpoint
    {Path(sys.argv[0]).name} /wp-login.php --method url.path

    # Search for ip
    {Path(sys.argv[0]).name} 1.1.1.1 --method ip

    # Search for cidr
    {Path(sys.argv[0]).name} xx.xx.xx.0/24 --method ip

    # Search for target creds by domain emsils
    {Path(sys.argv[0]).name} example.com --method cred.email.domain

    # Search for target email
    {Path(sys.argv[0]).name} someone@example.com --method cred.email  

    # search for multiple targets: 
    {Path(sys.argv[0]).name} targets.txt --method domain  --output example-creds.txt 
    '''

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.list_view_type:
        for i in VIEW_TYPE_LIST:
            print(i)
        sys.exit(0)

    if args.list_methods:
        for i in _METHODS:
            print(i)
        sys.exit(0)

    if args.version:
        print(VERSION)
        sys.exit(0)

    if args.scan:
        root=Scan(options=args)
        root.proc()

    else:
        root=CLI(options=args)
        root.proc()
