.DEFAULT_GOAL = help
CONTAINER_NAME = "mongo_db"
IMAGE_NAME = "mongo_db"

UNAME_M := $(shell uname -m)
ifneq ($(filter arm%,$(UNAME_M)),)
	BUILD_FLAGS = --platform linux/arm64
endif

help:
	@echo " "
	@echo "postgres_vector"
	@echo " "
	@echo "  make build        : Compilar a imagem docker"
	@echo "  make delete       : Remove container e imagem docker"
	@echo "  make run          : Executar a aplicação via docker"
	@echo " "

build:
	docker build . $(BUILD_FLAGS) -t ${IMAGE_NAME}

run:
	docker run --name ${CONTAINER_NAME} -i -d -p 27017:27017 ${IMAGE_NAME}

delete:
	-@docker stop ${CONTAINER_NAME}
	-@docker rm ${CONTAINER_NAME}
	-@docker rmi ${IMAGE_NAME}