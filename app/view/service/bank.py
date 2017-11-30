from flask import Blueprint, request, render_template, redirect, url_for

bank_service = Blueprint('bank_service', __name__)


@bank_service.route('/')
def index():
    return 'bank service'


@bank_service.route('/history')
def history():
    pass


@bank_service.route('/transfer')
def transfer():
    pass
