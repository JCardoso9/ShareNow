## File for deleting a pod manually

from kubernetes import client, config, utils
from kubernetes.client import configuration


def del_pod():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    api_response = v1.delete_namespaced_pod("configmap-test-pod", "default")


def start():
    config.load_kube_config()
    k8s_client = client.ApiClient()
    yaml_file = '/home/cnv/Desktop/ShareNow/test/test_config.yml'
    utils.create_from_yaml(k8s_client,yaml_file,verbose=True)

del_pod()