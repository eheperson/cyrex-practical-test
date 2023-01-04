HOST = vacancies.cyrextech.net
PORT = 7823
PROTO_DIR = ./src/proto
PROTO_FILE_NAMES = auth_service.proto,rpc_create_vacancy.proto,rpc_signin_user.proto,rpc_signup_user.proto,rpc_update_vacancy.proto,user_service.proto,vacancy.proto
SOURCE_DIR = ./src
VENV_DIR = ./venv

prepare:
	brew install protobuf \
	brew tap ktr0731/evans \
	brew install evans \
	python3 -m venv venv \
	source venv/bin/activate \
	pip install --upgrade pip \
	pip install -r requirements.txt \
	deactivate \

evans-cli:
	evans --host ${HOST} --port ${PORT} --path ${PROTO_DIR} --proto ${PROTO_FILE_NAMES}

generate_protos:
	protoc -I${PROTO_DIR} --python_out=${PROTO_DIR} ${PROTO_DIR}/*.proto

python_run:
	source ${VENV_DIR}/bin/activate && python ${SOURCE_DIR}/main.py && deactivate

clean_protos:
	rm ${PROTO_DIR}/*_pb2.py