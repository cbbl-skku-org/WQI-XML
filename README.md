<h1 align="center">
    WQI-XML
    <br>
<h1>

<h4 align="center">Standalone program for the WQI-XML paper</h4>

<p align="center">
<a href=""><img src="https://img.shields.io/github/stars/nhattruongpham/WQI-XML?" alt="stars"></a>
<a href=""><img src="https://img.shields.io/github/forks/nhattruongpham/WQI-XML?" alt="forks"></a>
<a href=""><img src="https://img.shields.io/github/license/nhattruongpham/WQI-XML?" alt="license"></a>
<a href="https://doi.org/10.5281/zenodo.12778534">
    <img src="https://zenodo.org/badge/doi/10.5281/zenodo.12778534.svg" alt="DOI">
</a>
</p>

<p align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#installation">Installation</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#citation">Citation</a>
</p>


# Introduction
This repository provides the standalone program for the WQI-XML framework. The virtual environment, extracted features, and final models are available via Zenodo at [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.12778534.svg)](https://doi.org/10.5281/zenodo.12778534)

* Development: https://github.com/nhattruongpham/WQI-XML.git
* Release: https://github.com/cbbl-skku-org/WQI-XML.git

# Installation
## Software requirements
* Ubuntu 20.04.6 LTS
* Python 3.9



## Cloning this repository
```shell
git clone https://github.com/nhattruongpham/WQI-XML.git
```
OR
```shell
git clone https://github.com/cbbl-skku-org/WQI-XML.git
```
```shell
cd WQI-XML
```

## Creating a virtual environment
* Please download the virtual environment (_**wqixml.tar.gz**_) via Zenodo at [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.12778534.svg)](https://doi.org/10.5281/zenodo.12778534)
* Please extract it into the **envs** folder as below:
```
tar -xzf wqixml.tar.gz -C envs 
```
* Activate the virtual environment as below:
```
source envs/bin/activate
```

# Getting started
## Downloading for the independent dataset
* Please download the independent dataset (_**test_data.csv**_) via Zenodo at [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.12778534.svg)](https://doi.org/10.5281/zenodo.12778534)
* Please put the downloaded **test_data.csv** file into the **examples** folder


## Downloading all trained models
* Please download all final models (_**models.tar.gz**_) via Zenodo at [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.12778534.svg)](https://doi.org/10.5281/zenodo.12778534)
* Please extract it into the **models** folder as below:
```
tar -xzf models.tar.gz -C models 
```


## Running prediction
### Usage
```shell
python predictor.py --model_name <MODEL_NAME> --model_path <PATH_TO_MODEL_FOLDER> --test_data_path <PATH_TO_TEST_DATA_FILE> --norm_weight_path <PATH_TO_SCALER_FOLDER> --output_path <PATH_TO_RESULT_FOLDER>
```

### Helper
```shell
python predictor.py --help
```

### Example using the default configuration
```shell
python predictor.py
```


## Calculating WQI based on Vietnam's standard (Optional)

**Note:** We provide snippets for calculating WQI based on Vietnam's standard in the **utils.py** file. Please modify it accordingly.

# Citation
_**If you use this code or any part of it, as well as the independent dataset, please cite the following papers:**_
## Main
```
@article{authoryeartitle,
  title={},
  author={},
  journal={},
  volume={},
  number={},
  pages={},
  year={},
  publisher={}
}
```

## Zenodo
```
@misc{nguyen_thanh_2024_12778534,
  author       = {Nguyen Thanh, Phong and
                  Pham, Nhat Truong and
                  Manavalan, Balachandran and
                  Tran Anh, Duong},
  title        = {WQI-XML},
  month        = sep,
  year         = 2024,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.12778534},
  url          = {https://doi.org/10.5281/zenodo.12778534}
}
```
