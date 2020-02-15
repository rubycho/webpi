echo "============================"
echo "Starting webpi on your PI"
echo "============================"

step=1
echo "[Step ${step}]: enable pigpiod."

sudo systemctl start pigpiod.service

step=$((step+1))
echo "[Step ${step}]: enabling site."

sudo a2ensite webpi
sudo service apache2 restart

echo "============================"
echo "All step completed."
echo "============================"
