
# Some useful commands
## Receiver command
```sh
python3 receiver.py --host localhost --port 5000 --dest_host localhost --dest_port 5001
```

## Sender command
This is to directly connect to the receiver, not using the newudpl
```sh
python3 sender.py --host localhost --port 5001 --dest_host localhost --dest_port 5000 --timeout 2 < sample.txt
```

## Using NEWUDPL
http://www.cs.columbia.edu/~hgs/research/projects/newudpl/newudpl-1.4/newudpl.html

notice that
```shell script
-B bit error rate
Specifies a rate of genarating bit errors for outgoing packets. The rate is in 1/100000(BITERRDENOM).
Available range: 1 - 99999(BITERRDENOM - 1)
Default: 0

-L random packet loss rate
Specifies a rate of genarating random packet loss for outgoing packets. The rate is in percentage.
Available range: 1 - 99
Default: 0

-O out of order rate
Specifies a rate of randomizing oreder of packets. The distination host will receive some packets in out of order in certain rate. The rate is in percentage.
Available range: 1 - 99
Default: 0
```

Sample test:

### The following is out of order test from sender

connect to outbound of receiver
```shell script
./newudpl -vv -p 5001 -i "localhost/*" -o localhost:5003
```

connect to outbound of sender
```shell script
./newudpl -vv -p 5002 -i "localhost/*" -o localhost:5000 -O 99
```

Now the sender argument is
```shell script
python3 sender.py --host localhost --port 5003 --dest_host localhost --dest_port 5002 --timeout 2 < sample.txt
```

Now the receiver argument is 
```shell script
python3 receiver.py --host localhost --port 5000 --dest_host localhost --dest_port 5001
```

### The following is Loss packet test from sender
connect to outbound of receiver
```shell script
./newudpl -vv -p 5001 -i "localhost/*" -o localhost:5003
```

connect to outbound of sender
```shell script
./newudpl -vv -p 5002 -i "localhost/*" -o localhost:5000 -L 60
```

Now the sender argument is
```shell script
python3 sender.py --host localhost --port 5003 --dest_host localhost --dest_port 5002 --timeout 2 < sample.txt
```

Now the receiver argument is 
```shell script
python3 receiver.py --host localhost --port 5000 --dest_host localhost --dest_port 5001
```

### The following is bit error test from sender

connect to outbound of receiver
```shell script
./newudpl -vv -p 5001 -i "localhost/*" -o localhost:5003
```

connect to outbound of sender
```shell script
./newudpl -vv -p 5002 -i "localhost/*" -o localhost:5000 -B 80
```

Now the sender argument is
```shell script
python3 sender.py --host localhost --port 5003 --dest_host localhost --dest_port 5002 --timeout 2 < sample.txt
```

Now the receiver argument is 
```shell script
python3 receiver.py --host localhost --port 5000 --dest_host localhost --dest_port 5001
```

### The following is bit error test from receiver
connect to outbound of receiver
```shell script
./newudpl -vv -p 5001 -i "localhost/*" -o localhost:5003 -B 80
```

connect to outbound of sender
```shell script
./newudpl -vv -p 5002 -i "localhost/*" -o localhost:5000
```

Now the sender argument is
```shell script
python3 sender.py --host localhost --port 5003 --dest_host localhost --dest_port 5002 --timeout 2 < sample.txt
```

Now the receiver argument is 
```shell script
python3 receiver.py --host localhost --port 5000 --dest_host localhost --dest_port 5001
```

### The following is packet loss from receiver
connect to outbound of receiver
```shell script
./newudpl -vv -p 5001 -i "localhost/*" -o localhost:5003 -L 60
```

connect to outbound of sender
```shell script
./newudpl -vv -p 5002 -i "localhost/*" -o localhost:5000
```

Now the sender argument is
```shell script
python3 sender.py --host localhost --port 5003 --dest_host localhost --dest_port 5002 --timeout 2 < sample.txt
```

Now the receiver argument is 
```shell script
python3 receiver.py --host localhost --port 5000 --dest_host localhost --dest_port 5001
```


## using natcat
```shell script
nc -vv localhost 5000 -u
```