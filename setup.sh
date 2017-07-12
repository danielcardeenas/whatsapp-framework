RED='\033[1;31m'
ORANGE='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
#printf "I ${CYAN}love${NC} Stack Overflow\n"

install_requirements() {
    module_requirements="$1"
    
    pip3.5 -qqq install -r $module_requirements
    
    return_code=$?
    if [ $return_code != 0 ]; then
        printf "${RED}Error:[%d]. Try running it with root privilages\n" $return_code
        exit $return_code
    fi
}

install_forked_yowsup() {
    printf "Installing ${ORANGE}yowsup libraries${NC}\n"
    echo "--------------------------"
    cd libs/python-axolotl
    python3.5 setup.py -q install
    wait
    cd ../yowsup
    python3.5 setup.py -q install
    wait
    echo "--------------------------"
    # Return to root
    cd ../../
}

install_modules() {
    echo "Configuring modules"
    echo "--------------------------"
    cd modules
    for D in *; do
        if [ -d "${D}" ] && [ "${D}" != "__pycache__" ]; then
            if [ -f ${D}/requirements.txt ]; then
                echo "[${CYAN}${D}${NC}] Installing dependencies..."
                module_requirements="${D}/requirements.txt"
                install_requirements "$module_requirements"
            else 
                echo "[${CYAN}${D}${NC}] All good..."
            fi
        fi
    done
    wait
    
    echo "--------------------------"
    
    # Return to root
    cd ../
}

install_app_dependencies() {
    echo "Configuring framework"
    echo "--------------------------"
    echo "[${CYAN}mac${NC}] Installing dependencies..."
    
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