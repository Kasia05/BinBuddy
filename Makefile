###################
# Deploy Locally
##################

build_container_local:
	docker build --tag=$$IMAGE:dev

run_container_local:
	docker run -it -e PORT=8000 -p 8000:8000 $$IMAGE:dev

#####################
# Deploy on Cloud
####################

# Step 1
allow_docker_push:
	gcloud auth configure-docker $$GCP_REGION-docker.pkg.dev

# Step 2
create_artifact_repo:
	gcloud artifacts repositories create $$ARTIFACTREPO --repository-format=docker --location=$$GCP_REGION

# Step 3
build_image_prod:
	docker build -t $$GCP_REGION-docker.pkg.dev/$$GCP_PROJECT/$$ARTIFACTREPO/$$IMAGE:prod .


### Step 3
build_image_prod_m1:
	docker build --platform linux/amd64 -t $$GCP_REGION-docker.pkg.dev/$$GCP_PROJECT/$$ARTIFACTREPO/$$IMAGE:prod .

# Step 4
push_image_to_production:

	docker push $$GCP_REGION-docker.pkg.dev/$$GCP_PROJECT/$$ARTIFACTREPO/$$IMAGE:prod

# Step 5
deploy_to_cloud_run:

	gcloud run deploy --image $$GCP_REGION-docker.pkg.dev/$$GCP_PROJECT/$$ARTIFACTREPO/$$IMAGE:prod --memory $$MEMORY --region $$GCP_REGION
