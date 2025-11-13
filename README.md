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
http://127.0.0.1:8000/outer-ear/space-domain-analysis?ec_length=0.03&fi=100&ff=1000&nf=100&frequencies=100&frequencies=200&middleEarCondition=otosclerosis&middleEarSeverity=low
```
or

```
http://127.0.0.1:8000/outer-ear/frequency-domain-analysis?ec_length=0.03&fi=100&ff=1000&nf=100&positions=0.005&positions=0.02&middleEarSeverity=low
```
or
```
http://127.0.0.1:8000/outer-ear/frf?ec_length=0.03&fi=4000&ff=7000&nf=100&input_position=0.01&output_position=0.025&me_severity=low
```
or

```
http://127.0.0.1:8000/middle-ear/frf?fi=4000&ff=7000&nf=2&measures=Hfp&measures=Zme&measures=ER&me_severity=low
```
or

```
http://127.0.0.1:8000/input-signal/magnitude-spectrum?fi=4000&ff=7000&nf=2&inputSignal=idealWhiteNoise
```


```
http://127.0.0.1:8000/input-signal/magnitude-spectrum?fi=4000&ff=7000&nf=2&inputSignal=speech
```