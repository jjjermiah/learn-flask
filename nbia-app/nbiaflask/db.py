import sqlite3

import click

from flask import current_app, g

from nbiatoolkit import NBIAClient

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    
    client = NBIAClient()
    
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    # collections_df = client.getCollections(return_type = "dataframe")
    # collections_df is a pandas dataframe with one column called "Collection"
    
    # schema for collections table:
    # CREATE TABLE collections (
        # name TEXT UNIQUE NOT NULL
    # );
    
    # save the dataframe to the database
    

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)