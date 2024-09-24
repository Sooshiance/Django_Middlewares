from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils import timezone


MAX_LIMIT_REQUEST = settings.MAX_LIMIT_REQUEST
TIME_LAPSE = settings.TIME_LAPSE
FIREWALL_RULES = settings.FIREWALL
IDS_SETTINGS = settings.IDS
IPS_SETTINGS = settings.IPS
THREAT_DATA_LOADED = settings.THREAT_DATA_LOADED


# TODO : Multi vector attack defense
class MultiVectorDefenseSystem(MiddlewareMixin):
    def __init__(self, get_response=None):

        self.get_response = get_response

        self.threat_intelligence = self.load_threat_intelligence()
        self.security_layers = self.setup_security_layers()

    def setup_firewall(self):
        # Example: Initialize firewall settings or rules
        firewall_rules = FIREWALL_RULES
        return firewall_rules

    def setup_ids(self):
        # Example: Initialize Intrusion Detection System (IDS) settings
        ids_settings = IDS_SETTINGS
        return ids_settings

    def setup_ips(self):
        # Example: Initialize Intrusion Prevention System (IPS) settings
        ips_settings = IPS_SETTINGS
        return ips_settings

    def load_threat_intelligence(self):
        # Example: Load threat intelligence data from a remote API or local file
        threat_data_url = THREAT_DATA_LOADED
        try:
            response = requests.get(threat_data_url)
            if response.status_code == 200:
                # Assuming the API returns JSON data
                return response.json()
            else:
                return {}
        except requests.RequestException as e:
            # Handle exceptions such as network errors
            print(f"Error loading threat intelligence: {e}")
            return {}

    def setup_security_layers(self):
        # Example: Set up various security measures like firewalls, IDS, IPS, etc.
        security_layers = {
            'firewall': self.setup_firewall(),
            'ids': self.setup_ids(),
            'ips': self.setup_ips(),
        }
        return security_layers

    def process_request(self, request):
        # Implement request processing logic here to utilize the security layers and threat intelligence data.
        pass


class RequestLimitMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get the request count from the cache or initialize it to zero
        request_count = cache.get('request_count', 0)
        last_request_time = cache.get('last_request_time', None)
        # Check if the request limit is reached
        
        # Get the current request time
        current_request_time = timezone.now()
        
        if request_count >= MAX_LIMIT_REQUEST and (last_request_time is None or current_request_time - last_request_time < TIME_LAPSE):
            # Return a custom response or raise an exception
            # or
            # raise Exception('Request limit exceeded')            
            return HttpResponse('Request limit exceeded', status=429)

        # Increment the request count and save it to the cache
        request_count += 1
        cache.set('request_count', request_count)
        
        # Save the current request time to the cache
        cache.set('last_request_time', current_request_time)

        # Pass the request to the next middleware or view
        response = self.get_response(request)

        return response
    

# TODO : You can add this function to a cronjob if you work with Redis
# def reset_request_limit():
#     # Delete the request count and the last request time from the cache
#     cache.delete('request_count')
#     cache.delete('last_request_time')
