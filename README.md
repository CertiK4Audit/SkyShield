### **Prerequisite**
1. Python 3.x
2. Node.js 16
### **POC Database**
1. https://github.com/xcyyang/poc_database
2. Clone this POC database to local machine.
    - `git clone https://github.com/xcyyang/poc_database`
### **Installing**
1. Clone project: `git clone https://github.com/CertiK-Yuannan/SkyShield.git`
2. Switch to the branch `ExploitFramework`: `git checkout ExploitFramework`
3. Modify `setting.yml`: change the path of poc_database
4. Init framework:
    - `python3 framework.py`
    - Execuate `init` command to intall require node_modules
### **Usage**
1. Show all command: `help`
2. Exit framework: `exit`
3. Clear command shell: `clear`
4. Show the info of specific command: `help [commmand]`
5. List all POC: `list`
6. Search POC with keyword: `search [keyword]`
7. Load a POC: `load [name]`
8. Show the parameters of loaded POC: `show_parameters`
9. Set specific parameter of loaded POC: `set [categories] [parameter] [value]`
    - Example: 
        - `set networks url https://speedy-nodes-nyc.moralis.io/TOKEN/bsc/mainnet/archive`
        - `set address PAIR 0x02b0551B656509754285eeC81eE894338E14C5DD`
10. Import parameters from config file: `import [path_to_config_yml]`
11. Run loaded POC: `run`
### **Development Mode**
1. Enter dev mode: `enter_dev_mode`
2. Exit dev mode: `exit_dev_mode`
3. In the dev mode, the `load` action will copy the source code of specific POC in poc_database to the folder `exploits`. Then, developer can modify the POC for debugging. Or developer can create a POC via creating a folder under `exploits` folder, like `exploits/[POC_name]`. To test this new POC, developer can simply execute `load [POC_name]` under dev mode, then use `run` command to test new POC.
4. Automatically generate template for POC: 
    - **Still in progress**
