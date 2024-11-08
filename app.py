from flask import Flask, render_template
from controllers.controller import controllerI

app = Flask(__name__)
app.secret_key = 'chave_mega_secreta'

app.register_blueprint(controllerI)

@app.errorhandler(404) #erro de pagina não encontrada
def erro404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)  #erro interno no servidor
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)