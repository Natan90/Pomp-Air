#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


                                    ## à ajouter
from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="localhost",                 # à modifier
            user="nbouche",                     # à modifier
            password="mdp",                # à modifier
            database="BDD_sae",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# DROP TABLE IF EXISTS Achat, Pompe, Intervention, Modele, Client;
#
# CREATE TABLE Client(
#    id_client INT AUTO_INCREMENT,
#    nom_client VARCHAR(50),
#    prenom_client VARCHAR(50),
#    adresse VARCHAR(50),
#    telephone VARCHAR(50),
#    adresse_mail VARCHAR(50),
#    id_client_1 INT,
#    PRIMARY KEY(id_client),
#    FOREIGN KEY(id_client_1) REFERENCES Client(id_client)
# );
#
# CREATE TABLE Modele(
#    id_modele INT AUTO_INCREMENT,
#    nom_modele VARCHAR(50),
#    prix INT,
#    caracteristique VARCHAR(50),
#    PRIMARY KEY(id_modele)
# );
#
# CREATE TABLE Pompe(
#    numero_pompe INT AUTO_INCREMENT,
#    poids INT,
#    puissance INT,
#    id_modele INT NOT NULL,
#    PRIMARY KEY(numero_pompe),
#    FOREIGN KEY(id_modele) REFERENCES Modele(id_modele)
# );
#
# CREATE TABLE Intervention(
#    id_intervention INT AUTO_INCREMENT,
#    date_intervention DATE,
#    descriptif_intervention VARCHAR(50),
#    numero_pompe INT NOT NULL,
#    id_client INT NOT NULL,
#    PRIMARY KEY(id_intervention),
#    FOREIGN KEY(numero_pompe) REFERENCES Pompe(numero_pompe),
#    FOREIGN KEY(id_client) REFERENCES Client(id_client)
# );
#
# CREATE TABLE Achat(
#    id_achat INT AUTO_INCREMENT,
#    date_achat DATE,
#    date_installation VARCHAR(50),
#    id_client INT NOT NULL,
#    numero_pompe INT NOT NULL,
#    PRIMARY KEY(id_achat),
#    FOREIGN KEY(id_client) REFERENCES Client(id_client),
#    FOREIGN KEY(numero_pompe) REFERENCES Pompe(numero_pompe)
# );




@app.route('/')
def show_layout():
    return render_template('index.html')

@app.route('/pompe/show')
def show_pompe():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT numero_pompe, poids, puissance, prix, id_modele FROM Pompe")
    pompe = mycursor.fetchall()
    return render_template('pompe/show_pompe.html', pompe=pompe)

@app.route('/pompe/add', methods=['GET'])
def add_pompe():
    mycursor = get_db().cursor()
    sql=''' SELECT numero_pompe, poids, puissance, prix, id_modele AS idModele  FROM Pompe'''
    mycursor.execute(sql)
    pompe = mycursor.fetchall()
    mycursor = get_db().cursor()
    sql=''' SELECT id_modele AS idModele, nom_modele FROM Modele '''
    mycursor.execute(sql)
    id_modele = mycursor.fetchall()


    return render_template('pompe/add_pompe.html', id_modele=id_modele )

@app.route('/pompe/add', methods=['POST'])
def valid_add_pompe():
    mycursor = get_db().cursor()
    poids = request.form.get('poids', '')
    puissance = request.form.get('puissance', '')
    prix = request.form.get('prix', '')
    idModele = request.form.get('idModele', '')

    sql=''' INSERT INTO Pompe (poids, puissance, prix, id_modele ) VALUES (%s, %s, %s, %s)'''
    mycursor.execute(sql, (poids, puissance, prix, idModele,))
    get_db().commit()

    print(u'pompe ajoutée, poids :', poids, u'puissance :', puissance, u'idModele :', idModele)
    message = u'pompe ajoutée, poids : %s, puissance : %s, idModele : %s' % (poids, puissance, idModele)
    flash(message, 'alert-success')
    return redirect('/pompe/show')

@app.route('/pompe/delete', methods=['GET'])
def delete_pompe():


@app.route('/pompe/delete-cascade', methods=['GET'])
def delete_pompe_cascade():
    id = request.args.get('id', '')
    id=int(id)
    mycursor = get_db().cursor()
    sql=''' SELECT COUNT DISTINCT id_achat FROM Achat WHERE numero_pompe = %s'''
    mycursor.execute(sql)
    achats = mycursor.fetchone()
    return render_template('pompe/delete_pompe.html', achats=achats)

@app.route('/pompe/delete-cascade', methods=['POST'])
def valid_delete_pompe_cascade():
    id = request.form.get('id', '')
    id = int(id)
    mycursor = get_db().cursor()
    sql=''' DELETE FROM Pompe WHERE numero_pompe = %s'''
    mycursor.execute(sql, (id,))
    get_db().commit()
    message = u'pompe supprimée, id : %s' % id
    flash(message, 'alert-warning')
    return redirect('/pompe/show')

