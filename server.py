"""Local-only HTTP server; fetch public listing pages without bypassing restrictions."""
import json, re, os
from pathlib import Path
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs, urlencode
from urllib.request import Request, build_opener, HTTPRedirectHandler
ROOT=Path(__file__).resolve().parent
HOSTS={'copart.com','www.copart.com','iaai.com','www.iaai.com','bid.cars','www.bid.cars'}
STATES=set('AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split())
def allowed(url):
    try:
        u=urlsplit(url)
        return u.scheme=='https' and u.hostname in HOSTS and not u.username and not u.password and u.port in (None,443) and bool(re.search(r'/(?:lot/(?:[01]-)?\d+|VehicleDetail/\d+)(?:/|$)',u.path,re.I))
    except ValueError:return False
class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if not allowed(newurl):raise ValueError('Redirect outside listing allowlist')
        return super().redirect_request(req,fp,code,msg,headers,newurl)
class Text(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.skip=0;self.in_title=False;self.title=''
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','noscript','template'):self.skip+=1
        if tag=='title':self.in_title=True
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript','template'):self.skip=max(0,self.skip-1)
        if tag=='title':self.in_title=False
    def handle_data(self,data):
        if self.skip:return
        if self.in_title:self.title+=data
        if data.strip():self.parts.append(' '.join(data.split()))
def parse_location(value):
    value=' '.join(value.split());m=re.fullmatch(r'([A-Z]{2})\s*[-–—]\s*([\w .\'/-]{2,65})',value,re.I)
    if m and m[1].upper() in STATES:return f'{m[2]} ({m[1].upper()})'
    m=re.fullmatch(r'([\w .\'/-]{2,65}?)\s*(?:\(([A-Z]{2})\)|,\s*([A-Z]{2}))',value,re.I)
    if m and (m[2] or m[3]).upper() in STATES:return f'{m[1].strip()} ({(m[2] or m[3]).upper()})'
    return None
def extract(html):
    p=Text();p.feed(html);text='\n'.join(p.parts)
    # Pickup location is more useful than sale location for off-site vehicles.
    loc=None
    for label in ('Pickup Location','Pick up Location','Vehicle Location','Sale Location','Lokalizacja pojazdu','Lokalizacja','Location','Branch'):
        for m in re.finditer(r'(?im)(?:^|\n)'+re.escape(label)+r'\s*:?\s*(?:\n\s*)?([^\n]{2,90})',text):
            v=m[1].strip();loc=parse_location(v)
            if not loc:
                # City and state occasionally are separate inline elements.
                tail=text[m.end():].splitlines();next_line=next((x for x in tail if x.strip()),'');loc=parse_location(v+' '+next_line) if re.fullmatch(r'\([A-Z]{2}\)',next_line) else None
            if loc:break
        if loc:break
    if not loc:return None
    pm=re.search(r'(?im)(?:^|\n)(?:Shipping from|Wysyłka z|Port wysyłkowy)\s*:?\s*([^\n]{2,90})',text)
    port=parse_location(pm[1]) if pm else None
    return {'location':loc,'port':port,'title':p.title.strip()[:160],'source':'Odczyt publicznej strony — potwierdź miejsce odbioru'}
def fetch_page(url):
    if not allowed(url):raise ValueError('Invalid listing URL')
    req=Request(url,headers={'User-Agent':'ImportUSA/1.3 (local quote calculator)','Accept':'text/html','Accept-Language':'en-US,en;q=0.9'})
    with build_opener(SafeRedirect()).open(req,timeout=7) as r:
        if not allowed(r.geturl()):raise ValueError('Invalid final URL')
        return extract(r.read(3_000_000).decode(r.headers.get_content_charset() or 'utf-8',errors='replace'))
def lookup(url):
    data=fetch_page(url)
    return data
class Handler(BaseHTTPRequestHandler):
    def reply(self,status,data,content='application/json; charset=utf-8'):
        if not isinstance(data,bytes):data=json.dumps(data,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type',content);self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(data)
    def do_GET(self):
        p=urlsplit(self.path)
        if p.path in ('/','/kalkulator.html'):return self.reply(200,(ROOT/'kalkulator.html').read_bytes(),'text/html; charset=utf-8')
        if p.path!='/api/vehicle':return self.reply(404,{'error':'Not found'})
        url=parse_qs(p.query).get('url',[''])[0]
        if not allowed(url):return self.reply(400,{'error':'Dozwolone są wyłącznie linki HTTPS do ofert aukcyjnych'})
        try:data=lookup(url)
        except Exception:data=None
        return self.reply(200,data) if data else self.reply(502,{'error':'Brak publicznie dostępnej lokalizacji lub strona blokuje odczyt'})
if __name__=='__main__':
    print('Kalkulator: http://127.0.0.1:8000 — serwer lokalny',flush=True)
    server=ThreadingHTTPServer(('127.0.0.1',8000),Handler)
    import sys
    if '--open' in sys.argv:
        import webbrowser, threading
        threading.Timer(0.4,lambda: webbrowser.open('http://127.0.0.1:8000')).start()
    server.serve_forever()
