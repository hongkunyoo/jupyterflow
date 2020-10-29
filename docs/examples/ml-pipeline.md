# ML Pipeline

Clone `jupyterflow` git repository and go to [examples/ml-pipeline](https://github.com/hongkunyoo/jupyterflow/tree/main/examples/ml-pipeline).

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

- `input.py`: Script for preparing train data.
- `train.py`: Model training experiments.
- `output.py`: Scores trained models.
- `workflow.yaml`: `jupyterflow` workflow file
- `requirements.txt`: Pip packages for ML pipeline

First, install required packages.

```bash
pip install -r requirements.txt
```

Run each script in jupyter notebook for test.

```bash
python input.py
python train.py softmax 0.5
python output.py
```

Write various training experiments to find the best performing model.

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

Run your ML Pipeline.

```bash
jupyterflow run -f workflow.yaml
```

Check out the result in Argo Web UI.
