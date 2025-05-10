import re
import os 
import sys
import time
import requests
from yaspin import Spinner 

VERSION = "3.0.2"
_API_URL = 'http://chiasmodon.online/v2/api/beta'
_API_HEADERS = {'user-agent':'cli/python'}
_VIEW_TYPE = {
    'full':[
        'cred.username',
        'cred.phone',
        'cred.password',
        'cred.email',
        'cred.email.domain',
        'cred.country',
        'domain',
        'domain.all',
        
        'ip',
        'ip.asn',
        'ip.isp',
        'ip.org',
        'ip.port',
        'ip.country',
        'app.id',
        'app.name',
        'app.domain',
        'url.path',
        'url.port',
    ],
    'cred':[
        'cred.phone',
        'cred.username',
        'cred.password',
        'cred.email',
        'cred.email.domain',
        'cred.country',
        'domain',
        'domain.all',
        
        'ip',
        'ip.asn',
        'ip.isp',
        'ip.org',
        'ip.port',
        'ip.country',
        'app.id',
        'app.name',
        'app.domain',
        'url.path',
        'url.port',
    ],
    'url':[
        'cred.username',
        'cred.password',
        'cred.phone',
        'cred.email',
        'cred.email.domain',
        'cred.country',
        'domain',
        'domain.all',
        'ip',
        'ip.asn',
        'ip.isp',
        'ip.org',
        'ip.port',
        'ip.country',
        'url.path',
        'url.port',
    ],
    'email':[
        'cred.username',
        'cred.phone',
        'cred.password',
        'cred.country',
        'cred.email.domain',
        'domain',
        'domain.all',
        'ip',
        'ip.asn',
        'ip.isp',
        'ip.org',
        'ip.port',
        'ip.country',
        'app.id',
        'app.name',
        'app.domain',
        'url.path',
        'url.port',
    ],
    'phone':[
        'cred.username',
        'cred.email',
        'cred.email.domain',
        'domain',
        'domain.all',
        'ip',
        'ip.asn',
        'ip.isp',
        'ip.org',
        'ip.port',
        'ip.country',
        'app.id',
        'app.name',
        'app.domain',
        'url.path',
        'url.port',
        'cred.country',
    ],    
    'password':[
        'cred.username',
        'cred.phone',

        'cred.email',
        'cred.email.domain',
        'domain',
        'domain.all',
        'ip',
        'ip.asn',
        'ip.isp',
        'ip.org',
        'ip.port',
        'ip.country',
        'app.id',
        'app.name',
        'app.domain',
        'url.path',
        'url.port',
        'cred.country',
    ],
    'username': [
        'cred.phone',
        'cred.password',
        'domain',
        'domain.all',
        'ip',
        'ip.asn',
        'ip.isp',
        'ip.org',
        'ip.port',
        'ip.country',
        'app.id',
        'app.name',
        'app.domain',
        'url.path',
        'url.port',
        'cred.country',
    ],
    'app':[
        'cred.phone',
        'cred.username',
        'cred.password',
        'cred.email',
        'cred.email.domain',
        'cred.country', 
        'app.domain'
    ],
    'domain':[
        'cred.username',
        'cred.phone',
        'cred.password',
        'cred.email',
        'cred.email.domain',
        'cred.country',
        'domain',
        'domain.all',
        
        'ip',
        'ip.asn',
        'ip.isp',
        'ip.org',
        'ip.port',
        'ip.country',
        'app.id',
        'app.name',
        'app.domain',
        'url.path',
        'url.port',
    ],
    'ip':[
        'cred.username',
        'cred.phone',
        'cred.password',
        'cred.email',
        'cred.email.domain',
        'domain',
        'domain.all',
        'ip.asn',
        'ip.isp',
        'ip.org',
        'ip.port',
        'ip.country',
        'app.id',
        'app.name',
        'app.domain',
        'url.path',
        'url.port',
        'cred.country',
    ],
    'related':[
        'domain',
    ],
    'subdomain':[
        'domain'
    ]
}

