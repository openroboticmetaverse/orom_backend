import docker
from rest_framework import status
from rest_framework.response import Response

client = docker.from_env()


def build_mujoco_image(image_name, dockerfile_path, dockefile_name):
    """
    Builds the docker image if does not exist
    Make sure to delete intermediate images (tag and name=none) after building
    """
    try:
        # Check if image already exists
        client.images.get(image_name)
        print(f"Image '{image_name}' already exists.")

    except docker.errors.ImageNotFound:
        # If image not found, build it from the Dockerfile
        try:
            print(f"Image '{image_name}' not found. Building the image...")
            client.images.build(
                                    path=dockerfile_path, 
                                    tag=image_name,
                                    dockerfile=dockefile_name,
                                    nocache=True,
                                    rm=True,
                                    forcerm=True
                                    #labels = {} -> use labels to set scene-id??
                                )
            print(f"Image '{image_name}' built successfully.")

        except Exception as build_error:
            print(f"Build failed: {str(build_error)}")
            
            # Try to clean up by removing any partially built image
            try:
                image = client.images.get(image_name)
                print(f"Cleaning up: removing partially built image '{image_name}'...")
                client.images.remove(image=image.id, force=True)
                print(f"Image '{image_name}' removed successfully.")
            except docker.errors.ImageNotFound:
                print(f"No partial image '{image_name}' to clean up.")
            except Exception as cleanup_error:
                print(f"Failed to clean up image '{image_name}': {str(cleanup_error)}")
    

    except Exception as ex:
        print(str(ex))



def run_mujoco_container(image_name, user_id, scene_id):
    # TODO: build image and push it to git so we can pull the prebuild image instead of building it from zero every time
    #* Possible to limit resources: mem_limit="2g" (limit 2GM RAM), nano_cpus=1e9 (1 CPU core)
    try:
        container = client.containers.run(
            image_name,
            name=f"{image_name}_{user_id}_{scene_id}",
            detach=True,
            auto_remove=True,       # container is removed automatically after it stops
            #ports={'<container_port>': '<host_port>'},  # Port mappings if needed
            #volumes={'/host_path/': {'bind': '/container_path/', 'mode': 'rw'}},  # If volume mappings are needed
            #environment=["ENV_VAR=value"],  # Pass environment variables if necessary
        )
        return container

    except Exception as ex:
        print(str(ex))
        # Handle errors (e.g., container creation failure)
        return False