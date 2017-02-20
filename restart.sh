cd /home/www/fitaholEnv/fitahol/ && git pull
supervisorctl -c /etc/supervisord.d/supervisord.conf restart fitahol
supervisorctl -c /etc/supervisord.d/supervisord.conf restart fitahol_celery