_METHODS = [
    # cred
    'cred.username',         # Query like -> somone
    'cred.password',         # Query like -> lol@123
    'cred.email',            # Query like -> somone@example.com
    'cred.phone',            # Query line -> xxxxxxxx # without : + or - or  space or ) or (
    'cred.email.domain',     # Query like -> example.com
    'cred.country',          # Query like -> US 

    # domain
    'domain',           # Query like -> example.com
    'domain.all',       # Query like -> example.com

    # ip
    'ip',               # Query like -> 1.1.1.1
    'ip.asn',           # Query like -> as123
    'ip.isp',           # Query like -> "isp company"
    'ip.org',           # Query like -> "org name"
    'ip.port',          # Query like -> 22
    'ip.country',       # Query like -> US
    
    # app
    'app.id',           # Query like -> com.example
    'app.name',         # Query like -> Example
    'app.domain',       # Query like -> example.com
    
    # url
    'url.path',         # Query like -> "isp company"
    'url.port',         # Query like -> 8080
]

VIEW_TYPE_LIST = list(_VIEW_TYPE.keys())

class T:
    RED      = '\033[91m'
    GREEN    = '\033[92m'
    YELLOW   = '\033[93m'
    BLUE     = '\033[94m'
    MAGENTA  = '\033[95m'
    CYAN     = '\033[96m'
    RESET    = '\033[0m'


