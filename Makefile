build-dev-env:
	docker image build \
		-f $(PWD)/Dockerfiles/Dockerfile-dev \
		-t phase-diagram-utils:0.1 $(PWD)

run-dev-env:
	docker container run \
		--rm \
		--volume="$(PWD):/usr/share/app" \
		--label="phase-diagram-utils" \
		-it \
		phase-diagram-utils:0.1 \
		bash
