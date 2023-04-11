from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class Research(db.Model, SerializerMixin):
    __tablename__="research"

    serialize_rules=('-research_authors.research_backref','-created_at', '-updated_at', )

    id=db.Column(db.Integer, primary_key=True)
    topic=db.Column(db.String)
    year=db.Column(db.Integer)
    page_count=db.Column(db.Integer)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


    research_authors=db.relationship('ResearchAuthors', backref='research_backref')

    @validates('year')
    def validate_year(self, key, value):
        if len(str(value))==4:
            return value
        else:
            raise Exception("Value must be integer with 4 digits.")


class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__="research_authors"

    serialize_rules=('-research_backref', '-author_backref',)
    id=db.Column(db.Integer, primary_key=True)
    author_id=db.Column(db.Integer, db.ForeignKey('authors.id'))
    research_id=db.Column(db.Integer, db.ForeignKey('research.id'))
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class Author(db.Model, SerializerMixin):
    __tablename__="authors"

    serialize_rules=('-research_authors.author_backref', '-created_at', '-updated_at',)
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    field_of_study=db.Column(db.String)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    research_authors=db.relationship('ResearchAuthors', backref='author_backref')

    @validates('field_of_study')
    def validate_field_of_study(self, key, value):
        list=['AI',"Robotics", "Machine Learning", "Vision", "Cybersecurity"]
        if value not in list: 
            raise Exception("Value must be in list.")
        else:
            return value