# @app.route('/pompe/delete-cascade', methods=['GET'])
# def delete_pompe_cascade():
#     id = request.args.get('id', '')
#     id=int(id)
#     mycursor = get_db().cursor()
#     sql=''' SELECT COUNT DISTINCT id_achat FROM Achat WHERE numero_pompe = %s'''
#     mycursor.execute(sql)
#     achats = mycursor.fetchone()
#     return render_template('pompe/delete_pompe_cascade.html', achats=achats)




@app.route('/pompe/edit', methods=['GET'])
def edit_jeu_plateau():
    id = request.args.get('id', '')
    id=int(id)
    mycursor = get_db().cursor()
    sql=''' SELECT numero_pompe AS id, puissance, poids, prix, id_modele FROM Pompe WHERE numero_pompe = %s'''
    mycursor.execute(sql, (id,))
    pompe = mycursor.fetchone()

    return render_template('/pompe/edit_pompe.html', pompe=pompe)

@app.route('/pompe/edit', methods=['POST'])
def valid_edit_jeu_plateau():
    id = request.form.get('id', '')
    puissance = request.form.get('puissance', '')
    poids = request.form.get('poids', '')
    prix = request.form.get('prix', '')
    mycursor = get_db().cursor()
    sql =''' UPDATE Pompe SET puissance = %s, poids = %s, prix = %s WHERE numero_pompe= %s'''
    mycursor.execute(sql, (puissance, poids, prix, id))
    get_db().commit()
    message = u'jeu modifié, id : %s, puissance : %s, poids : %s, prix : %s' % (id, puissance, poids, prix)
    print(message)
    flash(message, 'alert-success')
    return redirect('/pompe/show')





#Partie intervention ..............................................................................................................

@app.route('/intervention/show', methods=['GET'])
def show_interventions():
    mycursor = get_db().cursor()
    sql = "SELECT id_intervention, date_intervention, descriptif_intervention, numero_pompe, id_client FROM intervention"
    mycursor.execute(sql)
    interventions = mycursor.fetchall()
    return render_template('/intervention/show_intervention.html', intervention=interventions)

@app.route('/intervention/add' , methods=['GET'])
def add_intervention():
    mycursor = get_db().cursor()
    sql = "SELECT id_intervention, date_intervention, descriptif_intervention, numero_pompe, id_client FROM intervention"
    mycursor.execute(sql)
    intervention = mycursor.fetchall()
    return render_template('intervention/add_intervention.html', intervention=intervention)

@app.route('/intervention/add', methods=['POST'])
def valid_add_intervention():
    id = request.form.get('id_intervention')
    date = request.form.get('date_intervention','')
    descriptif = request.form.get('descriptif_intervention','')
    num_pompe = request.form.get('numero_pompe')
    if not date:
        date = None  # Remplacer une valeur vide par None
    if not descriptif:
        descriptif = None  # Remplacer une valeur vide par None

    id_client = request.form.get('id_client','')
    # message = 'Le titre du film modifié est "' + titre +' " , il est sortie en ' + date + ' le réalisateur est ' + realisateur + ' le genre du film est ' + genre + '. Le film dure ' + duree + 'minutes et il a comme affiche ' + affiche
    # print(message)
    mycursor = get_db().cursor()
    tuple_param = (id, date, descriptif, num_pompe, id_client)
    sql = "INSERT INTO intervention(id_intervention, date_intervention, de scriptif_intervention, numero_pompe, id_client) VALUES (%s, %s, %s, %s, %s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    flash(f"Le type d'intervention '{descriptif}' a été ajouté.", 'alert-success')
    return redirect('/intervention/show')

@app.route('/intervention/edit', methods=['GET'])
def edit_intervention():
    id = request.args.get('id_intervention','')
    mycursor = get_db().cursor()
    sql = "SELECT id_intervention, date_intervention, descriptif_intervention, numero_pompe, id_client FROM intervention WHERE id_intervention = %s"
    mycursor.execute(sql, (id,))
    intervention = mycursor.fetchall()
    mycursor.execute(sql)
    return render_template('intervention/edit_intervention.html', intervention=intervention)


@app.route('/intervention/edit', methods=['POST'])
def valid_edit_intervention():
    print('''ajout de l'intervention dans le tableau''')
    id = request.form.get('id_intervention', '')
    date = request.form.get('date_intervention', '')
    descriptif = request.form.get('descriptif_intervention', '')
    num_pompe = request.form.get('numero_pompe')
    id_client = request.form.get('id_client', '')
    # message = (
    #         'Le titre du film modifié est "' + titre +
    #         '", il est sorti en ' + date +
    #         ', le réalisateur est ' + realisateur +
    #         ', le genre du film est ' + genre +
    #         '. Le film dure ' + str(duree) +
    #         ' minutes et il a comme affiche ' + affiche
    # )
    # print(message)
    mycursor = get_db().cursor()
    tuple_param = (date, descriptif, num_pompe, id_client, id)
    sql = ("UPDATE intervention SET date = %s, descriptif = %s, num_pompe = %s, id_client = %s WHERE id_intervention = %s")

    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/intervention/show')