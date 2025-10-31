# auditory-system-api
API of the auditory system models

## Set up your local virtual environment

1. Create a virtual environment
```
python3 -m venv <venv_name>
```
If venv is not installed, run

```
sudo apt-get install python3-venv
```
2. Activate your virtual environment (for Linux)
```
source <venv_name>/bin/activate
```
3. Install packages using requirements.txt
```
pip install -r install/requirements.txt
```

## Fast test

1. After setup the environment, run the API
```
make run
```

2. Then, open your browser and type
```
http://127.0.0.1:8000/outer-ear/space-domain-analysis?ec_length=0.03&fi=100&ff=1000&nf=100&freqs_of_analysis=100&me_severity=low
```