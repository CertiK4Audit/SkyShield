### **Prerequisite**
1. Python 3.x
2. Node.js 16
### **POC Templates**
`https://github.com/CertiK-Yuannan/PoC_Template.git`

### **Installing**
1. Clone project: `git clone https://github.com/CertiK-Yuannan/SkyShield.git`
2. Switch to the branch `ExploitFramework-light`: `git checkout ExploitFramework-light`
3. Init framework:
    - `python3 framework.py`
    - Execuate `init` command to intall require node_modules
### **Usage**
#### Basic command
1. Show all command: `help`
2. Exit framework: `exit`
3. Clear command shell: `clear`
4. Show the info of specific command: `help [commmand]`

#### Exploit related command
1. List all POC: `list`
2. Load the desired POC: `load [name]`
3. Show the parameters of loaded POC: `show_parameters`
4. Set specific parameter of the loaded POC: `set [categories] [parameter] [value]`
    - Example: 
        - `set networks url https://speedy-nodes-nyc.moralis.io/TOKEN/bsc/mainnet/archive`
        - `set address PAIR 0x02b0551B656509754285eeC81eE894338E14C5DD`
5. Set parameters in the yaml files and updated it to the loaded PoCs.
6. Import parameters from config file: `import [path_to_config_yml]`
7. test it by `test`

    - **Still in progress**
