from src.StatusChecker import CheckOrganizer
from kubernetes import client, config
from kubernetes.client import configuration


def main():
    config.load_kube_config()
    check_org = CheckOrganizer()

    print("Active host is %s" % configuration.Configuration().host)

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_namespaced_pod("default")
    # ret = v1.list_pod_for_all_namespaces()
    for item in ret.items:
        # print(item.metadata)
        result = check_org.do_check(item) 
        # print("-----------------------------")
        print(result)

        # break


if __name__ == '__main__':
    main()