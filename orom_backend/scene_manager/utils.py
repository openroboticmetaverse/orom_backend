import docker
import os
import time
from rest_framework import status
from rest_framework.response import Response

client = docker.from_env()

def pull_image(image_link,image_name):
    """
    Pull a Docker image from the registry.
    """
    try:
        print(f"Attempting to pull image: {image_link}")
        image = client.images.pull(image_link).tag(image_name)
        print(f"Successfully pulled image: {image}")
        return image
    except docker.errors.ImageNotFound:
        print(f"Image not found: {image_link}")
        raise
    except docker.errors.APIError as e:
        print(f"Error while pulling image: {e}")
        raise


def build_mujoco_image(image_name, dockerfile_path, dockerfile_name):
    """
    Builds the docker image for the mujoco simulation (if does not exist)
    """
    try:
        # Check if image already exists
        client.images.get(image_name)
        print(f"Image '{image_name}' already exists.")

    except docker.errors.ImageNotFound:
        # If image not found, build it from the Dockerfile
        try:
            print(f"Image '{image_name}' not found. Building the image...")
            image, build_logs = client.images.build(
                                    path=dockerfile_path, 
                                    tag=image_name,
                                    dockerfile=dockerfile_name,
                                    nocache=True,
                                    rm=True,
                                    forcerm=True,
                                    quiet=True
                                )

            print(f"\nImage '{image_name}' built successfully.")

        except Exception as build_error:
            print(f"Build failed: {str(build_error)}")
            # Print build logs for debugging
            for log in build_logs:
                if 'stream' in log:
                    for line in log['stream'].splitlines():
                        print(str(line))
            
            # When building fails: try to clean up by removing any partially built image
            try:
                image = client.images.get(image_name)
                print(f"Cleaning up: removing partially built image '{image_name}'...")
                client.images.remove(image=image.id, force=True)
                print(f"Image '{image_name}' removed successfully.")

            except Exception as ex:
                print(f"Error while cleaning up failed build: {str(ex)}")

            # Delete intermediate images (name=none)
            try: 
                for image in client.images.list():
                    print(f"{image.id}-{image.tags}")
                    if "<none>" in image.tags:
                        image_id = image.id
                        print(f"Deleting image with ID: {image_id}")
                        client.images.remove(image=image_id, force=True)

            except Exception as ex:
                print(f"An unexpected error occurred: {str(ex)}")


            return Response({"message": f"Build failed: {str(build_error)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
    
    except Exception as ex:
        print(str(ex))
        return Response({"message": str(ex)}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )



def monitor_container(container):
    """
    Monitor the container state
    # TODO: Test and improve functionality
    """
    client = docker.from_env()
    try:
        # Check container status
        container_obj = client.containers.get(container.id)
        for line in container_obj.logs(stream=True):
            print(f"Sim-Container log: {line.decode().strip()}")
        
        # Check if container stopped
        container_obj.wait()
        print(f"Container {container.name} finished.")

    except Exception as ex:
        print(f"Error monitoring container {container.name}: {str(ex)}")



def run_mujoco_simulation_in_background(image_name, container_port, host_port, user_id, scene_id, error_queue):
    """
    Function to run the mujoco simualation docker container in a separate thread
    """
    try:
        # Run container
        container = run_mujoco_container(image_name, container_port, host_port, user_id, scene_id, error_queue)
        
        # Monitor the container's status in the background
        monitor_container(container)
        
    except Exception as ex:
        resp = Response({"message": f"Error running container: {str(ex)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
        error_queue.put(resp)



def run_mujoco_container(image_name, container_port, host_port, user_id, scene_id, error_queue):
    """
    Run mujoco container based on previously build image. The required files to run the simulation
    are mounted from the local machine (required setting environment variable - see README).
    On startup the simulation automatically starts.

    For debugging of the container set command='sleep infinity'
    """
    # TODO: build image and push it to git so we can pull the prebuild image instead of building it from zero every time
    # TODO: check if container is already running
    #* Possible to limit resources: mem_limit="2g" (limit 2GM RAM), nano_cpus=1e9 (1 CPU core)

    host_sim_folder_path = os.getenv("OROM_BACKEND_PATH")
    target_sim_folder_path = '/sim_ws/simulation_mujoco'

    # Create mount for required simulation files
    mount = docker.types.Mount(
        target=target_sim_folder_path,      # Path inside the inner container
        source= f"{host_sim_folder_path}/simulation_mujoco", # Path on local machine where docker daemon is running
        type='bind',
        read_only=True
    )
    
    try:
        container = client.containers.run(
            image_name,
            name=f"{image_name}_{user_id}_{scene_id}",      # container name
            mounts=[mount],
            network="orom_backend_default",
            command=f"python -u {target_sim_folder_path}/mujoco_simulation.py",
            #command="sleep infinity",   # debugging container
            detach=True,
            stdout=True,
            stderr=True,
            auto_remove=True,       # container is removed automatically after it stops
            environment={           # environment variables
                        "USER_ID":user_id, 
                        "SCENE_ID":scene_id,
                        "CONTAINER_PORT":container_port,
                        "OROM_BACKEND_URL":os.getenv("OROM_BACKEND_URL"),
                        },
            ports={str(container_port):str(host_port)},  # Port mappings between frontend and simulation
        )
        return container

    except Exception as ex:
        resp = Response({"message": f"Error running container: {str(ex)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
        error_queue.put(resp)
        return None



def stop_and_remove_container(image_name, user_id, scene_id, error_queue):
    """
    Stop a running docker container.
    Due to the auto_remove paramater the container is automatically removed after it stops
    """
    try:
        container_name = f"{image_name}_{user_id}_{scene_id}"
        # Get the container by name
        container = client.containers.get(container_name)
        
        print(f"Stopping container: {container_name}")
        # Stop container
        container.stop()
        
        print(f"Container '{container_name}' stopped and removed successfully.")
    
    except docker.errors.NotFound:
        resp = Response({"message": f"Container '{container_name}' not found."}, 
                            status=status.HTTP_404_NOT_FOUND
                        )
        error_queue.put(resp)
    
    except Exception as ex:
        resp = Response({"message": str(ex)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
        error_queue.put(resp)

def pull_or_build_image(image_name, dockerfile_path, dockerfile_name, dockerfile_github):
    """
    Attempt to pull the Docker image, and if it fails, build the image locally.
    """
    try:
        # Try pulling the image
        pull_image(dockerfile_github,image_name)
    except docker.errors.ImageNotFound:
        print(f"Pull failed. Building image: {image_name}")
        # If pulling fails, build the image
        build_mujoco_image(image_name, dockerfile_path, dockerfile_name)
    except docker.errors.APIError as e:
        print(f"Unexpected error during pull: {e}. Attempting to build the image.")
        build_mujoco_image(image_name, dockerfile_path, dockerfile_name)