from flask import Flask, render_template, redirect, request
import pandas as pd
import sqlalchemy
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
engine = sqlalchemy.create_engine('sqlite:///website.db', echo=True)

Base = declarative_base()

class Contato(Base):
 __tablename__ = 'contatos' 
 id = Column(Integer, primary_key=True) 
 nome = Column(String(100))
 email = Column(String(100))
 celular= Column(String(100))
 tags= Column(String(100))
 links = Column(String(500))

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

familia = "https://cdn-icons-png.flaticon.com/512/2452/2452717.png"
outro = "https://cdn-icons-png.flaticon.com/512/5895/5895032.png"
amigo = "https://cdn-icons-png.flaticon.com/512/1000/1000272.png"
trabalho = "https://cdn-icons-png.flaticon.com/512/1395/1395461.png"

def criar_contato_sql(contato: Contato):
  Session = sessionmaker(bind=engine)
  session = Session()
  #criando a sessão 
  session.add(contato)
  session.commit()
  return 'sucess'

def deletar_contato_sql(id):
  Session = sessionmaker(bind=engine)
  session = Session()
  contato_del = session.query(Contato).filter_by(id=id).first()
  session.delete(contato_del)
  session.commit()
  return 'sucess'

def buscar_contato_sql():
  Session = sessionmaker(bind=engine)
  session = Session()
  contatos = session.query(Contato).all()
  return contatos

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)

@app.route('/')
def home():
    contatos = buscar_contato_sql()
    for c in range(len(contatos)):
        contatos[c].tags = contatos[c].tags.split(',')
        contatos[c].links = contatos[c].links.split(',')

    return render_template(
        'home.html',
        titulo = 'Projeto 1',
        contatos = contatos
)       
@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/salvar_contato', methods=['POST'])
def salvar_contato():
    tags = request.form['tags'].split(',')

    tagsd = ''
    links = ''

    for tag in tags:
        if tagsd == '':
            tagsd = tag
        else:
            tagsd = tagsd + ',' + tag    
        if tag == 'Família':
            if links == '':
                links = familia
            else:
                links = links + ',' + familia
        elif tag == 'Outro':
            if links == '':
                links = outro
            else:
                links = links + ',' + outro
        elif tag == 'Amigo':
            if links == '':
                links = amigo
            else:
                links = links + ',' + amigo
        elif tag == 'Trabalho':
            if links == '':
                links = trabalho
            else:
                links = links + ',' + trabalho
        else:
            if links == '':
                links = ''
            else:
                links = links + ',' + ''

    print(tagsd)
    print(links)
    if request.form['tipo'] == 'novo': 
        cont = Contato(nome=request.form['nome'],
                email=request.form['email'],
                celular=request.form['celular'],
                tags=tagsd,
                links=links)               
        criar_contato_sql(cont)
    else:
        Session = sessionmaker(bind=engine)
        session = Session()
        contato_edit = session.query(Contato).filter_by(id=request.form['id']).first()
        contato_edit.nome = request.form['nome']
        contato_edit.email = request.form['email']
        contato_edit.celular = request.form['celular']
        contato_edit.tags = tagsd
        contato_edit.links = links
        session.commit()
    return redirect('/')
@app.route('/deletar_contato', methods=['POST'])
def deletar_contato():
    deletar_contato_sql(request.form['id'])
    return redirect('/')
app.run(host='0.0.0.0',debug=False,port=81)