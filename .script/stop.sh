echo "============================"
echo "Stopping webpi on your PI"
echo "============================"

step=1
echo "[Step ${step}]: disable pigpiod."

sudo systemctl stop pigpiod.service

step=$((step+1))
echo "[Step ${step}]: disabling site."

sudo a2dissite webpi
sudo service apache2 stop

echo "============================"
echo "All step completed."
echo "============================"
