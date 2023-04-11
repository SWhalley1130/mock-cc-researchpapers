#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/research')
def research():
    research=Research.query.all()
    um=[]
    for r in research:
        ugh={
            'id':r.id,
            'topic':r.topic,
            'year':r.year,
            'page_count':r.page_count,
        }
        um.append(ugh)
    res=make_response(jsonify(um), 200)
    return res

@app.route('/research/<int:id>', methods=['GET', 'DELETE'])
def research_by_id(id): 
    research=Research.query.filter(Research.id==id).first()
    if request.method=='GET':
        try: 
            res=make_response(jsonify(research.to_dict()),200)
            return res
        except Exception as e:
            return make_response({'errors':[e.__str__()]}, 404)
    elif request.method=='DELETE':
        research_papers=ResearchAuthors.query.filter(ResearchAuthors.research_id==id).all()
        for paper in research_papers:
            db.session.delete(paper)
        db.session.delete(research)
        db.session.commit()
        r=make_response({'message':"shit deleted"},200)
        return r

    # if research:
    #     res=make_response(jsonify(research.to_dict()),200)
    #     return res
    # else: 
    #     rb=make_response({'message':'Research not found'},404)
    #     return rb

    


@app.route('/authors')
def authors():
    research=Author.query.all()
    um=[]
    for r in research:
        ugh=r.to_dict()
        um.append(ugh)
    res=make_response(jsonify(um), 200)
    return res


@app.route('/research_author', methods=['GET','POST'])
def research_author():
    if request.method=='POST':
        data=request.get_json()
        try:
            new_ra=ResearchAuthors(
                author_id=data['author_id'], 
                research_id=data['research_id']
            )
            db.session.add(new_ra)
            db.session.commit()
            author=Author.query.filter(Author.id==new_ra.author_id).first().to_dict()
            return make_response(jsonify(author),202)
        except Exception as e:
            return make_response({'errors':[e.__str__()]}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
