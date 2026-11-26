"""Public web entrypoint. Run behind Gunicorn and the hosting platform's HTTPS proxy."""
import json, time, threading
from collections import deque
from urllib.parse import parse_qs
from pathlib import Path
from server import allowed, lookup
ROOT=Path(__file__).resolve().parent
calls=deque(); lock=threading.Lock(); slots=threading.BoundedSemaphore(3)

def application(environ,start_response):
    def respond(status,body,typ='application/json; charset=utf-8'):
        if not isinstance(body,bytes):body=json.dumps(body,ensure_ascii=False).encode()
        start_response(status,[('Content-Type',typ),('Content-Length',str(len(body))),('Cache-Control','no-store'),('X-Content-Type-Options','nosniff'),('Referrer-Policy','no-referrer'),('X-Frame-Options','DENY'),('Content-Security-Policy',"default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")]);return [body]
    if environ.get('REQUEST_METHOD')!='GET':return respond('405 Method Not Allowed',{'error':'Tylko GET'})
    path=environ.get('PATH_INFO','/')
    if path in ('/','/kalkulator.html'):return respond('200 OK',(ROOT/'kalkulator.html').read_bytes(),'text/html; charset=utf-8')
    if path=='/health':return respond('200 OK',{'status':'ok'})
    if path!='/api/vehicle':return respond('404 Not Found',{'error':'Nie znaleziono'})
    query=environ.get('QUERY_STRING','')
    if len(query)>4096:return respond('400 Bad Request',{'error':'Link jest za długi'})
    url=parse_qs(query).get('url',[''])[0]
    if not allowed(url):return respond('400 Bad Request',{'error':'Dozwolone są wyłącznie linki HTTPS do ofert aukcyjnych'})
    with lock:
        now=time.monotonic()
        while calls and calls[0]<=now-60:calls.popleft()
        if len(calls)>=30:return respond('429 Too Many Requests',{'error':'Limit zapytań — spróbuj później lub wybierz stan ręcznie'})
        calls.append(now)
    if not slots.acquire(blocking=False):return respond('503 Service Unavailable',{'error':'Serwer zajęty — wybierz stan ręcznie lub spróbuj ponownie'})
    try:
        try:data=lookup(url)
        except Exception:data=None
        return respond('200 OK',data) if data else respond('502 Bad Gateway',{'error':'Brak publicznie dostępnej lokalizacji'})
    finally:slots.release()
