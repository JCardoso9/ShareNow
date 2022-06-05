import pytest
from kubernetes import client, config, utils
from kubernetes.client import configuration
from kubernetes.client.rest import  ApiException

@pytest.fixture(scope="session")
def pod_list(request):
    config.load_kube_config()

    k8s_client = client.ApiClient()
    yaml_file = 'test/test_config.yml'
    utils.create_from_yaml(k8s_client,yaml_file,verbose=True)

    print("Active host is %s" % configuration.Configuration().host)

    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)

    yield ret.items

    def fin():
        try:
            api_response = v1.delete_namespaced_pod("configmap-test-pod", "default")
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
    request.addfinalizer(fin)