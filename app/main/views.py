from flask import (render_template, redirect, url_for, current_app,
                   abort, flash, request, make_response)

from . import main
from .forms import *
from ..models import *

from ..crawler import crawler

def find_project(project_name):
    _find_project = Project.objects(project_name = project_name).first()
    if _find_project is None:
        return False
    else:
        return True

def delete_project(project_name):
    Project(project_name = project_name).delete()   
    ProjectFork(project_name = project_name).delete()
    ChangedFile(project_name = project_name).delete()
            
@main.route('/', methods=['GET', 'POST'])
def index():
    """ INFOX Homepage
    """
    form = SearchProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        if not find_project(_input_project_name):
            flash('The Project (%s) is not be added. You can turn to Add to add it!' % _input_project_name)
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.project_overview', project_name=_input_project_name))

    page = request.args.get('page', 1, type=int) # default is 1st page
    pagination = Project.objects.paginate(page=page, per_page=current_app.config['SHOW_NUMBER_FOR_PAGE'])
    projects = pagination.items
    return render_template('index.html', form=form, projects=projects, pagination=pagination)

@main.route('/project/<project_name>', methods=['GET', 'POST'])
def project_overview(project_name): # add filter
    """ Overview of the project
    :param project_name
    """
    if not find_project(project_name):
        abort(404)

    refresh = RefreshProjectForm()
    if refresh.validate_on_submit():
        crawler.start(project_name)
        return redirect(url_for('main.project_overview', project_name=project_name))

    if project_name in crawler.current_crawling:
        flash('The Project (%s) is updating!' % project_name)
        refresh = None

    _project = Project.objects(project_name = project_name).first()
    _forks = ProjectFork.objects(project_name = project_name, file_list__ne = []).order_by('-last_committed_time')
    #page = request.args.get('page', 1, type=int) # default is 1st page
    #pagination = _forks.paginate(page=page, per_page=10)
    #forks = pagination.items
    return render_template('project_overview.html', project=_project, forks=_forks, refresh=refresh)

@main.route('/add', methods=['GET', 'POST'])
def add():
    """ Add Project
    """
    form = AddProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        _input_project_name = _input_project_name.replace('/','_')
        if not find_project(_input_project_name):
            crawler.start(_input_project_name)
            flash('The Project (%s) is added. The data is loading......' % _input_project_name)
            return redirect(url_for('main.index'))
        else:
            flash('The Project (%s) has already added!' % _input_project_name)
            return redirect(url_for('main.add'))
    return render_template('add.html', form=form)

@main.route('/localadd', methods=['GET', 'POST'])
def localadd():
    form = AddProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        analyser.analyse_project(_input_project_name, False)
        return redirect(url_for('main.project_overview', project_name=_input_project_name))
    return render_template('localadd.html', form=form)

@main.route('/delete', methods=['GET', 'POST'])
def delete():
    """ Delete Project
    """
    form = DeleteProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        if find_project(_input_project_name):
            delete_project(_input_project_name)
            flash('The project (%s) is already deleted!' % _input_project_name)
            return redirect(url_for('main.index'))
        else:
            flash('The project (%s) is not found.' % _input_project_name)
            return redirect(url_for('main.delete'))
    return render_template('delete.html', form=form)

@main.route('/about')
def about():
    """About Page
    """
    return render_template('about.html')
