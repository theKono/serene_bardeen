#!/usr/bin/env python

# standard library imports
import os.path
import time

# third party realted imports
from fabric.api import cd, env, local, run, sudo
from fabric.operations import put

# local library imports


CURR_TIME = int(time.time())
SERVER_ROOT = '/home/ubuntu/serene_bardeen'
SERVER_RELEASE_DIR = os.path.join(SERVER_ROOT, 'releases')
SERVER_NEW_RELEASE_DIR = os.path.join(SERVER_ROOT, 'releases', str(CURR_TIME))
SERVER_CURRENT_RELEASE_DIR = os.path.join(SERVER_ROOT, 'current')

VIRTUALENV_ROOT = '/home/ubuntu/.virtualenvs/serene_bardeen'
VIRTUALENV_PYTHON_EXECUTABLE = VIRTUALENV_ROOT + '/bin/python'
VIRTUALENV_PIP_EXECUTABLE = VIRTUALENV_ROOT + '/bin/pip'
VIRTUALENV_FAB_EXECUTABLE = VIRTUALENV_ROOT + '/bin/fab'

env.user = 'ubuntu'
env.key_filename = '/home/yuliang/.ssh/serene_bardeen.pem'


def production():

    env.hosts = ['serene.thekono.com']
    env.config_file = 'serene_bardeen/config_production.py'


def deploy_server():

    upload_server_code()
    install_server_code()
    restart_gunicorn_gracefully()


def upload_server_code():

    archive_file = 'latest.tar.gz'
    local('git archive --format=tar.gz -o %s HEAD' % archive_file)

    remote_dir = 'serene_bardeen_%s' % CURR_TIME
    remote_path = os.path.join(remote_dir, archive_file)
    run('mkdir -p %s' % remote_dir)
    put(archive_file, remote_path)
    with cd(remote_dir):
        run('tar -xf %s' % archive_file)
        run('rm %s' % archive_file)
        put(env.config_file, 'serene_bardeen/config.py')

    sudo('mkdir -p %s' % SERVER_RELEASE_DIR)
    sudo('mv %s %s' % (remote_dir, SERVER_NEW_RELEASE_DIR))
    sudo('rm -f %s' % SERVER_CURRENT_RELEASE_DIR)
    sudo('ln -sf %s %s' % (SERVER_NEW_RELEASE_DIR, SERVER_CURRENT_RELEASE_DIR))

    local('rm %s' % archive_file)


def install_server_code():

    with cd(SERVER_CURRENT_RELEASE_DIR):
        sudo('%s install -r requirements.txt' % VIRTUALENV_PIP_EXECUTABLE)


def restart_gunicorn_gracefully():

    sudo('kill -HUP `cat /var/run/gunicorn.pid`')
