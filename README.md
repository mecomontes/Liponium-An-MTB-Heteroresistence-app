# **Liponium:** An MTB-Heteroresistence app

A Bioinformatic tool to find mutations that cause Heteroresistance of MTB that is considered a preliminary stage to full resistance. Studies addressing the mechanisms underlying heteroresistance in TB are lacking so far. The aim of this tool is helping in studies of systematical causes of heteroresistance to Delamanid, Ethambutol, Etionamida, Streptomycin, Fluoroquinolones,  Isoniazide, Pyrazinamide, and other antibiotics.
---
## 0. Basic Requirements
You shold have installed make, pip for python 3, and conda before to install Liponium tool in you machine.

### Install make
The make utility will determine automatically which pieces of a large program need to be compiled, and issue the commands to recompile them. You may install make and build-essentail by typing:
```
sudo apt-get install make
sudo apt-get install build-essential
```

### Install pip package installer for Python
pip is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes. To install pip copy the below line and type enter:
```
sudo apt-get update
sudo apt-get install -y python3-pip
```
### Install Conda package manager
Conda is a cross-platform, language-agnostic binary package manager. It is the package manager used by Anaconda installations, but it may be used for other systems as well. Conda makes environments first-class citizens, making it easy to create independent environments even for C libraries. Conda is written entirely in Python, and is BSD licensed open source.
To install conda copy the below line and type enter:
```
pip install -y conda
```

**IMPORTANT: You may need to close and restart your shell (Terminal) before to install Liponium tool**
---

## 1. Download the Liponium repository [here](https://github.com/mecomontes/MTB-Heteroresistence)

<div align ="center "><img src='./images/download.png' alt='Liponium' width="700"></div>
---

## 2. Extract Liponium folder on your local machine.

---
## 3. Move into **"Liponium-An-MTB-Heteroresistence-app"** folder in your local machine and open a terminar (CLI).

<div align ="center "><img src='./images/terminal.png' alt='Liponium' width="700"></div>
---

## 4. Create a virtual enviroment for Liponium app:
```
conda create -n liponium python=3.7
```
and type y (yes)

<div align ="center "><img src='./images/create.png' alt='Liponium' width="700"></div>
---

## 5. Activate the Liponium enviroment:
```
conda activate liponium
```
<div align ="center "><img src='./images/activate.png' alt='Liponium' width="700"></div>
---

## 6. Install modules, libraries, and all the necessary dependencies:
```
make
```
<div align ="center "><img src='./images/requirements.png' alt='Liponium' width="700"></div>
---

## 7. Run Liponium app:
```
./Liponium.py
```
<div align ="center "><img src='./images/run.png' alt='Liponium' width="700"></div>
---

## 8. Selec the folder with your fastq files

<div align ="center "><img src='./images/folder.png' alt='Liponium' width="700"></div>
---

## 9. Liponium creates 3 different reports in the same folder.

<div align ="center "><img src='./images/reports.png' alt='Liponium' width="700"></div>
---

You could find the generated reports at "Reports" folder inside the Liponium folder.

- Reference_Report.xlsx: An EXCEL file that contains the initial info inputed.

- Unmerged_Report.xlsx: An EXCEL file with the result after aplying the Liponium searching. 

- Merged_Report.xlsx: Its a full report with that merged the initial info (Reference.xlsx) with the generated data (Unmerged.xlsx).

<div align ="center "><img src='./images/merged.png' alt='Liponium' width="700"></div>
---

## 10. Deactivate the enviroment (Optional):
```
conda deactivate
```
---

## Authors

* **Robinson Montes** - [mecomonteshbtn](https://github.com/mecomontes)
* **Felipe Rodríguez** - [felipe](https://github.com/felipedjrg)
