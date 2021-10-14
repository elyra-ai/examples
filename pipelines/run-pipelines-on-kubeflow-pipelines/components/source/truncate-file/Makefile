.PHONY: container-image lint
.PHONY: publish-container-image publish-container-image-quay publish-container-image-dh

# Customize the variables as desired/required
CONTAINER_IMAGE_NAME=kfp-tutorial-truncate-file-component:v000
DH_ORG=elyra
QUAY_ORG=elyra

lint:
	pip install -r test-requirements.txt
	flake8 .

container-image: lint
	docker build -t $(CONTAINER_IMAGE_NAME) .

publish-container-image: publish-container-image-quay publish-container-image-dh
	# handled by dependencies

publish-container-image-quay: container-image ## Publish component container image on quay.io
	docker tag $(CONTAINER_IMAGE_NAME) quay.io/$(QUAY_ORG)/$(CONTAINER_IMAGE_NAME)
	docker push quay.io/$(QUAY_ORG)/$(CONTAINER_IMAGE_NAME)
	docker inspect --format="{{index .RepoDigests 0}}" quay.io/$(QUAY_ORG)/$(CONTAINER_IMAGE_NAME)

publish-container-image-dh: container-image ## Publish component container image on hub.docker.com
	docker tag $(CONTAINER_IMAGE_NAME) docker.io/$(DH_ORG)/$(CONTAINER_IMAGE_NAME)
	docker push docker.io/$(DH_ORG)/$(CONTAINER_IMAGE_NAME)
	docker inspect --format="{{index .RepoDigests 0}}" docker.io/$(DH_ORG)/$(CONTAINER_IMAGE_NAME)
