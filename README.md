
# Some useful commands
## Receiver command
```sh
python3 receiver.py --host localhost --port 5000 --dest_host localhost --dest_port 5001
```

## Sender command
This is to directly connect to the receiver, not using the newudpl
```sh
python3 sender.py --host localhost --port 5001 --dest_host localhost --dest_port 5000 --timeout 2
```

## using natcat
```shell script
nc -vv localhost 8888 -u
```