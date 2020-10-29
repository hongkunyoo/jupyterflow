# ML Pipeline

```bash
git clone https://github.com/hongkunyoo/jupyterflow.git
cd examples/ml-pipeline

ls -alh
# input.py
# train.py
# output.py
# workflow.yaml
# requirements.txt
```

- `input.py`: 
- `train.py`: 
- `output.py`: 
- `workflow.yaml`: 
- `requirements.txt`: 


```bash
pip install -r requirements.txt
```


```bash
python input.py
```


```bash
python train.py softmax 0.5
```


```bash
python output.py
```

```yaml
# workflow.yaml
jobs:
- python intput.py 
- python train.py softmax 0.5
- python train.py softmax 0.9
- python train.py relu 0.5
- python train.py relu 0.9
- python output.py

# Job index starts at 1.
dags:
- 1 >> 2
- 1 >> 3
- 1 >> 4
- 1 >> 5
- 2 >> 6
- 3 >> 6
- 4 >> 6
- 5 >> 6
```


```bash
jupyterflow run -f workflow.yaml
```