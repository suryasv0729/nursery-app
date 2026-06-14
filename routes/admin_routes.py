from flask import Blueprint, request, jsonify
from controllers.auth_controller import authorize
from controllers.admin_controller import get_dashboard_stats, get_all_users, get_all_orders

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@authorize(role_required='admin')
def stats(current_user_id, current_user_role):
    return get_dashboard_stats()

@admin_bp.route('/users', methods=['GET'])
@authorize(role_required='admin')
def users_list(current_user_id, current_user_role):
    return get_all_users()

@admin_bp.route('/orders', methods=['GET'])
@authorize(role_required='admin')
def orders_list(current_user_id, current_user_role):
    return get_all_orders()
