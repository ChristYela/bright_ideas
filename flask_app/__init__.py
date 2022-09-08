from flask import Flask

app = Flask(__name__)

#  generar la secret key
app.secret_key="hasselhoff"