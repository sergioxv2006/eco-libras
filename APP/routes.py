import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session
from werkzeug.utils import secure_filename
from .models import Termo, Curso
from .extencoes import db
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


# Proteção de rota admin
def admin_logado():
    return session.get('admin_logado') is True

@rotas_principal.route("/admin", methods=["GET"])
def pagina_admin():
    if not admin_logado():
        flash("Faça login para acessar a área administrativa.", "warning")
        return redirect(url_for("principal.pagina_inicial"))
    cursos = Curso.query.order_by(Curso.nome).all()
    curso_id = request.args.get('curso_id', type=int)
    if curso_id:
        glossario = Termo.query.filter_by(curso_id=curso_id).order_by(Termo.id.desc()).all()
    else:
        glossario = Termo.query.order_by(Termo.id.desc()).all()
    return render_template("admin.html", glossario=glossario, cursos=cursos, curso_id=curso_id)

# Login admin via AJAX
@rotas_principal.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json() or request.form
    username = data.get("username")
    password = data.get("password")
    admin_user = os.environ.get("ADMIN_USER", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin")
    if username == admin_user and password == admin_password:
        session['admin_logado'] = True
        return jsonify({"success": True, "redirect": url_for("principal.pagina_admin")})
    return jsonify({"success": False, "message": "Usuário ou senha inválidos."}), 401

# Logout admin
@rotas_principal.route("/admin/logout")
def admin_logout():
    session.pop('admin_logado', None)
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("principal.pagina_inicial"))

# Adicionar novo termo
@rotas_principal.route("/admin/adicionar", methods=["POST"])
def adicionar_termo():
    termo = request.form.get("termo")
    descricao = request.form.get("descricao")
    curso_id = request.form.get("curso_id", type=int)
    video_file = request.files.get("video")
    video_filename = None
    if video_file and video_file.filename:
        video_filename = secure_filename(video_file.filename)
        pasta_videos = os.path.join("APP", "static", "videos")
        os.makedirs(pasta_videos, exist_ok=True)
        video_file.save(os.path.join(pasta_videos, video_filename))
    novo_termo = Termo(
        nome_termo=termo,
        curso_id=curso_id,
        descricao=descricao,
        video=video_filename or ""
    )
    db.session.add(novo_termo)
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
        return jsonify({'success': True, 'message': 'Termo adicionado com sucesso!'})
    flash("Termo adicionado com sucesso!", "success")
    return redirect(url_for("principal.pagina_admin"))

# Adicionar novo curso
@rotas_principal.route("/admin/adicionar_curso", methods=["POST"])
def adicionar_curso():
    nome_curso = request.form.get("curso")
    if not nome_curso:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
            return jsonify({'success': False, 'message': 'Nome do curso é obrigatório!'}), 400
        flash("Nome do curso é obrigatório!", "danger")
        return redirect(url_for("principal.pagina_admin"))
    curso_existente = Curso.query.filter_by(nome=nome_curso).first()
    if curso_existente:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
            return jsonify({'success': False, 'message': 'Já existe um curso com esse nome!'}), 400
        flash("Já existe um curso com esse nome!", "warning")
        return redirect(url_for("principal.pagina_admin"))
    novo_curso = Curso(nome=nome_curso)
    db.session.add(novo_curso)
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
        return jsonify({'success': True, 'message': 'Curso adicionado com sucesso!'})
    flash("Curso adicionado com sucesso!", "success")
    return redirect(url_for("principal.pagina_admin"))

