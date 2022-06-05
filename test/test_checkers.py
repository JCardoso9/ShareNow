import sys

sys.path.append("src")

from pytz import timezone
# from src.StatusChecker import LabelChecker
from StatusChecker import ImageNameChecker, LabelChecker, StartTimeChecker, CheckOrganizer
import pytest
from mocks import MockContainers, MockImage, MockLabels, MockStartTime
from datetime import datetime, timezone, timedelta



@pytest.mark.parametrize("pod_containers, expected_result", [
    (MockContainers([MockImage("bitnami/sajv")]), True),
    (MockContainers([MockImage("bit/sajv")]), False),
    (MockContainers([MockImage("bit/sajv"), MockImage("bit/sajv")]), False),
    (MockContainers([MockImage("bitnami/sajv"), MockImage("bitnami/sajv")]), True),
    (MockContainers([MockImage("bit/sajv"), MockImage("bitnami/sajv")]), False),
])
def test_image_name_mock(pod_list, monkeypatch, pod_containers, expected_result):
    check_org = ImageNameChecker("bitnami")
    pod = pod_list[0]
    monkeypatch.setattr(pod, "spec", pod_containers)

    assert check_org.do_check(pod) == expected_result 




@pytest.mark.parametrize("pod_labels, expected_result", [
    (MockLabels({"run":"mongo"}), False),
    (MockLabels({"team":"abc"}), True),
    (MockLabels({"run":"mongo", "team":"abc"}), True),
])
def test_labels_mock(pod_list, monkeypatch, pod_labels, expected_result):
    check_org = LabelChecker("team")
    pod = pod_list[0]
    monkeypatch.setattr(pod, "metadata", pod_labels)

    assert check_org.do_check(pod) == expected_result




@pytest.mark.parametrize("pod_start_times, time_amout, time_metric, expected_result", [
    (MockStartTime(datetime.now(timezone.utc)), 7, "days" ,False),
    (MockStartTime(datetime.now(timezone.utc)), 7, "hours" ,False),
    (MockStartTime(datetime.now(timezone.utc)), 7, "minutes" ,False),
    (MockStartTime(datetime.now(timezone.utc)), 7, "seconds" ,False),
    (MockStartTime(datetime.now(timezone.utc) - timedelta(days=7) ), 7, "days" ,False),
    (MockStartTime(datetime.now(timezone.utc) - timedelta(days=8) ), 7, "days" ,True),
    (MockStartTime(datetime.now(timezone.utc) - timedelta(hours=7) ), 7, "hours" ,False),
    (MockStartTime(datetime.now(timezone.utc) - timedelta(hours=8) ), 7, "hours" ,True),
    (MockStartTime(datetime.now(timezone.utc) - timedelta(minutes=7) ), 7, "minutes" ,False),
    (MockStartTime(datetime.now(timezone.utc) - timedelta(minutes=8) ), 7, "minutes" ,True),
    (MockStartTime(datetime.now(timezone.utc) - timedelta(seconds=7) ), 7, "seconds" ,False),
    (MockStartTime(datetime.now(timezone.utc) - timedelta(seconds=10) ), 7, "seconds" ,True), 
])
def test_start_times_mock(pod_list, monkeypatch, pod_start_times, time_amout, time_metric, expected_result):
    check_org = StartTimeChecker(time_amout, time_metric)
    pod = pod_list[0]
    monkeypatch.setattr(pod, "status", pod_start_times)

    assert check_org.do_check(pod) == expected_result




@pytest.mark.parametrize("pod_start_times, time_amout, time_metric, expected_result", [
    (MockStartTime(datetime.now(timezone.utc)), 7, "abc" ,False),
    (MockStartTime(datetime.now(timezone.utc)), "abc", "abc" ,False),
])
def test_error_args_start_times(pod_list, monkeypatch, pod_start_times, time_amout, time_metric, expected_result):
    with pytest.raises(ValueError) as excinfo:
        check_org = StartTimeChecker(time_amout, time_metric)





def test_do_check(pod_list):
    check_org = CheckOrganizer()

    # Pod is being created without start_time, there might be a way to create with start_time?
    # Since here we test for expected response creation, it is okay for now
    for pod in pod_list:
        if pod.metadata.name == "configmap-test-pod":
            pod_to_test = pod
            break
    pod_to_test.status.start_time = datetime.now(timezone.utc) 

    result = check_org.do_check(pod_to_test)

    expected = {
        'pod': 'configmap-test-pod', 
        'rule_evaluation': [
            {
                'name': 'image_prefix', 
                'valid': True
            }, 
            {
                'name': 'team_label_present', 
                'valid': False
            }, 
            {
                'name': 'recent_start_time', 
                'valid': False
            }
        ]
    }

    assert result == expected