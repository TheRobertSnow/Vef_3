import os
import sqlite3
import flask import Flask, request, session, g, reirect, url_for, abort, render_template, flash

app = Flask(__name__) #Býr til app dæmið
app.config.from_object(__name__) #loadar stillingar frá þessum file, flaskr.py

#loadar sjálfgefnar stillingar og skrifar yfir stillingar frá umhverfis breytu
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'flaskr.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
	'''Tengir við ákveðinn gagnagrunn'''
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	'''frumstillir gagnagrunnin'''
	init_db()
	print('Initialized the database.')

def get_db():
	'''opnar nýja gagnagrunns tengingu ef það er engin'''
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	'''Lokar gagnagrunns tengingu'''
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


