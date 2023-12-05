run-server:
	python3 chat-backend/manage.py runserver
setup:
	@cd chat-ui && yarn install
	pip3 install -r chat-backend/requirements.txt

vite:
	@rm -Rf /dist \
	&& rm -Rf chat-backend/chatnoir_chat/static/ui/ \
	&& cd chat-ui \
	&& /usr/local/lib/node_modules/.bin/vite build \
	&& mv /dist ../chat-backend/chatnoir_chat/static/ui