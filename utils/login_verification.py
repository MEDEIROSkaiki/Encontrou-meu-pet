from functools import wraps
from flask import session, flash, redirect, url_for

def login_requerido(f):
    """
    Decorator que verifica se o usuário está logado na sessão.
    Se não estiver, redireciona para a página de login com uma mensagem flash.
    """
    @wraps(f) # Isso é importante para preservar metadados da função original para o Flask
    def funcao_decorada(*args, **kwargs):
        if not session.get('esta_logado'):
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('auth_bp.login')) 
        return f(*args, **kwargs)
    return funcao_decorada