class Chiasmodon:
    def __init__(self, token=None, color=True, debug=True,conf_file=None,check_token=True) -> None:
        self.token                 = token
        self.conf_file             = conf_file
        self.debug                 = debug
        self.err :bool             = False 
        self.msg :str              = '' 
        self.__result:list[Result] = []
        self.scan_mode             = False

        if not color:
            T.RED      = ''
            T.GREEN    = ''
            T.YELLOW   = ''
            T.BLUE     = ''
            T.MAGENTA  = ''
            T.CYAN     = ''
            T.RESET    = ''
        
        if self.token and check_token:
            if self.__check_token():
                self.print(f'{T.GREEN}Set token successfully{T.RESET}')

            else:
                try:os.remove(conf_file)
                except:pass

                self.print(f'{T.RED}{self.msg}{T.RESET}')
                return

    def proc_all_domains(self,
                query,
                view_type,
                sort,
                timeout,
                limit,
                callback_view_result,
                yaspin,
                search_text,
                err_text) -> list:
        

        domains :list = self.__proc_query(
                query=query,
                method='domain',
                view_type='subdomain',
                sort=sort,
                timeout=timeout,
                limit=limit,
                callback_view_result=None,
                yaspin=None,
                search_text=search_text,
                err_text=err_text,
        )
        self.__result :list = []
        result :list = []
        
        domains = [i.domain for i in domains]
        if query not in domains:domains.append(query)

        for domain in domains:
            result.extend(self.__proc_query(
                query=domain,
                method='domain',
                view_type=view_type,
                sort=sort,
                timeout=timeout,
                limit=limit,
                callback_view_result=callback_view_result,
                yaspin=yaspin,
                search_text=search_text.replace(query, domain),
                err_text=err_text,
            ))
            self.__result :list = []
        
        return result

    
    def filter(self,query:str,method:str):

        if 'domain' in method:
            if not re.match(r"^(?!.*\d+\.\d+\.\d+\.\d+$)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", query):
                self.print(f'{T.RED}Your format query is wrong!\nThis is not domain.{T.RESET}')
                return False

        elif method == 'ip':
            if not re.match(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", query):
                self.print(f'{T.RED}Your format query is wrong!\nAccept only ipv4.{T.RESET}')
                return False
        
        elif method == 'ip.asn':
            if not query.lower().startswith('as'):
                self.print(f'{T.RED}Your format query is wrong!\nThe ASN starts with AS\nLike this: AS1234.{T.RESET}')
                return False
        
        elif method in ['ip.port', 'url.port']:
            if not re.match(r":(\d+)", query):
                self.print(f'{T.RED}Your format query is wrong!\nThis is not port.{T.RESET}')
                return False
        
        elif method == 'cred.email':
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', query):
                self.print(f'{T.RED}Your format query is wrong!\nThis is not email.{T.RESET}')
                return False
        
        elif method == 'cred.country' or method == 'ip.country':
            if not len(query) == 2:
                self.print(f'{T.RED}Your format query is wrong!\nAccept only country code.{T.RESET}')
                return False
        
        elif method == 'url.path':
            if not query[0] == '/':
                self.print(f'{T.RED}Your format query is wrong!\nThe url path moset be like: /somthing{T.RESET}')
                return False
        
        return query

    def print(self,text, ys=None, ys_err=False) -> None:
        if text == None:return 
        if self.debug:
            if ys:
                if not ys_err:
                    ys.write(text)
                else:
                    ys.text = text
            else:
                print(text)

    def __check_token(self):
        if self.__request({
            'token'     : self.token,
            'version'   : VERSION,
            'method'    : 'token'
        }).get('is_active'):
            return True 

        return False 

    def __request(self, data:dict,timeout=60):

        try:
            resp = requests.post(_API_URL, data=data, headers=_API_HEADERS, timeout=timeout)
            resp.close()
            resp = resp.json()

            try:
                if resp.get('err'):
                    self.err = True 
                    self.msg = resp['msg']
            except:pass

            return resp

        except requests.exceptions.ReadTimeout:
            self.print(f"{T.RED}\nError: timeout !\nPlease try agine later.{T.RESET}")
            sys.exit()

        except requests.exceptions.InvalidJSONError:
            self.print(f"{T.RED}\nError: Server send wrong data.\nPlease try agine later.{T.RESET}")
            sys.exit()

        except Exception as e:
            self.print(f"{T.RED}\nRequest error: {e}\nPlease try agine later.{T.RESET}")
            sys.exit()


    def __proc_query(self, 
                    method:str, 
                    query:str, 
                    view_type:str, 
                    timeout:int,
                    sort:bool, 
                    limit:int,
                    yaspin:bool,
                    callback_view_result,
                    search_text='',
                    err_text=''
                    ) -> dict:
        Result.VIEW_TYPE = view_type

        result : list[Result] = []

        data = {

            'token'         :       self.token,
            'type-view'     :       view_type,
            'method'        :       method,
            'version'       :       VERSION,
            'query'         :       query,
            'get-info'      :       'yes'
        }

        if yaspin:
            with yaspin(Spinner(["🐟","🐠","🐡","🐬","🐋","🐳","🦈","🐙","🐚","🪼","🪸"], 200),text=f"Processing {query} ..." if not search_text else search_text) as sp:
                process_info = self.__request(
                    data=data,
                    timeout=timeout,
                )

            if process_info and process_info.get('count') == 0:
                if not err_text:
                    self.print(f"{T.RED}Not found result{T.RESET}", sp,ys_err=True)
                else:
                    self.print(f"{T.RED}{err_text}{T.RESET}", sp,ys_err=True)
                        

                sp.fail("💥 ")
                sp.stop()
                return result 

            else:
                sp.ok("⚓ ")

        else:
            process_info = self.__request(
                data=data,
                timeout=timeout,
            )
            if process_info and process_info.get('count') == 0:
                self.print(f"{T.RED}Not found result{T.RESET}")
                return result
            
        
        del data['get-info'] 

        if self.err:
            self.err= False
            self.print(f'{T.RED}Error: {self.msg}{T.RESET}',ys_err=True) 
            return
            
        if yaspin: 
            self.print(f"{T.YELLOW}Pages count{T.YELLOW}: {T.GREEN}{process_info['pages'] if process_info['count'] != -1 else 'unknown'}{T.RESET}")

        data['sid'] = process_info['sid']

        if yaspin:
            YS = yaspin(f'Get pages 0/{process_info["pages"]}').green.bold.shark #.on_black
            YS.start()

        else:
            YS = None
        
        for p in range(1, process_info['pages']+0x1):
            if yaspin:YS.text = f'Get pages {p}/{process_info["pages"]}'
            
            data['page'] = p

            beta_result = self.__request(
                data=data,
                timeout=timeout,
            )

            if self.err:
                self.err=False
                if yaspin:self.print(f"{T.RED}{self.msg}{T.RESET}", YS, ys_err=True);YS.fail("💥 ");YS.stop()
                return result

            for r in beta_result['data']:
                
                column :Result = Result(**r)

                if sort and column in self.__result:
                    continue
                
                if callback_view_result != None:
                    callback_view_result(beta=column, ys=YS)

                result.append(column)
                self.__result.append(column)

                if len(result) == limit:
                    if yaspin:YS.text='';YS.stop()
                    return result
                
            if beta_result['done']:
                if yaspin:YS.text='';YS.stop()
                return result

            time.sleep(0x1)

        if not result:
            if yaspin:self.print(f"{T.RED}Not found result{T.RESET}", YS,ys_err=True);YS.fail("💥 ");YS.stop()
            else:self.print(f"{T.RED}Not found result{T.RESET}")
        else:
            if yaspin:YS.text='';YS.stop()
        return result
    
    def search(self,
               query,
               method='domain',
               view_type='full',
               limit=10000,
               timeout=60,
               sort=True,
               yaspin=False,
               search_text='',
               err_text='',
               callback_view_result=None) -> dict:
        
        
        if method not in _METHODS:
            raise Exception(f"{T.RED}not found this method: {method}.{T.RESET}")
        
        if method not in _VIEW_TYPE[view_type]:
            raise Exception(f"{T.RED}{view_type} doesn't support ({method}).{T.RESET}")
        
        
        self.err = False
        self.msg = ''
        result = None

        query = self.filter(query, method)
        if query == False:
            return

        if method == "domain.all":
            result = self.proc_all_domains(
                query=query,
                view_type=view_type,
                sort=sort,
                timeout=timeout,
                limit=limit,
                callback_view_result=callback_view_result,
                yaspin=yaspin,
                search_text=search_text,
                err_text=err_text,
            )

        else:

            result = self.__proc_query(
                query=query,
                method=method,
                view_type=view_type,
                sort=sort,
                timeout=timeout,
                limit=limit,
                callback_view_result=callback_view_result,
                yaspin=yaspin,
                search_text=search_text,
                err_text=err_text,
            )

        self.__result:list = []

        return result

class Result(dict):
    VIEW_TYPE = None
    HID_PASS  = True if os.environ.get('HID_PASS') else False 
    def __init__(self,type,**kwargs) -> None:
        
        self.kwargs         = kwargs
        Type           = type 

        self.url            = None
        self.urlPort        = None
        self.urlPath        = None
        self.credEmail      = None
        self.credUsername   = None
        self.credPassword   = None
        self.credCountry    = None
        self.credDate       = None 
        self.credPhone      = None 
        self.domain         = None 
        self.ip             = None 
        self.ipAsn          = None
        self.ipIsp          = None
        self.ipOrg          = None
        self.ipPorts        = None
        self.ipCountry      = None
        self.appID          = None
        self.appName        = None 
        self.appIcon        = None 
        self.appDomain      = None 

        if Type == "login":
            if kwargs.get('url'):
                self.urlPath = kwargs['url']['path']
                self.urlPort = kwargs['url']['port']
                self.url    = self.__convert_url(kwargs['url'])
                
                if kwargs['url']['ip']:
                    self.__convert_and_set_ip(kwargs['url']['ip'])

                elif kwargs['url']['domain']:
                    self.domain = self.__convert_domain(kwargs['url']['domain'])    
                

            if kwargs.get('app'):
                self.appID   = kwargs['app']['id']
                self.appName = kwargs['app']['name']
                self.appIcon = kwargs['app']['icon']
                if kwargs['app']['domain']:
                    self.appDomain = self.__convert_domain(kwargs['app']['domain'])

            if kwargs.get('cred'):
                if kwargs['cred']['email']:
                    self.credEmail = self.__convert_email(kwargs['cred']['email'])

                self.credUsername = kwargs['cred']['username']
                self.credPassword = kwargs['cred']['password'] if not self.HID_PASS else '*'*len(kwargs['cred']['password']) 
                if kwargs['cred']['phone']:
                    self.credPhone = self.__convert_phone(kwargs['cred']['phone'])


            if kwargs.get('country'):
                self.credCountry = kwargs['country']['f']
            
            self.credDate = kwargs['date']

        elif Type == 'url':
            self.urlPath = kwargs['path']
            self.urlPort = kwargs['port']
            self.url = self.__convert_url(kwargs)

            if kwargs['ip']:
                self.url    = self.__convert_url(kwargs)
                self.__convert_and_set_ip(kwargs['ip'])

            elif kwargs['domain']:
                self.domain = self.__convert_domain(kwargs['domain'])    

        elif Type == "email":
            self.credEmail = self.__convert_email(kwargs)
        
        elif Type == "domain":
            self.domain = self.__convert_domain(kwargs)

        elif Type == 'app':
            self.appID = kwargs['id']
            self.appName = kwargs['name']
            self.appIcon = kwargs['icon']

            if kwargs['domain']:
                self.domain = self.__convert_domain(kwargs['domain'])    


        elif Type == 'ip':
            self.__convert_and_set_ip(kwargs)
    
    def __convert_phone(self,phone):
        return f"+{phone['country']['p']} {phone['number']}"

    def __convert_email(self,email):
        return f"{email['name']}@{self.__convert_domain(email['domain'])}"

    def __convert_and_set_ip(self,ip):
        self.ip         = ip['ip']
        self.ipAsn      = ip['asn']
        self.ipOrg      = ip['org']
        self.ipIsp      = ip['isp']
        self.ipPorts    = ip['ports']
        self.ipCountry  = ip['country']['f'] if ip['country'] else None

    def __convert_url(self,url:dict):
        if url['domain']:
            return f"{url['proto']}://{self.__convert_domain(url['domain'])}:{url['port']}{url['path']}" 
        elif url['ip']:
            return f"{url['proto']}://{url['ip']['ip']}:{url['port']}{url['path']}" 

        
        return None 

    def __convert_domain(self,domain:dict):
        return f"{(domain['sub']+'.') if domain['sub'] else ''}{domain['name']}{('.'+domain['suffix']) if domain['suffix']  else ''}"


    def __str__(self) -> str:
        return self.save_format()

    def __radd__(self, other):
        if isinstance(other, str):
            return   other + self.save_format() 
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, str):
            return self.save_format() + other
        else:
            return NotImplemented
          
    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError(f"'Result' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value
        
    
    def print(self,):
        c=""

        if self.VIEW_TYPE == "email" and self.credEmail:
            c+=f"{T.MAGENTA}[ {T.YELLOW}Email{T.MAGENTA} ]{T.MAGENTA}> {T.CYAN}{self.credEmail}{T.RESET}"

        if self.VIEW_TYPE == "password" and self.credPassword:
            c+=f"{T.MAGENTA}[ {T.YELLOW}Email{T.MAGENTA} ]{T.MAGENTA}> {T.CYAN}{self.credPassword}{T.RESET}"

        if self.VIEW_TYPE == "username" and self.credUsername:
            c+=f"{T.MAGENTA}[ {T.YELLOW}Email{T.MAGENTA} ]{T.MAGENTA}> {T.CYAN}{self.credUsername}{T.RESET}"
        
        if self.VIEW_TYPE == "app" and self.appID:
            if self.appID:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA} ]{T.RED}{T.MAGENTA}>  {T.CYAN}{self.appID}{T.RESET}\n"
            if self.appName:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA} ]{T.RED}{T.MAGENTA}> {T.RED} Name{T.RESET}{' ':10}: {T.CYAN}{self.appName}{T.RESET}\n"
            if self.appIcon:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA} ]{T.RED}{T.MAGENTA}> {T.RED} Icon{T.RESET}{' ':10}: {T.CYAN}{self.appIcon}{T.RESET}\n"
            if self.appDomain:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Domain{T.RESET}{' ':8}: {T.CYAN}{self.appDomain}{T.RESET}\n"
            
        if self.VIEW_TYPE == "url" and self.url:
            if self.url:c+=f"{T.MAGENTA}[ {T.YELLOW}URL{T.MAGENTA}  ]{T.MAGENTA}>  {T.CYAN}{self.url}{T.RESET}\n"
            if self.urlPath:c+=f"{T.MAGENTA}[ {T.YELLOW}URL{T.MAGENTA}  ]{T.MAGENTA}> {T.RED} Path{T.RESET}{' ':10}: {T.CYAN}{self.urlPath}{T.RESET}\n"
            if self.urlPort:c+=f"{T.MAGENTA}[ {T.YELLOW}URL{T.MAGENTA}  ]{T.MAGENTA}> {T.RED} Port{T.RESET}{' ':10}: {T.CYAN}{self.urlPort}{T.RESET}\n"

        if self.VIEW_TYPE == "ip" and self.ip:
            if self.ip:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA} ]{T.MAGENTA}>  {T.BLUE}{self.ip}{T.RESET}\n"
            if self.ipPorts:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA} ]{T.RED}{T.MAGENTA}> {T.RED} Ports{T.RESET}{' ':9}: {T.CYAN}{self.ipPorts}{T.RESET}\n"
            if self.ipAsn:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA} ]{T.RED}{T.MAGENTA}> {T.RED} Asn{T.RESET}{' ':11}: {T.CYAN}{self.ipAsn}{T.RESET}\n"
            if self.ipIsp:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA} ]{T.RED}{T.MAGENTA}> {T.RED} Isp{T.RESET}{' ':11}: {T.CYAN}{self.ipIsp}{T.RESET}\n"
            if self.ipOrg:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA} ]{T.RED}{T.MAGENTA}> {T.RED} Org{T.RESET}{' ':11}: {T.CYAN}{self.ipOrg}{T.RESET}\n"
            if self.ipCountry:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA} ]{T.MAGENTA}>{T.RED}  Country{T.RESET}{' ':7}: {T.CYAN}{self.ipCountry}{T.RESET}\n"

        if self.VIEW_TYPE in ["domain", 'subdomain', 'related'] and self.domain:
            c+=f"{T.MAGENTA}[ {T.YELLOW}Domain{T.MAGENTA} ]{T.MAGENTA}> {T.CYAN}{self.domain}{T.RESET}"

        if self.VIEW_TYPE == "phone" and self.credPhone:
            return f"{T.MAGENTA}> {T.CYAN}{self.credPhone}{T.RESET}"

        if self.VIEW_TYPE == "cred":
            if self.url:c+=f"{T.MAGENTA}[ {T.YELLOW}URL{T.MAGENTA}  ]{T.MAGENTA}>  {T.BLUE}{self.url}{T.RESET}\n"
            if self.appID:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA}  ]{T.RED}{T.MAGENTA}>  {T.CYAN}{self.appID}{T.RESET}\n"
            if self.credEmail:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Email{T.RESET}{' ':9}: {T.GREEN}{self.credEmail}{T.RESET}\n"
            if self.credUsername and not self.credEmail:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Username{T.RESET}{' ':6}: {T.GREEN}{self.credUsername}{T.RESET}\n"
            if self.credPassword:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Password{T.RESET}{' ':6}: {T.GREEN}{self.credPassword}{T.RESET}\n"
            if self.credPhone:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Phone{T.RESET}{' ':9}: {T.GREEN}{self.credPhone}{T.RESET}\n"
            if self.credCountry:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}>{T.RED}  Country{T.RESET}{' ':7}: {T.CYAN}{self.credCountry}{T.RESET}\n"

        if self.VIEW_TYPE == "full":
            if self.url:c+=f"{T.MAGENTA}[ {T.YELLOW}URL{T.MAGENTA}  ]{T.MAGENTA}>  {T.BLUE}{self.url}{T.RESET}\n"
            if self.urlPath and self.urlPath != '/':c+=f"{T.MAGENTA}[ {T.YELLOW}URL{T.MAGENTA}  ]{T.MAGENTA}> {T.RED} Path{T.RESET}{' ':10}: {T.CYAN}{self.urlPath}{T.RESET}\n"
            if self.urlPort and self.urlPort not in [80, 443]:c+=f"{T.MAGENTA}[ {T.YELLOW}URL{T.MAGENTA}  ]{T.MAGENTA}> {T.RED} Port{T.RESET}{' ':10}: {T.CYAN}{self.urlPort}{T.RESET}\n"
            if self.ip:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA}   ]{T.MAGENTA}>  {T.BLUE}{self.ip}{T.RESET}\n"
            if self.ipPorts:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA}   ]{T.RED}{T.MAGENTA}> {T.RED} Ports{T.RESET}{' ':9}: {T.CYAN}{self.ipPorts}{T.RESET}\n"
            if self.ipAsn:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA}   ]{T.RED}{T.MAGENTA}> {T.RED} Asn{T.RESET}{' ':11}: {T.CYAN}{self.ipAsn}{T.RESET}\n"
            if self.ipIsp:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA}   ]{T.RED}{T.MAGENTA}> {T.RED} Isp{T.RESET}{' ':11}: {T.CYAN}{self.ipIsp}{T.RESET}\n"
            if self.ipOrg:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA}   ]{T.RED}{T.MAGENTA}> {T.RED} Org{T.RESET}{' ':11}: {T.CYAN}{self.ipOrg}{T.RESET}\n"
            if self.ipCountry:c+=f"{T.MAGENTA}[ {T.YELLOW}IP{T.MAGENTA}   ]{T.MAGENTA}>{T.RED}  Country{T.RESET}{' ':7}: {T.CYAN}{self.ipCountry}{T.RESET}\n"
            
            if self.appID:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA}  ]{T.RED}{T.MAGENTA}>  {T.CYAN}{self.appID}{T.RESET}\n"
            if self.appName:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA}  ]{T.RED}{T.MAGENTA}> {T.RED} Name{T.RESET}{' ':10}: {T.CYAN}{self.appName}{T.RESET}\n"
            if self.appIcon:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA}  ]{T.RED}{T.MAGENTA}> {T.RED} Icon{T.RESET}{' ':10}: {T.CYAN}{self.appIcon}{T.RESET}\n"
            if self.appDomain:c+=f"{T.MAGENTA}[ {T.YELLOW}APP{T.MAGENTA}  ]{T.MAGENTA}> {T.RED} Domain{T.RESET}{' ':8}: {T.CYAN}{self.appDomain}{T.RESET}\n"
            
            if self.credEmail:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Email{T.RESET}{' ':9}: {T.GREEN}{self.credEmail}{T.RESET}\n"
            if self.credUsername and not self.credEmail:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Username{T.RESET}{' ':6}: {T.GREEN}{self.credUsername}{T.RESET}\n"
            if self.credPassword:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Password{T.RESET}{' ':6}: {T.GREEN}{self.credPassword}{T.RESET}\n"
            if self.credPhone:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}> {T.RED} Phone{T.RESET}{' ':9}: {T.GREEN}{self.credPhone}{T.RESET}\n"
            if self.credCountry:c+=f"{T.MAGENTA}[ {T.YELLOW}CRED{T.MAGENTA} ]{T.MAGENTA}>{T.RED}  Country{T.RESET}{' ':7}: {T.CYAN}{self.credCountry}{T.RESET}\n"

        return c            

    def save_format(self):
        result = []
        if self.VIEW_TYPE in ['cred', 'full']:
            # 1 
            if self.url:
                result.append(self.url)
            elif self.appID:
                result.append(self.appID)
            else:
                result.append('')

            # 2
            if self.credUsername:
                result.append(self.credUsername)
            elif self.credEmail:
                result.append(self.credEmail)
            else:
                result.append('')
            
            # 3 
            if self.credPassword:
                result.append(self.credPassword)
            else:
                result.append('')
            
            # 4 
            if self.credCountry:
                result.append(self.credCountry)
            else:
                result.append('')
            
            # 5
            #if self.credDate:
            #    result.append(self.credDate)
            #else:
            #    result.append('')

            return result

        elif self.VIEW_TYPE in ['subdomain', 'related', 'domain']:
            return self.domain
        
        elif self.VIEW_TYPE == 'email':
            return self.credEmail

        elif self.VIEW_TYPE == 'phone':
            return self.credPhone

        elif self.VIEW_TYPE == 'username':
            return self.credUsername
        
        elif self.VIEW_TYPE == 'password':
            return self.credPassword
        
        
        elif self.VIEW_TYPE == 'ip':
            return self.ip
        
        elif self.VIEW_TYPE == 'app':
            return self.appID

        elif self.VIEW_TYPE == 'url':
            return self.url
        else:
            return 'null'
