# **Liponium:** An MTB-Heteroresistence app

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
pip install -r requirements.txt
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

Reference_Report.xlsx: An EXCEL file that contains the initial info inputed.

Unmerged_Report.xlsx: An EXCEL file with the result after aplying the Liponium searching. 

Merged_Report.xlsx: Its a full report with that merged the initial info (Reference.xlsx) with the generated data (Unmerged.xlsx).

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
