import urllib.request
import re

try:
    # Get the wikipedia page for actor vivek
    req = urllib.request.Request('https://en.wikipedia.org/wiki/Vivek_(actor)', headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    # Find the main infobox image
    # Looking for: <img alt="..." src="//upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Vivek_at_an_event_in_2016.png/220px-Vivek_at_an_event_in_2016.png" decoding="async" width="220" height="295" class="mw-file-element" data-file-width="604" data-file-height="808" />
    match = re.search(r'<img[^>]+src="([^"]+Vivek[^"]+)"[^>]*>', html, re.IGNORECASE)
    
    if match:
        url = match.group(1)
        if url.startswith('//'):
            url = 'https:' + url
            
        print("Found URL:", url)
        
        # Download the image
        img_req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        img_data = urllib.request.urlopen(img_req).read()
        
        with open('static/images/vivek_sir.png', 'wb') as f:
            f.write(img_data)
        print("Successfully saved to static/images/vivek_sir.png")
    else:
        print("Couldn't find image URL in HTML.")
except Exception as e:
    print("Error:", e)
