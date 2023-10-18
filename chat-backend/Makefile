run-server:
	python3 manage.py runserver

run-server-docker:
	docker run -p 8080:80 -p 8888:8888 --rm -ti webis/chatnoir-chat:0.0.1

build-app:
	docker build -t webis/chatnoir-chat:0.0.1 -f docker/Dockerfile .

run-test:
	DJANGO_SETTINGS_MODULE=tests.settings_test python3 manage.py reset_db --no-input
	DJANGO_SETTINGS_MODULE=tests.settings_test python3 manage.py makemigrations chatnoir_chat
	DJANGO_SETTINGS_MODULE=tests.settings_test python3 manage.py migrate chatnoir_chat
	DJANGO_SETTINGS_MODULE=tests.settings_test python3 manage.py test

vite:
	docker run --rm -ti -v ${PWD}/../chatnoir_chat_ui:/chat-ui -v ${PWD}/chatnoir_chat/static/ui:/dist -w /chat-ui --entrypoint vite webis/tira:vuetify-dev-0.0.1 build
