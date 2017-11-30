"""
Jinja过滤器
"""
from app import app


@app.template_filter()
def test(arg):
    pass