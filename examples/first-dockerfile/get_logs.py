import docker

def get_container_logs(container_name=None):
    """
    Retrieve logs from the specified container. If no container name is provided,
    retrieves logs from the current container.
    """
    client = docker.from_env()
    try:
        if container_name:
            container = client.containers.get(container_name)
        else:
            # Get logs from the current container
            container_id = open("/proc/self/cgroup").read().splitlines()[0].split("/")[-1]
            container = client.containers.get(container_id)
        
        logs = container.logs().decode("utf-8")
        print(f"Logs for container '{container.name}':")
        print(logs)
    except Exception as e:
        print(f"Error retrieving logs: {e}")

def get_container_info(container_name=None):
    """
    Retrieve basic information about the specified container.
    """
    client = docker.from_env()
    try:
        if container_name:
            container = client.containers.get(container_name)
        else:
            # Get info for the current container
            container_id = open("/proc/self/cgroup").read().splitlines()[0].split("/")[-1]
            container = client.containers.get(container_id)

        print(f"Information for container '{container.name}':")
        print(f"ID: {container.id}")
        print(f"Image: {container.image.tags}")
        print(f"Status: {container.status}")
        print(f"Ports: {container.ports}")
        print(f"Mounts: {container.attrs['Mounts']}")
    except Exception as e:
        print(f"Error retrieving container info: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get Docker container logs or info.")
    parser.add_argument("--logs", help="Retrieve logs of the specified container.", nargs='?', const=True)
    parser.add_argument("--info", help="Retrieve info of the specified container.", nargs='?', const=True)
    parser.add_argument("--container", help="Specify container name (default: current container).")

    args = parser.parse_args()

    if args.logs:
        get_container_logs(args.container)
    if args.info:
        get_container_info(args.container)
