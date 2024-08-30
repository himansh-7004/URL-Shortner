
import webbrowser
from django.http import JsonResponse
import hashlib
from django.urls import reverse
url_shortner_storage = {}

def url_shortner(request):
    url_to_be_shorted = request.GET.get('url')
    
    if not url_to_be_shorted:
        return JsonResponse({'error': 'No URL provided'}, status=400)
    
    # Create a short key using a hash function
    short_key = hashlib.md5(url_to_be_shorted.encode()).hexdigest()[:6]
    
    # Store the mapping in the dictionary
    url_shortner_storage[short_key] = url_to_be_shorted
    
    # Create a shortened URL
    shortened_url = request.build_absolute_uri(reverse('redirect_url', args=[short_key]))
    
    return JsonResponse({'url': url_to_be_shorted, 'shortened_url': shortened_url})

def redirection_url(request, short_key):
    """
    Redirects the user to the original URL based on the shortened key.
    """
    redirection_url = url_shortner_storage.get(short_key)
    
    if not redirection_url:
        return JsonResponse({'error': 'Shortened URL not Found'}, status=404)
    try:
        webbrowser.open(redirection_url)
    except Exception as e:
        return JsonResponse({'error': "Not valid Url"}, status=500)
    
    return JsonResponse({'result': "url opening"}, status=200)
