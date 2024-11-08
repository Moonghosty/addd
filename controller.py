from flask import Flask, Blueprint, render_template,redirect,url_for,session,flash, request, abort,make_response
from models.model import lista_tarefas
import _json

controllerI = Blueprint('controllerI', __name__)

@controllerI.route('/')
def index():
    return render_template('index.html')

@controllerI.route('/index', methods=['GET', 'POST'])
def add():
    if request.method =="POST":
        



@controllerI.route('/logout')
def logout():
    response=make_response(redirect(url_for("controllerI.index")))
    session.pop("id", None) #"remove" o usuário
    response.set_cookie('nome', '', expires=0)
    response.set_cookie('senha', '', expires=0)
    return response