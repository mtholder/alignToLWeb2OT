import sys
url = 'http://tolweb.org/onlinecontributors/app'
data = {'service': 'external',
        'page': 'xml/TreeStructureService',
        'node_id': 1
}
sys.exit('''This script is deprecated because it makes an expensive request of the ToLWeb servers.
It is preserved here for posterity sake, but not functional.
Remove this line and on comment the following lines if you need to run it again.

See http://tolweb.org/tree/home.pages/downloadtree.html for information
on tolweb APIs.
''')
#import requests
#import codecs
#response = requests.get(url, params=data)
#fn = 'tolweb.xml'
#with codecs.open(fn, 'w', encoding='utf-8') as fo:
    #fo.write(response.content)

