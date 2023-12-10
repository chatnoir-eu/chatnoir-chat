FROM webis/chatnoir-chat:0.0.3-dev

ADD chatnoir_chat /chatnoir_chat/chatnoir_chat
ADD manage.py /chatnoir_chat/manage.py
ADD management /chatnoir_chat/management
ADD tests /chatnoir_chat/tests
ADD chatnoir_chat/uwsgi.ini /chatnoir_chat/uwsgi.ini

ADD chatnoir_chat/static/ui/ /var/www/static

RUN cd /chatnoir_chat/ \
	&& DJANGO_SETTINGS_MODULE=tests.settings_test python3 manage.py reset_db --no-input \
	&& DJANGO_SETTINGS_MODULE=tests.settings_test python3 manage.py makemigrations chatnoir_chat \
	&& DJANGO_SETTINGS_MODULE=tests.settings_test python3 manage.py migrate chatnoir_chat \
	&& DJANGO_SETTINGS_MODULE=tests.settings_test python3 manage.py test \
	&& chown -R www-data:www-data /var/www/static \
	&& chown -R www-data:www-data /chatnoir_chat \
	&& rm -r tests

CMD sh -c "nginx && uwsgi --uid 33 --gid 33 --ini /chatnoir_chat/uwsgi.ini"

