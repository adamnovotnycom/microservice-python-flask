import subprocess
import sys
import generate_docker_files

app = "forecast_service"
sut = "sut_fs" # system under test
mode_options = ["dev", "devcloud", "stage", "prod"]

def main():
    mode = gen_docker_files()
    run_docker(mode)

def gen_docker_files():
    print("""
    Generate docker files. App mode:
    - options: {}
    - q: do not generate files
    """.format(mode_options))
    mode = input("Please make a selection: ")
    if mode in mode_options:
        generate_docker_files.main(mode=mode)
        return mode
    elif mode == "q":
        pass
    else:
        sys.exit("Invalid selection")
    
def run_docker(mode):
    print("""
    'ssh' - ssh into a service
    1 - start all services: {0}, {1}
    2 - stop all services: {0}, {1}
    3 - remove all services: {0}, {1}
    """.format(app, sut))

    help_str = "Please make selection(s). For multi-selection, separate by ',': "
    selections = [x.strip() for x in input(help_str).split(",")]

    for i in selections:
        if i == "ssh":
            sel_ssh()
        elif i == "1":
            sel_1(mode)
        elif i == "2":
            sel_2()
        elif i == "3":
            sel_3()
        else:
            sys.exit("Invalid selection")
    
def sel_ssh():
    cont = input("Please select a container: ")
    if cont == app or cont == sut:
        subprocess.call("docker exec -it {} /bin/bash".format(cont), shell=True)
    else:
        print("Incorrect container entered for ssh")
def sel_1(mode):
    if mode == "devcloud":
        mode = "dev"
    subprocess.call("""
    git checkout {};
    docker-compose -f docker-compose.yml up;
    """.format(mode), shell=True)
def sel_2():
    subprocess.call("""
    docker stop {1};
    docker stop {0};
    """.format(app, sut), shell=True)
def sel_3():
    subprocess.call("""
    docker rm {0};
    docker rm {1};
    """.format(app, sut), shell=True)

if __name__ == "__main__":
    main()