import requests

class TicsMetricsReport:

    def __init__(self, unit_name):
        self.unit_name = unit_name

    def get_coverity_errors(self, level):
        return self._get_tics_metrics("AI", str(level))

    def get_security_errors(self, level):
        return self._get_tics_metrics("SEC", str(level))

    def _get_tics_metrics(self, metric_type, level):
        url_gen = 'http://nlybstqvp4vws04.code1.emi.philips.com:42506/tiobeweb/IGT-New/api/public/v1/Measure?'
        node = "HIE://Allura_Main_" + self.unit_name + "_PreInt/main"
        metrics = "G(Violations(" + metric_type + "),Level(" + level + "))"
        parameters = {'metrics': metrics, 'nodes': node}

        print("get coverity info url=" + url_gen + " metrics=" + metrics + " nodes=" + node)

        service = requests.Session()
        service.trust_env = False
        response = service.get(url=url_gen, params=parameters, allow_redirects=True, cookies={'coockies': 'coockies'})
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
        return data["data"][0]["value"]
