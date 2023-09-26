from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    print("Raw request:")
    print(request)
    print("Headers:")
    print(request.headers)
    return redirect("http://127.0.0.1:8000/flag", code=302)

if __name__ == '__main__':
    app.run(debug=False, port=5000)
