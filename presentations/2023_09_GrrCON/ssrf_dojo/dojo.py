import requests
import socket
import time
from flask import Flask, request, redirect, abort  
  
app = Flask(__name__)

required_token = "eyJ1c2VyIjoiZGVwbG95bWVudGFkbWluIiwicGFzcyI6Ik15U3VwZXJTZWNyZXRQd2QifQ=="
bind_port = 8000

@app.route('/cornerkick', methods=['GET'])  
def cornerkick():  
    url = request.args.get('url', f'http://127.0.0.1:{bind_port}')  
    headers = {'BackendToken':required_token}    
      
    try:
        # check header   
        if not (request.headers.get('metadata') and request.headers.get('metadata').lower() == 'true'):  
            raise ValueError("error")

        # send web request   
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=5)  
        if(response.status_code == 200):  
            return response.text 
        else:  
            raise ValueError("error")    
        
    except Exception as e:    
        return f"Access denied to CornerKick. Metadata header missing. The proper URL could look like http://127.0.0.1:{bind_port}/cornerkick?url=http://127.0.0.1:{bind_port}/flag", 403

@app.route('/leakyfaucet', methods=['GET'])  
def leakyfaucet():  
    url = request.args.get('url', f'http://127.0.0.1:{bind_port}')
    legacyauth = request.args.get('legacyauth', 'False') 
    headers = {}
    
    # check authentication
    if(legacyauth == 'True'):
        headers = {'BackendToken':required_token}
    else:
         headers = {'Hint':'&legacyauth=False'}  
    
    try:  
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=5)  
          
        if(response.status_code == 200):  
            return response.text 
        else:  
             raise ValueError("error")  
      
    except Exception as e:  
        return f"Access denied to LeakyFaucet because no valid BackendToken header. The proper URL could look like http://127.0.0.1:{bind_port}/leakyfaucet?url=http://127.0.0.1:{bind_port}/flag", 403

@app.route('/shapeshifter', methods=['GET'])  
def shapeshifter():  
    url = request.args.get('url', f'http://127.0.0.1:{bind_port}')  
    headers = {'BackendToken':required_token}    
      
    try:
        # check ip deny list
        if('127.' in url or 'localhost' in url):  
            raise ValueError("error") 

        # send web request   
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=5)  
        if(response.status_code == 200):  
            return response.text 
        else:  
            raise ValueError("error")    
        
    except Exception as e:    
        return f"Access denied to ShapeShifter. We don't allow 127.0.0.1. The proper URL could look like http://127.0.0.1:{bind_port}/shapeshifter?url=http://127.0.0.1:{bind_port}/flag", 403

@app.route('/misguidedparser', methods=['POST'])
def misguidedparser():
    url = request.form.get('url', f'http://127.0.0.1:{bind_port}')
    legacyauth = request.args.get('legacyauth', 'True')
    headers = {}

    if(legacyauth == 'True'):
        headers = {'BackendToken':required_token}

    try:
        response = requests.get(url + "/notflag", headers=headers, allow_redirects=False)

        if(response.status_code == 200):
            return response.text
        else:
            raise ValueError("error")

    except Exception as e:
        return f"Access denied to MisguidedParser. Wherever you go, you always visit /notflag. The proper URL could look like http://127.0.0.1:{bind_port}/misguidedparser?url=http://127.0.0.1:{bind_port}/flag", 403

@app.route('/detour', methods=['GET'])  
def detour():  
    url = request.args.get('url', f'http://127.0.0.1:{bind_port}')  
    legacyauth = request.args.get('legacyauth', 'True')  
    headers = {}   
      
    if(legacyauth == 'True'):  
        headers = {'BackendToken':required_token}    
      
    try:
        # check port deny list
        if f':{bind_port}' in url:  
            raise ValueError("error") 

        response = requests.get(url, headers=headers, allow_redirects=True, timeout=5)    
            
        if(response.status_code == 200):    
                return response.text  
        else:    
            raise ValueError("error")    
        
    except Exception as e:    
        return f"Access denied to Detour. We don't allow connections to port {bind_port}. The proper URL could look like http://127.0.0.1:{bind_port}/detour?url=http://127.0.0.1:{bind_port}/flag", 403
  
@app.route('/baitandswitch', methods=['GET'])  
def baitandswitch():  
    url = request.args.get('url', f'http://127.0.0.1:{bind_port}')  
    legacyauth = request.args.get('legacyauth', 'True')  
    headers = {}  
  
    if(legacyauth == 'True'):  
        headers = {'BackendToken':required_token}  
  
    try:  
        # check ip deny list 
        hostname = url.replace("https://", "").replace("http://", "").split(":")[0].split("/")[0]  
        ip_address = socket.gethostbyname(hostname)
        print("DNS resolution: " + str(ip_address))  
        if '127.' in ip_address:  
            raise ValueError("error")  
  
        # send web request   
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=5)  
        if(response.status_code == 200):  
            return response.text  
        else:  
            raise ValueError("error")  
    except Exception as e:  
        return f"Access denied to BaitAndSwitch. We require you use DNS that does not point to 127/8. The proper URL could look like http://127.0.0.1:{bind_port}/baitandswitch?url=http://localhost:{bind_port}/flag", 403  
        
@app.route('/flag', methods=['GET'])  
def flag():
    BackendToken = request.headers.get('BackendToken', None)  
    
    if(BackendToken is not None and BackendToken == required_token):  
        return f"You captured the flag!", 200  
    else:  
        return f"Unauthorized: BackendToken required.", 401   
  
if __name__ == '__main__':  
    app.run(debug=False, port=bind_port)
