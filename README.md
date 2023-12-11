# gRPC_Banking
Project implemented as part of requirement for the course CSE 531 Distributed and Multiprocessor Operating Systems offered by Arizona State University. The goal of this project is to build a distributed banking system that allows multiple customers to withdraw or deposit
money from multiple branches in the bank.
The read-your-writes consistency model is also implemented to ensure that successive writes from a single client remain consistent across multiple branches.
## 1. Prerequisites
- Python3 with pip installed
- Linux (Tested with Ubuntu 22.04)
- Git

## 2. Setup Environment
- Clone the git repository and checkout to the submission-3 branch
```shell
$ git clone https://github.com/pranavh4/gRPC_Banking.git
$ cd ./gRPC_Banking
$ git checkout submission-3
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
- The above command will run the customer events and write the output in the specified output file.
```shell
$ python run_customer.py -i ./test/input.json -o /path/to/output/file
```
## 4. Configuration Options
- The branch servers are all hosted on separate ports, starting from a single start_port and incrementing by one for each server. 
- The start_port value can be set in the [config file](resources/config.json)
- The default start_port is 9000