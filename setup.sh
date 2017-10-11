RED='\033[1;31m'
ORANGE='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

install_requirements() {
    module_requirements="$1"
    
    #printf "pip3 -qqq install -r $module_requirements"
    pip3 -qqq install -r $module_requirements
    
    return_code=$?
    if [ $return_code != 0 ]; then
        printf "${RED}Error:[%d]. Try running it with root privilages\n" $return_code
        exit $return_code
    fi
}

install_forked_yowsup() {
    printf "Installing ${ORANGE}yowsup libraries${NC}\n"
    printf "${NC}--------------------------\n"
    cd libs/python-axolotl
    python3 setup.py -qqq install
    wait
    cd ../yowsup
    python3 setup.py -qqq install
    wait
    printf "${NC}--------------------------\n"
    # Return to root
    cd ../../
}

install_modules() {
    printf "Configuring modules\n"
    printf "${NC}--------------------------\n"
    cd modules
    for D in *; do
        if [ -d "${D}" ] && [ "${D}" != "__pycache__" ]; then
            if [ -f ${D}/requirements.txt ]; then
                printf "[${CYAN}${D}${NC}] Installing dependencies...\n"
                module_requirements="${D}/requirements.txt"
                install_requirements "$module_requirements"
            else 
                printf "[${CYAN}${D}${NC}] All good...\n"
            fi
        fi
    done
    wait
    
    printf "${NC}--------------------------\n"
    
    # Return to root
    cd ../
}

install_app_dependencies() {
    printf "Configuring framework\n"
    printf "${NC}--------------------------\n"
    printf "[${CYAN}mac${NC}] Installing dependencies...\n"
    
    app_requirements="app/requirements.txt"
    install_requirements "$app_requirements"
    wait
}

# Step 1
install_forked_yowsup

# Step 2
install_modules

# Step 3
install_app_dependencies
