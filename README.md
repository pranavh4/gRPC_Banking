# gRPC_Banking

## 1. Prerequisites
- Python3 with pip installed
- Linux (Tested with Ubuntu 22.04)
- Git

## 2. Setup Environment
- Clone the git repository
```shell
$ git clone https://github.com/pranavh4/gRPC_Banking.git
$ cd ./gRPC_Banking
```
- Create and activate a virtual environment in python. You can skip this step if you want to.
```shell
# install virtual env if you haven't
$ python -m pip install --user virtualenv
$ python -m venv ./.venv
$ source ./venv/bin/activate
```
- Install the required python packages using the provided requirements.txt. This will install the grpc libraries required for running the code.
```shell
$ pip install -r requirements.txt
```
## 3. Running the Programs
- Open two terminals and activate the python env if you have it
- Run the script to start the branch servers using the following command
```shell
$ python run_branch.py -i ./test/input.json
```
- In the other terminal, start the customer clients using the following command
```shell
$ python run_customer.py -i ./test/input.json
```
- The above command will run the customer events and print out the responses. If you need the output in a file, you can just pipe them to a file
```shell
$ python run_customer.py -i ./test/input.json > /path/to/output/file
```
