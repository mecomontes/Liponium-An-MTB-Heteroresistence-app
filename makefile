.PHONY: all setup_env install_requirements basic_requirements

all: setup_env install_requirements

setup_env :
	sudo apt install parallel
	sudo apt install gawk
	

install_requirements : requirements.txt
	pip install -r requirements.txt
	sudo apt-get upgrade
	sudo apt-get update

basic_requirements:
	sudo apt-get update
	sudo apt-get install -y python3-pip
	pip install conda

