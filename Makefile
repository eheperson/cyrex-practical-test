HOST = vacancies.cyrextech.net
PORT = 7823
PROTO_DIR = src/rpcagent/proto
PROTO_FILE_NAMES = auth_service.proto,rpc_create_vacancy.proto,rpc_signin_user.proto,rpc_signup_user.proto,rpc_update_vacancy.proto,user_service.proto,vacancy.proto,vacancy_service.proto
SOURCE_DIR = src
VENV_DIR = venv

prepare:
	brew install protobuf && \
	brew tap ktr0731/evans && \
	brew install evans && \
	python -m venv venv && \
	source venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r ${SOURCE_DIR}/requirements.txt && \
	deactivate \

evans-help:
	@echo "help ------------------------------> evans"
	@echo ""
	@echo "connect ---------------------------> evans --host <host> --port <port_no> --path <proto_dir> --proto <proto_files>"
	@echo ""
	@echo "set headers for each request ------> header <header_name>=<header_value>"
	@echo "show headers ----------------------> show header"
	@echo ""
	@echo "show summary of packages ----------> show package"
	@echo "specify package -------------------> package <PackageName>"
	@echo ""
	@echo "show summary of services ----------> show service"
	@echo "specify service -------------------> package <ServiceName>"
	@echo ""
	@echo "show summary of messages ----------> show message"
	@echo "show description of the message ---> desc <MessageName>"
	@echo ""
	@echo "call rpc --------------------------> call <RpcName>"


evans-connect:
	evans --host ${HOST} --port ${PORT} --path ${PROTO_DIR} --proto ${PROTO_FILE_NAMES}
	
generate_protos:
	protoc -I${PROTO_DIR} --python_out=${PROTO_DIR}  ${PROTO_DIR}/*.proto

generate_protos_python:
	source ${VENV_DIR}/bin/activate && python -m grpc_tools.protoc --proto_path=${PROTO_DIR} --python_out=${PROTO_DIR} --grpc_python_out=${PROTO_DIR} ${PROTO_DIR}/*.proto && deactivate

clean_protos:
	rm ${PROTO_DIR}/*_pb2.py

locust_run:
	source ${VENV_DIR}/bin/activate && locust -f ${SOURCE_DIR}/main.py --config ${SOURCE_DIR}/locust.docker.conf

start-docker:
	sudo chmod +x ${SOURCE_DIR}/entrypoint.sh && \
	docker-compose up -d --build; docker logs --follow worker