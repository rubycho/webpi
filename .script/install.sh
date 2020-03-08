echo "============================"
echo "Installing webpi on your PI"
echo "============================"

curr_dir=$(pwd)
if [ ! "${curr_dir}" = '/home/pi/webpi' ]; then
  echo "Aborting installation."
  echo "Please place the webpi repo on /home/pi."
  exit
fi

step=1
echo "[Step ${step}]: install apt packages."

sudo apt update
sudo apt -y install python3 python3-pip virtualenv
sudo apt -y install pigpio python-pigpio python3-pigpio
sudo apt -y install apache2 apache2-dev libapache2-mod-wsgi-py3

step=$((step+1))
echo "[Step ${step}]: create venv and activate."

if [ ! -d "venv" ]; then
  virtualenv venv -p python3
fi
source venv/bin/activate

step=$((step+1))
echo "[Step ${step}]: install pip packages."

pip install -r requirements.txt
pip install mod_wsgi

step=$((step+1))
echo "[Step ${step}]: enable pigpiod."

wget https://raw.githubusercontent.com/joan2937/pigpio/master/util/pigpiod.service
sudo cp pigpiod.service /etc/systemd/system
sudo systemctl enable pigpiod.service
sudo systemctl start pigpiod.service

# cleanup
rm pigpiod.service

step=$((step+1))
echo "[Step ${step}]: create admin user."

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

step=$((step+1))
echo "[Step ${step}]: collect static files."

python manage.py collectstatic

step=$((step+1))
echo "[Step ${step}]: create self-signed certificate."

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
 -keyout ./.cert/webpi.key -out ./.cert/webpi.crt

step=$((step+1))
echo "[Step ${step}]: enabling site."

sudo a2enmod ssl
sudo service apache2 start

if ! grep -q ".env.prod" /etc/apache2/envvars; then
  echo ". /home/pi/webpi/.envs/.env.prod" | sudo tee -a /etc/apache2/envvars 1>/dev/null
fi

sudo cp .prod/webpi.conf /etc/apache2/sites-available/
sudo a2ensite webpi
sudo service apache2 restart

sleep 1

chmod 775 .
chmod 664 ./db.sqlite3
sudo chown :www-data ./db.sqlite3
sudo chown :www-data ./

echo "============================"
echo "All step completed."
echo "Have fun!"
echo "============================"
