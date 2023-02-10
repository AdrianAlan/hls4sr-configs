# hls4sr-configs

[hls4ml](https://github.com/fastmachinelearning/hls4ml/) symbolic expressions may be optimized for latency.
This script generates `complexity_of_operators` which should be used as one of the arguments to [PySRRegressor](https://github.com/MilesCranmer/PySR) to guide  evolutionary search.

Run as follows:
```
python generate_cfg.py --part <part> --precision <precision>
```
