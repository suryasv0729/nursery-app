import urllib.request
import json

def test():
    try:
        url = "http://router.project-osrm.org/route/v1/driving/80.2366,12.9349;80.2707,13.0827?geometries=geojson"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode('utf-8'))
            print("OSRM Success")
            print("Distance:", data['routes'][0]['distance'])
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    test()
