import docker


client = docker.from_env()


def build_mujoco_image(image_name, dockerfile_path, dockefile_name):
    """
    Builds the docker image if does not exist
    TODO: Delete intermediate images (tag and name=none) after building
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
                                    dockerfile=dockefile_name,
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



def monitor_container(container):
    """
    Monitor the container state
    # TODO: Test functionality
    """
    client = docker.from_env()
    try:
        # Check container status
        container_obj = client.containers.get(container.id)
        for line in container_obj.logs(stream=True):
            print(f"Sim-Container log: {line.decode().strip()}")
        
        # Check if container stopped
        container_obj.wait()
        print(f"Container {container.id} finished.")

    except Exception as ex:
        print(f"Error monitoring container {container.id}: {str(ex)}")



def run_mujoco_simulation_in_background(image_name, container_port, host_port, user_id, scene_id):
    """
    Function to run the Docker container in a separate thread
    """
    try:
        # Run the Docker container (using the appropriate Docker SDK command)
        #print(f"image-name: {image_name}")
        container = run_mujoco_container(image_name, container_port, host_port, user_id, scene_id)
        
        # Monitor the container's status in the background
        monitor_container(container)
        
    except Exception as ex:
        print(f"Error running container: {str(ex)}")



def run_mujoco_container(image_name, container_port, host_port, user_id, scene_id):
    # TODO: build image and push it to git so we can pull the prebuild image instead of building it from zero every time
    # TODO: check if container is already running
    #* Possible to limit resources: mem_limit="2g" (limit 2GM RAM), nano_cpus=1e9 (1 CPU core)
    try:
        container = client.containers.run(
            image_name,
            name=f"{image_name}_{user_id}_{scene_id}",      # container name
            detach=True,
            stdout=True,
            stderr=True,
            auto_remove=True,       # container is removed automatically after it stops
            environment={           # environment variables
                        "USER_ID":user_id, 
                        "SCENE_ID":scene_id,
                        "CONTAINER_PORT":container_port
                        },
            ports={str(container_port):str(host_port)},  # Port mappings between frontend and simulation
            #* Bind object_files for faster setup??
            #volumes={'/host_path/': {'bind': '/container_path/', 'mode': 'rw'}},  # If volume mappings are needed
        )

        return container

    except Exception as ex:
        print(str(ex))
        return None