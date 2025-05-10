if [ ! -f env.sh ]; then
  touch env.sh
fi

sudo docker run -p 5001:5001 -d --restart=on-failure  -env-file=env.sh --device=/dev/i2c-1 --device=/dev/i2c-2 --name powerhour  powerhour
