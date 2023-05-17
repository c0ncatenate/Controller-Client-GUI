# Controller-Client-GUI

## Disclaimer
This project was initially developed as a fundamental component of my university coursework. Subsequently, I dedicated further efforts to enhance its capabilities by integrating a more sophisticated graphical user interface (GUI) and expanding its repertoire of commands. The purpose of sharing this project is to allow individuals to utilize it as a valuable learning resource.

However, I must stress that it is not intended for employment in academic assignments. **Engaging in any form of plagiarism or academic misconduct can have severe consequences, compromising one's academic integrity and professional standing**. Consequently, I cannot assume responsibility for any such outcomes resulting from the misuse of this project.

# TODO
1. Enhance the GUI further.
2. Add more commands.
3. Spawn other processes and be able to control them.
4. Create a process and be able to maintain processes.
5. Be able to ethically escalate your priviledges. (example: using sudo)

# User Documentation
## Introduction
This document provides clear instructions on how to use this software, along with any module requirements that are needed to run or compile this software. The software is written in Python 3.11.1 and can be executed on any platform that has a Python environment installed.

## Requirements
Before running or compiling the software, the following requirements must be installed on your system:

- Python 3.x
- The modules listed in *requirements.txt*

## Installation
1. Clone or download the repository.
2. Open a terminal or command prompt and navigate to the directory containing the software.
3. Run the following command to install the necessary modules:  

    ```py
    pip install -r requirements.txt 
    ```
## Usage
To run this software, open a terminal or command prompt and navigate to the directory containing the software. Then, run the following command:

```bash
python main.py
```

This will start the controller.

## Interface

![image](https://github.coventry.ac.uk/storage/user/4924/files/d6bd127e-308d-40bf-b16d-6c90cb9ecd52)

Please enter the controller's IP address and port here, or just leave it as default.


### 1 - Connecting clients

![image](https://github.coventry.ac.uk/storage/user/4924/files/1a194162-06cd-4707-bbbd-59b8dfdd6dab)

Click on the start button to start the server, then launch client.py using this command:

```bash
python client.py
```
![image](https://github.coventry.ac.uk/storage/user/4924/files/cce31060-f442-4c3f-bc1b-1715afd77ab2)

Enter your controller's IP and it should connect.

### 2 - Send commands

![image](https://github.coventry.ac.uk/storage/user/4924/files/ede0ac2b-d71c-45c8-9737-fbf554deaa55)

Send commands using the textbox and click on 'Execute'

## Commands
The following commands are supported by the client and controller:

1. `hello`            - used to test the connection. The client will respond with `hi`.
2. `bye`              - used to end the connection and disconnect from the client.
3. `get_users()`      - used to get the list of users on the client.
4. `get_processes()`  - used to get all running processes on the client.
5. `get_id()`         - used to get the id of the client.
6. `get_os()`         - used to get the operating system of the client.
