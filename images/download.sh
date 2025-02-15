for img in $(grep jpg images.json | cut -d '"' -f 4 | sed 's/.jpg//')
do
  if [ -f "${img}.jpg" ]
  then
    continue
  fi
  wget "https://ids.si.edu/ids/deliveryService?max_w=550&id=${img}" -O ${img}.jpg
done
