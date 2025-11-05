from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory
from .models import Termo, Curso
import os

rotas_principal = Blueprint("principal", __name__)

# Página do glossário
@rotas_principal.route("/glossario")
def pagina_glossario():
    return render_template("glossario.html")

# Página inicial
@rotas_principal.route("/")
def pagina_inicial():
    return render_template("index.html")

# Página de acessibilidade
@rotas_principal.route("/acessibilidade")
def pagina_acessibilidade():
    return render_template("acessibilidade.html")

# Rota para servir vídeos diretamente
@rotas_principal.route('/videos/<path:filename>')
def video(filename):
    videos_dir = os.path.join(os.path.dirname(__file__), "static", "videos")
    return send_from_directory(videos_dir, filename, as_attachment=False)

# Página de visualização do termo (detalhe)
@rotas_principal.route('/vizualizacaoTermo/<int:termo_id>')
def visualizar_termo(termo_id):
    termo = Termo.query.get(termo_id)
    if not termo:
        flash("Termo não encontrado.", "warning")
        return redirect(url_for("principal.pagina_glossario"))
    termo_data = {
        "id": termo.id,
        "termo": termo.nome_termo,
        "descricao": termo.descricao,
        "video": termo.video,
        "curso_nome": termo.curso.nome if termo.curso else None
    }
    return render_template("vizualizacaoTermo.html", termo=termo_data)

# Redirecionamentos amigáveis para cursos
def _redirect_to_curso_like(pattern):
    curso = Curso.query.filter(Curso.nome.ilike(pattern)).first()
    if not curso:
        flash("Curso não encontrado.", "warning")
        return redirect(url_for("principal.pagina_glossario"))
    return redirect(url_for("principal.pagina_glossario") + f"?curso_id={curso.id}")

# Rotas amigáveis por curso
@rotas_principal.route('/cursos/psicologia')
def termos_psicologia():
    return _redirect_to_curso_like("%psicologia%")

@rotas_principal.route('/cursos/ciencia-da-computacao')
def termos_ciencia_da_computacao():
    return _redirect_to_curso_like("%ciencia%computacao%")

@rotas_principal.route('/cursos/direito')
def termos_direito():
    return _redirect_to_curso_like("%direito%")

# Opcional: rota genérica por id de curso
@rotas_principal.route('/cursos/<int:curso_id>')
def termos_por_curso_id(curso_id):
    curso = Curso.query.get(curso_id)
    if not curso:
        flash("Curso não encontrado.", "warning")
        return redirect(url_for("principal.pagina_glossario"))
    return redirect(url_for("principal.pagina_glossario") + f"?curso_id={curso.id}")