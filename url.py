# -*- coding: utf-8 -*-
"""
Create by: Osamah Awadh (oaokm)
Plugin: Analysis URL
"""

import re

regex = re.compile(
        r'^(?:http|ftp)s?://|www.' # http:// or https:// or www.
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

class URL:
    def __init__(self, url:str):
        self.url     = url
        self._is_url = re.match(regex, self.url) is not None
    
    def components(self):
        if self._is_url:
            protocol    = self.url.split(':')[0]
            domain      = self.url.split(':')[1][2:].split('/')[0]
            path        = '/'.join(self.url.split(':')[1][2:].split('/')[1:])
            pramter     = path.split("?")[1] if path.count('?') == 1 else ''
            pathWithoutPramter = path.split("?")[0]
            anchor      = path.split('#')[-1] if path.find('#') != -1 else ''
            ANAtopLevel = self.url.split(':')[1][2:].split('/')[0].split('.')
            topLevel    = list()
            for look in ANAtopLevel:
                if len(look) <= 5:
                    topLevel.append(look)
                else:
                    continue

            return {
                'url': self.url,
                'protocol': protocol,
                'domain': domain,
                'topLevel': '|'.join(topLevel),
                'path': ''.join(['/', path]),
                "pramter": ''.join(['?', pramter]),
                "pathWithoutPramter": ''.join(['/', pathWithoutPramter]),
                'anchor': anchor
            }
        else:
            return False
    
    def __repr__(self) -> str:
        return f"<url: '{self.url}' | is-url: {self._is_url}>"


if __name__ == '__main__':
    urlForTest  = ["https://en.wikipedia.org/search?q=dsds+s#vf", 'https://google.com/Image/png.png?4654fdsdf']
    urlAnalysis = URL(url=urlForTest[1])
    print(f"[urlAnalysis > components] {urlAnalysis.components()}")
    
    