from flask import Blueprint

from controllers.DashboardController import dashboard_view, explore_view, library_view, highlight_view, bookmarked_view, finished_view, search_view

dashboard_bp = Blueprint('dashboard_bp', __name__)

dashboard_bp.route('/', methods=['GET'])(dashboard_view)
dashboard_bp.route('/explore', methods=['GET'])(explore_view)
dashboard_bp.route('/library', methods=['GET'])(library_view)
dashboard_bp.route('/library/bookmark/', methods=['GET'])(bookmarked_view)
dashboard_bp.route('/library/bookmark/<int:page>', methods=['GET'])(bookmarked_view)
dashboard_bp.route('/library/finished', methods=['GET'])(finished_view)
dashboard_bp.route('/highlight', methods=['GET'])(highlight_view)
dashboard_bp.route('/search', methods=['GET'])(search_view)