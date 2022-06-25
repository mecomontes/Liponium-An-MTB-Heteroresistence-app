# Download the sequences from SRA
---

## 1. Instal sra-tools in the server
### Create and go to install directory
```
(env) home$ cd ~/home/tools/ncbi_sra_tools/
```
### Download latest SRA-toolkit version ( Ubuntu,  2022 )
```
(env) home$ wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.0.0/sratoolkit.3.0.0-ubuntu64.tar.gz
```
### decompress
```
(env) home$ tar -xvzf sratoolkit.3.0.0-ubuntu64.tar.gz
```
### check directory name (sra-tools version)
```
(env) home$ home$ ls

sratoolkit.3.0.0-ubuntu64/
sratoolkit.3.0.0-ubuntu64.tar.gz
```
### add location to system PATH (using current version directory name)
```
(env) home$ export PATH=$PATH:$HOME/tools/ncbi_sra_tools/sratoolkit.3.0.0-ubuntu64/bin
```
### SRA-toolkit configuration: define download path and other tool settings 
```
(env) home$ vdb-config --interactive
```
For example: define a large temporary download directory (default is location of $TMPDIR )

  CACHE: process-local location: /tmp/scratch

[https://github.com/ncbi/sra-tools/wiki/05.-Toolkit-Configuration](https://github.com/ncbi/sra-tools/wiki/05.-Toolkit-Configuration)
### check installation
```
(env) home$ fasterq-dump --help
(env) home$ fasterq-dump -V
```
---
## 2. Split the index file
split -d -l 100 SraPeruList.txt Peru
---

## 3. Run the main script to Clusterize the datasets
./main.sh Peru

