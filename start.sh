RED='\033[0;31m'
GREEN='\033[0;36m'
NC='\033[0m' # No Color
#printf "I ${GREEN}love${NC} Stack Overflow\n"
echo "Searching modules"
cd modules
for D in *; do
    if [ -d "${D}" ] && [ "${D}" != "__pycache__" ]; then
        printf "Installing ${GREEN}${D}${NC}\n"
        if find ${D}/requirements.txt -maxdepth 0 -type f &> /dev/null
            then 
                echo "Installing dependencies...."
                pip3.5 install -r ${D}/requirements.txt
                
            else 
                echo "No dependencies needed"
        fi
    fi
done

#sudo python3.5 run.py