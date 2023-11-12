# gRPC_Banking
Project implemented as part of requirement for the course CSE 531 Distributed and Multiprocessor Operating Systems offered by Arizona State University. The goal of this project is to build a distributed banking system that allows multiple customers to withdraw or deposit
money from multiple branches in the bank.
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
$ python run_branch.py -i ./test/input_10.json
```
- In the other terminal, start the customer clients using the following command
```shell
$ python run_customer.py -i ./test/input_10.json -o /path/to/output/folder
```

- The above command will run the customer events and store the outputs in 3 files `output1.json`, `output2.json` and `output3.json` in the mentioned output folder.
- **IMPORTANT:** If you want to rerun the programs, ensure that you re-run both the branch and customer scripts. If you re-run only `run_customer.py`, the output from the branch processes will contain results from the previous execution as well. 
## 4. Configuration Options
- The branch servers are all hosted on separate ports, starting from a single start_port and incrementing by one for each server. 
- The start_port value can be set in the [config file](resources/config.json)
- The default start_port is 9000