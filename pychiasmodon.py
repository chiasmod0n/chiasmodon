import sys
import time
import requests
import tldextract
from yaspin import Spinner

VERSION = "0.2.28"

class Chiasmodon:
    API_URL         = 'https://beta.chiasmodon.com/v2/api/beta'
    API_HEADERS     = {'user-agent':'cli/python'}
    VIEW_TYPE = {
        'cred':['domain', 'email', 'cidr', 'app', 'asn', 'username','password'],
        'url':['domain', 'email', 'cidr', 'asn', 'username','password'],
        'subdomain':['domain'],
        'email':['domain', 'cidr', 'asn', 'app' ],
        'password':['domain', 'cidr', 'app', 'asn', 'email' 'username'],
        'username': ['domain', 'cidr', 'app', 'asn', 'email','password'],
        'app':['cidr', 'asn', 'email', 'username','password'],
    }

    METHODS= [
    'domain',
    'email',
    'asn',
    'cidr',
    'app',
    'username',
    'password',
    ]

    class T:
        RED      = '\033[91m'
        GREEN    = '\033[92m'
        YELLOW   = '\033[93m'
        BLUE     = '\033[94m'
        MAGENTA  = '\033[95m'
        CYAN     = '\033[96m'
        RESET    = '\033[0m'
    def __init__(self, token=None, color=True, debug=True,check_token=True) -> None:

        self.token = token
        self.debug = debug
        self.err :bool   = False 
        self.msg :str    = '' 
        self.__result:list[Result] = []
        
        if not color:
            self.T.RED      = ''
            self.T.GREEN    = ''
            self.T.YELLOW   = ''
            self.T.BLUE     = ''
            self.T.MAGENTA  = ''
            self.T.CYAN     = ''
            self.T.RESET    = ''
        
        if self.token and check_token:
            if self.__check_token():
                self.print(f'{self.T.GREEN}Set token successfully{self.T.RESET}')

            else:
                self.print(f'{self.T.RED}{self.msg}{self.T.RESET}')
                sys.exit()
    
    def filter_domain(self,d) -> str:
        x = tldextract.extract(d)
        if x.subdomain:return '{}.{}.{}'.format(x.subdomain,x.domain, x.suffix)
        else:return '{}.{}'.format(x.domain, x.suffix)

    def print(self,text, ys=None, ys_err=False) -> None:
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
            'token':    self.token,
            'method':   'check-token'
        }).get('is_active'):
            return True 

        return False 

    def __request(self, data:dict,timeout=60):

        try:
            resp = requests.post(self.API_URL, data=data, headers=self.API_HEADERS, timeout=timeout)
            resp.close()
            resp = resp.json()
            try:
                if resp.get('err'):
                    self.err = True 
                    self.msg = resp['msg']
            except:pass
            return resp
        except Exception as e:
            self.print(f"{self.T.RED}Request error: {e}\nPlease try agine later.{self.T.RESET}")
            sys.exit()


    def __proc_query(self, 
                    method:str, 
                    query:str, 
                    view_type:str, 
                    country:str,
                    timeout:int,
                    sort:bool, 
                    only_domain_emails:bool,
                    all:bool,
                    limit:int,
                    callback_view_result:None,
                    yaspin:bool,
                    ) -> dict:
        
        result : list[Result] = []

        data = {

            'token':self.token,
            'type-view':view_type,
            'method' : 'search-by-%s' % method,
            'query' : query,
            'country' : country.upper(),
            'all':'yes' if all else 'no',
            'domain-emails':'yes' if only_domain_emails else 'no',
            'get-info':'yes'
        }
        

        if yaspin:
            with yaspin(Spinner(["🐟","🐠","🐡","🐬","🐋","🐳","🦈","🐙","🐚","🪼","🪸"], 200),text=f"Processing {query} ...") as sp:
                process_info = self.__request(
                    data=data,
                    timeout=timeout,
                )

            if process_info and process_info.get('count') == 0:
                if method == 'domain' and not all and not only_domain_emails:
                    self.print(f"{self.T.RED}Not found result\nTo view more result try: --all  {self.T.RESET}", sp,ys_err=True)
                else:
                    self.print(f"{self.T.RED}Not found result{self.T.RESET}", sp,ys_err=True)

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
                self.print(f"{self.T.RED}Not found result{self.T.RESET}")
                return result
            
        
        del data['get-info'] 

        if self.err:
            self.err= False
            raise Exception(f'{self.T.RED}Error: {self.msg}{self.T.RESET}') 

        self.print(f"{self.T.YELLOW}Result count{self.T.YELLOW}: {self.T.GREEN}{process_info['count']}{self.T.RESET}")

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
                if yaspin:self.print(f"{self.T.RED}{self.msg}{self.T.RESET}", YS, ys_err=True);YS.fail("💥 ");YS.stop()
                return result
            
            for r in beta_result['data']:
                
                if r.__class__ == dict:
                    column :Result = Result(**r)
                else:
                    column :Result = Result(**{view_type:r})

                if len(result) == limit:
                    if yaspin:YS.text='';YS.stop()
                    return result

                if sort and column in self.__result:
                    continue
                
                if callback_view_result:
                    callback_view_result(beta=column, view_type=view_type, ys=YS)

                result.append(column)
                self.__result.append(column)

            if beta_result['done']:
                if yaspin:YS.text='';YS.stop()
                return result

            time.sleep(0x1)

        if not result:
            
            if yaspin:self.print(f"{self.T.RED}Not found result{self.T.RESET}", YS,ys_err=True);YS.fail("💥 ");YS.stop()
            else:self.print(f"{self.T.RED}Not found result{self.T.RESET}")
        else:
            if yaspin:YS.text='';YS.stop()

        return result
    
    def search(self,
               query,
               method='domain',
               country='all',
               view_type='cred',
               limit=10000,
               all=False,
               only_domain_emails=False,
               timeout=60,
               sort=True,
               yaspin=False,
               callback_view_result=None) -> dict:
        
        
        if method not in self.METHODS:
            raise Exception(f"{self.T.RED}not found this method: {method}.{self.T.RESET}")
        
        if method not in self.VIEW_TYPE[view_type]:
            raise Exception(f"{self.T.RED}{view_type} doesn't support ({method}).{self.T.RESET}")

        if only_domain_emails and method != 'domain':
            raise Exception(f"{self.T.RED}domain emails support only (domain) method.{self.T.RESET}")
        
        if all and method not in ['app', 'domain']:
            raise Exception(f"{self.T.RED}all support only methods (app, domain).{self.T.RESET}")
        
        self.err = False
        self.msg = ''

        if method == 'domain':query = self.filter_domain(query)

        result = self.__proc_query(
            method=method,
            query=query,
            country=country,
            view_type=view_type,
            sort=sort,
            timeout=timeout,
            only_domain_emails=only_domain_emails,
            all=all,
            limit=limit,
            callback_view_result=callback_view_result,
            yaspin=yaspin,
        )

        self.__result:list = []

        return result

class Result(dict):
    def __init__(self,
                url=None,
                password=None,
                username=None,
                app_name=None,
                app_id=None,
                subdomain=None,
                country=None,
                date=None,
                ip=None,
                email=None,
                ) -> None:

        self.url        = url 
        self.password   = password 
        self.username   = username 
        self.app_name   = app_name 
        self.app_id     = app_id 
        self.country    = country 
        self.subdomain  = subdomain
        self.date       = date 
        self.ip         = ip 
        self.email      = email
    
    def __str__(self) -> str:
        if (self.url and self.date ) or (self.app_id and self.date):
            return super().__str__()
        else:
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
        
    def save_format(self):
        if (self.url and self.date ) or (self.app_id and self.date):
            return [
                self.url if self.url else self.app_id,
                self.username if self.username else self.email,
                self.password,
                self.country,
                self.date,
            ]
        
        else:
            for i in list(self.values()):
                if i != None:return i