# Editar termo
@rotas_principal.route("/admin/editar", methods=["POST"])
def editar_termo():
    termo_id = request.form.get("id")
    novo_nome = request.form.get("termo")
    novo_curso_id = request.form.get("curso_id", type=int)
    nova_descricao = request.form.get("descricao")
    video_file = request.files.get("video")
    termo = Termo.query.get(termo_id)
    if termo:
        termo.nome_termo = novo_nome
        termo.curso_id = novo_curso_id
        termo.descricao = nova_descricao
        if video_file and video_file.filename:
            # Remove vídeo antigo
            if termo.video:
                caminho_antigo = os.path.join("APP", "static", "videos", termo.video)
                if os.path.exists(caminho_antigo):
                    try:
                        os.remove(caminho_antigo)
                    except Exception:
                        pass
            # Salva novo vídeo
            video_filename = secure_filename(video_file.filename)
            pasta_videos = os.path.join("APP", "static", "videos")
            os.makedirs(pasta_videos, exist_ok=True)
            video_file.save(os.path.join(pasta_videos, video_filename))
            termo.video = video_filename
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
            return jsonify({'success': True, 'message': 'Termo editado com sucesso!'})
        flash(f"Termo '{novo_nome}' editado com sucesso!", "success")
    return redirect(url_for("principal.pagina_admin", editar_id=termo_id))

# Remover termo
@rotas_principal.route("/admin/remover", methods=["POST"])
def remover_termo():
    termo_id = request.form.get("id")
    termo = Termo.query.get(termo_id)
    if termo:
        db.session.delete(termo)
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
            return jsonify({'success': True, 'message': 'Termo removido com sucesso!'})
        flash("Termo removido com sucesso!", "success")
    return redirect(url_for("principal.pagina_admin"))

# Remover curso
@rotas_principal.route("/admin/remover_curso", methods=["POST"])
def remover_curso():
    curso_id = request.form.get("id", type=int)
    curso = Curso.query.get(curso_id)
    if not curso:
        return jsonify({'success': False, 'message': 'Curso não encontrado!'}), 404
    termos_vinculados = Termo.query.filter_by(curso_id=curso_id).count()
    db.session.delete(curso)
    db.session.commit()
    if termos_vinculados > 0:
        return jsonify({'success': True, 'message': f'Curso e {termos_vinculados} termo(s) vinculados removidos com sucesso!'}), 200
    return jsonify({'success': True, 'message': 'Curso removido com sucesso!'}), 200

# AJAX: buscar termos
@rotas_principal.route("/admin/buscar", methods=["GET"])
def buscar_termos():
    termo = request.args.get("termo", "").strip().lower()
    curso_id = request.args.get("curso_id", None)
    query = Termo.query
    if termo:
        query = query.filter(Termo.nome_termo.ilike(f"%{termo}%"))
    # Se curso_id não for informado, vazio, null, undefined ou zero (string ou int), retorna todos os termos
    if curso_id not in [None, '', 'null', 'undefined', 0, '0', False]:
        try:
            curso_id_int = int(curso_id)
            if curso_id_int != 0:
                query = query.filter(Termo.curso_id == curso_id_int)
        except Exception:
            pass
    resultados = query.order_by(Termo.id.desc()).all()
    termos_json = [
        {
            "id": t.id,
            "termo": t.nome_termo,
            "descricao": t.descricao,
            "video": t.video,
            "curso_id": t.curso_id
        } for t in resultados
    ]
    return jsonify(termos_json)

@rotas_principal.route("/admin/buscar_cursos", methods=["GET"])
def buscar_cursos():
    termo = request.args.get("termo", "").strip().lower()
    if termo:
        resultados = Curso.query.filter(Curso.nome.ilike(f"%{termo}%")).order_by(Curso.nome).all()
    else:
        resultados = Curso.query.order_by(Curso.nome).all()
    cursos_json = [
        {
            "id": c.id,
            "nome": c.nome
        } for c in resultados
    ]
    return jsonify(cursos_json)

# Rota para servir vídeos diretamente (caso queira usar url_for('principal.video', filename=...))
@rotas_principal.route('/videos/<filename>')
def video(filename):
     pasta_videos = os.path.join('APP', 'static', 'videos')
     return send_from_directory(pasta_videos, filename)

