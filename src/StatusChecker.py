from abc import abstractmethod
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

class StatusChecker:

    @abstractmethod
    def do_check(self):
        pass


class ImageNameChecker(StatusChecker):

    def __init__(self, gold_image_prefix):
        super().__init__()
        self.name = "image_prefix"
        self.gold_image_prefix = gold_image_prefix

    def do_check(self, pod_info):
        image_names = [status.image for status in pod_info.spec.containers]
        if len(image_names) == 0:
            return False

        valid = self._check_image_prefix(image_names[0])

        if len(image_names) >= 2:
            for image_name in image_names:
                valid = valid and self._check_image_prefix(image_names[0])

        return valid

    
    def _check_image_prefix(self, image_name):
        split_image_name = image_name.split("/")

        split_image_name = set(split_image_name[:-1])
        return self.gold_image_prefix in split_image_name





class LabelChecker(StatusChecker):

    def __init__(self, label_name):
        super().__init__()
        self.name = f"{label_name}_label_present"
        self.label_name = label_name

    def do_check(self, pod_info):
        labels = pod_info.metadata.labels
        if labels is None:
            return False

        return self.label_name in labels and labels[self.label_name] is not None




class StartTimeChecker(StatusChecker):

    accepted_time_metrics = {
        "days",
        "hours",
        "minutes",
        "seconds"
    }

    def __init__(self, time_amount, time_metric):
        super().__init__()
        
        if (not isinstance(time_amount, int)) \
            or time_metric not in StartTimeChecker.accepted_time_metrics:
            raise ValueError("Start time arguments are invalid.")
        
        self.name = "recent_start_time"
        self.time_amount = time_amount
        self.time_metric = time_metric



    def do_check(self, pod_info):
        pod_start_time = pod_info.status.start_time
        now_utc = datetime.now(timezone.utc)
        time_diff = now_utc - pod_start_time

        if self.time_metric == "days":
            return  time_diff.days > self.time_amount
        
        elif self.time_metric == "hours":
            return  time_diff.seconds / 3600  > self.time_amount

        elif self.time_metric == "minutes":
            return  time_diff.seconds / 60 > self.time_amount
        
        elif self.time_metric == "seconds":
            return  time_diff.seconds > self.time_amount

    

class CheckOrganizer():

    def __init__(self):

        load_dotenv()
        self.IMAGE_PREFIX = os.getenv('IMAGE_PREFIX')
        self.LABEL_CHECK = os.getenv('LABEL_CHECK')
        self.TIME_AMOUNT = int(os.getenv('TIME_AMOUNT'))
        self.TIME_METRIC = os.getenv('TIME_METRIC')
        self.evaluators = []

        if self.IMAGE_PREFIX != "":
            self.evaluators.append(ImageNameChecker(self.IMAGE_PREFIX))


        if self.LABEL_CHECK != "":
            self.evaluators.append(LabelChecker(self.LABEL_CHECK))


        if self.TIME_AMOUNT != "" and self.TIME_METRIC != "":
            self.evaluators.append(StartTimeChecker(self.TIME_AMOUNT, self.TIME_METRIC))




    def do_check(self, pod_info):

        rule_evals = []
        for checker in self.evaluators:
            rule_evals.append({
                "name": checker.name,
                "valid": checker.do_check(pod_info)
            })

        return {
            "pod": pod_info.metadata.name,
            "rule_evaluation": rule_evals
        }


