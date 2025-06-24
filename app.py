if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)from flask import Flask, render_template, request
import socket, ssl, requests, whois
from flask import Flask, render_template, request
import socket, ssl, requests, whois

app = Flask(__name__)

def scan_site(url):
    try:
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        ip = socket.gethostbyname(domain)
        headers = requests.get(url).headers
        whois_info = whois.whois(domain)

        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        return {
            "domain": domain,
            "ip": ip,
            "headers": dict(headers),
            "whois": whois_info.domain_name,
            "ssl_issuer": cert['issuer'][0][0][1] if 'issuer' in cert else 'Unknown',
        }

    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        data = scan_site(url)
        return render_template('index.html', data=data)
    return render_template('index.html')


# ✅ IMPORTANT: This makes it work on Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

