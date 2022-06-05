# ShareNow

To run the evaluator first start the kubernetes cluster using kind
```
kind create cluster
```

Then run as many pods as you want using kubectl

```
kubectl run <pod_name> --image=<container-name> --restart=Never
```

Once the pods are ready, you can run the main python script to make necessary checks

```
python main.py
```

To adapt the computed checks, you can alter the .env file, leaving variables empty if you do not want them to run.

To test the package you can run

```
pytest
```

Note that it takes some time for the test pod to be deleted after the test suite, so running multiple times takes some time.


I wanted to deploy the package in a container but I was unable to connect the container to the kubernetes cluster. However, once that
is done it should work. The idea is to pass an environment file to the docker when it is ran, to adapt the number of checks done and 
which cluster is being evaluated.

Adding more rules is a matter of adding a new StatusCheck sub-class with a new environment variable

