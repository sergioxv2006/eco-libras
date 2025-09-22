from .extencoes import db

class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    termos = db.relationship('Termo', back_populates='curso', cascade='all, delete-orphan')

class Termo(db.Model):
    __tablename__ = 'termo'
    id = db.Column(db.Integer, primary_key=True)
    nome_termo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    video = db.Column(db.String(255))
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=True)
    curso = db.relationship('Curso', back_populates='termos')
