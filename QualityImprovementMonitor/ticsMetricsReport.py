import requests
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser 
  
class TicsMetricsReport:

    def __init__(self, unit_name):
        self.unit_name = unit_name

    def get_coverity_errors(self, level):
        self.new_url='https://nlybstqvp4vws04.code1.emi.philips.com/tiobeweb/IGT-New/api/public/v1/Measure?metrics=G%28Violations%28AI%29%2CLevel%281%29%29&nodes=HIE%3A%2F%2FAllura_Main_'+ self.unit_name+'_PreInt%2Fmain'
        return self._get_tics_metrics("AI", str(level))

    def get_security_errors(self, level):
        #self.new_url='https://nlybstqvp4vws04.code1.emi.philips.com/tiobeweb/IGT-New/api/public/v1/Measure?metrics=G%28Violations%28SEC%29%2CLevel%281%29%29&nodes=HIE%3A%2F%2FAllura_Main_'+ self.unit_name+'_PreInt%2Fmain'
        
        self.new_url='https://nlybstqvp4vws04.code1.emi.philips.com/tiobeweb/IGT-New/api/public/v1/Measure?metrics=G%28Violations%28SEC%29%2CLevel%28'+str(level)+'%29%29&nodes=HIE%3A%2F%2FAllura_Main_'+ self.unit_name+'_PreInt%2Fmain'
        return self._get_tics_metrics("SEC", str(level))
        
    ###########################################################
    def get_count_of_errotype(self,tictype):
       self.new_url='https://nlybstqvp4vws04.code1.emi.philips.com/tiobeweb/IGT-New/api/public/v1/Measure?metrics=' + tictype +'%29%2CLevel%81%29%29&nodes=HIE%3A%2F%2FAllura_Main_' + self.unit_name + '_PreInt%2Fmain'
       return self._get_tics_metrics("SEC", str(1))
       
    ###########################################################

    def _get_tics_metrics(self, metric_type, level):
        #url_gen = 'http://nlybstqvp4vws04.code1.emi.philips.com:42506/tiobeweb/IGT-New/api/public/v1/Measure?'
        url_gen = 'http://nlybstqvp4vws04.code1.emi.philips.com:42506/tiobeweb/IGT-New/api/public/v1/Measure?'
        node = "HIE://Allura_Main_" + self.unit_name + "_PreInt/main"
        metrics = "G(Violations(" + metric_type + "),Level(" + level + "))"
        parameters = {'metrics': metrics, 'nodes': node}

        print("get coverity info url=" + url_gen + " metrics=" + metrics + " nodes=" + node)

        service = requests.Session()
        service.trust_env = False
        
        configur = ConfigParser()
        configur.read('config.ini')
        uid=configur.get('user info','UID')
        pwd=configur.get('user info','PWD')
        
        auth = HTTPBasicAuth(uid, pwd)
        print (' ASD$$$$$$$$$ ',auth)
        
        print(' parameter :  ',parameters)
        print('type of Node= ',type(self.unit_name))
        real_url=url_gen+metrics+node
        #new_url='https://nlybstqvp4vws04.code1.emi.philips.com/tiobeweb/IGT-New/api/public/v1/Measure?metrics=G%28Violations%28AI%29%2CLevel%281%29%29&nodes=HIE%3A%2F%2FAllura_Main_'+ self.unit_name+'_PreInt%2Fmain'
        
        print( '  Tic URL= ', self.new_url);  
        #response = service.get(url=url_gen, params=parameters, allow_redirects=True, cookies={'coockies': 'coockies'})
        response=service.get(url=self.new_url,auth=HTTPBasicAuth(uid,pwd), allow_redirects=True, cookies={'coockies': 'coockies'})
        #response = service.get('https://nlybstqvp4vws04.code1.emi.philips.com/tiobeweb/IGT-New/api/public/v1/Measure?metrics=G%28Violations%28AI%29%2CLevel%281%29%29&nodes=HIE%3A%2F%2FAllura_Main_Acq_PreInt%2Fmain',auth=HTTPBasicAuth(uid, pwd),allow_redirects=True, cookies={'coockies': 'coockies'})
        response.raise_for_status()
        print(' response code  AAMR1 ',response.status_code)
        if response.status_code == 200:
            data = response.json()
        print(' data["data"]  AAMR1_2-  ',data["data"][0]["value"]) 
        if data["data"][0]["value"] is None :
           return 0;        
        return round(data["data"][0]["value"],2)
