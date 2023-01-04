HOST = vacancies.cyrextech.net
PORT = 7823
PROTO_DIR = ./src/proto
PROTO_FILE_NAMES = auth_service.proto,rpc_create_vacancy.proto,rpc_signin_user.proto,rpc_signup_user.proto,rpc_update_vacancy.proto,user_service.proto,vacancy.proto

prepare:
	brew tap ktr0731/evans \
	brew install evans

evans-cli:
	evans --host ${HOST} --port ${PORT} --path ${PROTO_DIR} --proto ${PROTO_FILE_NAMES}