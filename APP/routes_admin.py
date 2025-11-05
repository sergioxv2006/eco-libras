import os
from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from .models import Termo, Curso
from .extencoes import db
from .auth_utils import token_required

rotas_admin = Blueprint("admin", __name__, url_prefix="/admin")

@rotas_admin.route("/")
@token_required
def pagina_admin():
    cursos = Curso.query.order_by(Curso.nome).all()
    curso_id = request.args.get('curso_id', type=int)
    
    if curso_id:
        glossario = Termo.query.filter_by(curso_id=curso_id).order_by(Termo.id.desc()).all()
    else:
        glossario = Termo.query.order_by(Termo.id.desc()).all()
        
    return render_template("admin.html", glossario=glossario, cursos=cursos, curso_id=curso_id)

@rotas_admin.route("/logout")
def admin_logout():
    flash("Logout: descarte o token no cliente.", "success")
    return redirect(url_for("principal.pagina_inicial"))

@rotas_admin.route("/adicionar", methods=["POST"])
@token_required
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
    return redirect(url_for("admin.pagina_admin"))

@rotas_admin.route("/adicionar_curso", methods=["POST"])
@token_required
def adicionar_curso():
    nome_curso = request.form.get("curso")
    if not nome_curso:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
            return jsonify({'success': False, 'message': 'Nome do curso é obrigatório!'}), 400
        flash("Nome do curso é obrigatório!", "danger")
        return redirect(url_for("admin.pagina_admin"))
    curso_existente = Curso.query.filter_by(nome=nome_curso).first()
    if curso_existente:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
            return jsonify({'success': False, 'message': 'Já existe um curso com esse nome!'}), 400
        flash("Já existe um curso com esse nome!", "warning")
        return redirect(url_for("admin.pagina_admin"))
    novo_curso = Curso(nome=nome_curso)
    db.session.add(novo_curso)
    db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
        return jsonify({'success': True, 'message': 'Curso adicionado com sucesso!'})
    flash("Curso adicionado com sucesso!", "success")
    return redirect(url_for("admin.pagina_admin"))

@rotas_admin.route("/editar", methods=["POST"])
@token_required
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
            if termo.video:
                caminho_antigo = os.path.join("APP", "static", "videos", termo.video)
                if os.path.exists(caminho_antigo):
                    try:
                        os.remove(caminho_antigo)
                    except Exception:
                        pass
            video_filename = secure_filename(video_file.filename)
            pasta_videos = os.path.join("APP", "static", "videos")
            os.makedirs(pasta_videos, exist_ok=True)
            video_file.save(os.path.join(pasta_videos, video_filename))
            termo.video = video_filename
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
            return jsonify({'success': True, 'message': 'Termo editado com sucesso!'})
        flash(f"Termo '{novo_nome}' editado com sucesso!", "success")
    return redirect(url_for("admin.pagina_admin", editar_id=termo_id))

@rotas_admin.route("/remover", methods=["POST"])
@token_required
def remover_termo():
    termo_id = request.form.get("id")
    termo = Termo.query.get(termo_id)
    if termo:
        db.session.delete(termo)
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json']:
            return jsonify({'success': True, 'message': 'Termo removido com sucesso!'})
        flash("Termo removido com sucesso!", "success")
    return redirect(url_for("admin.pagina_admin"))

@rotas_admin.route("/remover_curso", methods=["POST"])
@token_required
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

@rotas_admin.route("/buscar", methods=["GET"])
@token_required
def buscar_termos():
    termo = request.args.get("termo", "").strip().lower()
    curso_id = request.args.get("curso_id", None)
    query = Termo.query
    if termo:
        query = query.filter(Termo.nome_termo.ilike(f"%{termo}%"))
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

@rotas_admin.route("/buscar_cursos", methods=["GET"])
@token_required
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