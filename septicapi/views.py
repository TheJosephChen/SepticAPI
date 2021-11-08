from django.http import JsonResponse
from collections import OrderedDict
import requests, urllib.parse

# Ordered Dictionary collection representing a simple cache
SEARCH_CACHE = OrderedDict()
CACHE_CAPACITY = 10

 
# GET property sewer system is a septic system
# Query parameters:
#   address: (required) address of the property
#   zipcode: (required) zipcode of the property
# Handles the home/septic endpoint for acquiring home sewer system information from a 3rd party API.
# Endpoint is current to the HouseCanary API property details endpoint as of November 11, 2021.
def septic(request):
    addr = urllib.parse.quote_plus(request.GET.get('address', ''))
    zipcode = request.GET.get('zipcode', '')
    cache_key = addr + zipcode

    # Check cache for current query parameters.
    # Perform 3rd party API call if not found. Otherwise load data.
    geodata = get_from_cache(cache_key)
    if geodata == -1:
        # Mock Server Endpoint
        url = 'https://62292a2f-c5e4-4efc-a0ba-f9c563c7890b.mock.pstmn.io/details?address=%s&zipcode=%s' % (addr, zipcode)
        response = requests.get(url)
        geodata = response.json()
        put_to_cache(cache_key, geodata)
    
    # Parse sewer property from response data
    has_septic = { 'septic': False }
    if 'property/details' in geodata:
        if 'result' in geodata['property/details']:
            if 'property' in geodata['property/details']['result']:
                if 'sewer' in geodata['property/details']['result']['property']:
                    has_septic['septic'] = geodata['property/details']['result']['property']['sewer'] == 'septic'
                else:
                    print("key 'sewer' not found")
            else:
                print("key 'property' not found")
        else:
            print("key 'result' not found")
    else:
        print("key 'property/details' not found")
    return JsonResponse(has_septic)


# Searches for the address key in the cache and returns its value if found.
# Updates cache order to facilitate Least Recently Used (LRU) strategy.
# Returns:
#   value of key search_addr if found
#   -1 otherwise
def get_from_cache(search_addr):
    if search_addr not in SEARCH_CACHE:
        return -1
    else:
        SEARCH_CACHE.move_to_end(search_addr)
        return SEARCH_CACHE[search_addr]


# Manages insertion into the cache using a Least Recently Used (LRU) strategy.
def put_to_cache(search_addr, response):
    if len(SEARCH_CACHE) >= CACHE_CAPACITY:
        SEARCH_CACHE.popitem(last = False)
    SEARCH_CACHE[search_addr] = response