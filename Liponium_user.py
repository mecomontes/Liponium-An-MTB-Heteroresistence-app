#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 21:15:32 2021

@author: Robinson Montes
"""
from distutils.command.clean import clean
from typing import List, Optional
from time import time
from glob import glob
from os import popen
import numpy as np
import pandas as pd
from fuzzysearch import find_near_matches
from Bio.Seq import Seq
from easygui import diropenbox, msgbox
from datetime import datetime


class heteroresistence:
    """Preliminary stage of a Bioinformatic tool to find a Heteroresistance of MTB addressing the heteroresistance in TB.
    """
    def __init__(self, reference_file: str):
        """Constructor for heteroresistence class.

        Args:
            reference_file (str): Input file that contains genes, probes, positions, and reference codons.
        """
        reference: pd.DataFrame = pd.read_csv('Probes_MTB.csv')
        reference.dropna(subset=['Probe', 'Reference Aminoacid'], inplace=True)
        reference.to_csv('forward5.csv', columns=['Gen-Position', 'Probe', 'Position'], index=False)
        self.ignore: pd.DataFrame  = reference[['Gen-Position', 'Reference Codon']]
        reference.drop(columns=['Position', 'Mutated Codon', 'Reference Aminoacid', 'Mutated Aminoacid'], inplace=True)

        self.forward = self.running('forward.csv')
        df_final: pd.DataFrame  = self.aminoacids_frequencies()
        df_final['Reference Codon'].replace('', np.nan, inplace=True)
        df_final.dropna(inplace=True)
        df_final.reset_index(inplace=True)
        final: pd.DataFrame = reference.merge(df_final, on='Reference Codon', how='right')
        final.fillna('', inplace=True)
        final = final[['Gen', 'Gen-Position', 'Gen AA', 'Mutation type', 'Probe', 'Position', 'Read', 'Reference Codon',
                    'Mutated Codon', 'Counts', 'Frequencies', 'Reference Aminoacid', 'Mutated Aminoacid', 'Drug Resistance',
                    'Notes', 'forward_SONDA', 'Gen.1', 'nucleotido', 'nucleotid', 'en']]
        
        date: str = datetime.today().strftime('%Y-%m-%d-%H-%M')
        
        final = final[final['Gen'] != 'pykA']

        popen('mkdir -p Reports').read()
        final.to_excel(f'./Reports/Merged_Report_{date}.xlsx', index=False)
        df_final.to_excel(f'./Reports/Unmerged_Report_{date}.xlsx', index=False)
        reference.to_excel(f'./Reports/Reference_Report_{date}.xlsx', index=False)


    def running(self, file_name: str) -> pd.DataFrame:
        """Call the AWK process and take it dataframe results called file to mapping the data
        and retuns a dataframe with full data for each probe.  

        Args:
            file_name (str): Filename of the csv with probes and position to search.
            ignore (pd.DataFrame): Gen and Reference codon to ignore.

        Returns:
            (pd.DataFrame): Dataframe called file with full data for each finding probe in the fastq files.
        """
        start = time()
        file: pd.DataFrame = self.gawk_process(file_name)
        file['Raw'].replace('\n', float('NaN'), inplace=True)
        file.dropna(subset=['Raw'], inplace=True)
        df: pd.DataFrame = file.apply(lambda line: self.mapping_data(line['Gen-Position'],
                                                    line['Raw'],
                                                    line['Probe'],
                                                    line['Position'],
                                                    self.ignore[self.ignore['Gen-Position'] == line['Gen-Position']]),
                                                    axis=1)
        print(f'Total time to {file_name[:-4]} process:  {time() - start} seconds')
        msgbox(title='Liponium: An MTB-Heterorresistence app',
               msg=f"""The reports were created successfully!\n\nTotal time for the {file_name[:-4]} process:  {time() - start} seconds'""",
               ok_button='Done',
               image=None)
        return df


    def gawk_process(self, file_name: str) -> pd.DataFrame:
        """Run a Blast searching on CLI injecting a AWK command to find lead considences in
        the fastq files.

        Args:
            file_name (str): Filename of the csv with probes and position to search.

        Returns:
            (pd.DataFrame): Dataframe called file with the raw data of reads finding in the AWK process.
        """
        file: pd.DataFrame = pd.read_csv(file_name)
        file['Position'] = file['Position'].str.strip('[]')
        file = file.assign(pos=file['Position'].str.split('-')).explode('pos')
        file.dropna(inplace=True)
        file.drop(columns='Position', inplace=True)
        file.rename(columns={'pos': 'Position'}, inplace=True)
        file.insert(2, 'Raw', None, allow_duplicates=False)
        path: str = diropenbox(title="Liponium",
        		          msg="Select the fastq folder",
                          default='./Fastq_Examples')
        print(path)

        files = self.compressed_files(path)
        
        start = time()
        gawk: str = f"""cut -d',' -f2 {file_name}|tail --lines=+2|parallel -j12 \
            gawk -v pattern={{}} \\''BEGIN {{
                RS="@ER";
                probe = "";
                probe = pattern;
                for (i=0; i<=length(pattern); i++)
                    pp=substr(pattern,1,i-1) "." substr(pattern, i+1);
                    probe = probe "|" substr(pattern,1,i-1) "." substr(pattern, i+1);
                    print "~~~~"pattern"~~~~"
        }}
        $0 ~ probe'\\' {files}"""
        reads: str = popen(gawk).read()
        raw_data: List[str] = reads.split('~~~~')[1:]
        popen('rm -rf ./tmp').read()
        
        data: dict = {}
        for index in range(len(raw_data) - 1):
            data[raw_data[index]] = raw_data[index + 1]

        for index, row in file.iterrows():
            file.loc[index, 'Raw'] = data[row['Probe']]
        
        print(f'Time for AWK in Gen:  {time() - start} seconds')
        return file


    def compressed_files(self, path: str) -> str:
        """Handling .gz compressed files as temporal extracted files.

        Args:
            path (str): Path with the fastq and fastq.gz files.

        Returns:
            files (str): All the files to be processed.
        """
        popen('mkdir -p tmp').read()
        gz_files: list = glob(f'{path}/*.fastq.gz')
        fastq_files: list = glob(f'{path}/*.fastq')
        
        for gz_file in gz_files:
            popen(f'cp {gz_file} ./tmp').read()
        
        gz_files: str = ' '.join(glob(f'./tmp/*.fastq.gz'))
        popen(f'gzip -df {gz_files}').read()
        
        tmp_files = glob(f'./tmp/*.fastq')
        fastq_files.extend(tmp_files)
        files = ' '.join(fastq_files)
        return files


    def mapping_data(self, gen: str, reads: str, lead: str, position: int, ignore: pd.DataFrame) -> pd.Series:
        """Mapping and transform the data in the raw dataframe obtained in AWK process to
        be processed, traduced, and filtered.

        Args:
            gen (str): Name of the gen to search in the fastq files.
            reads (str): fastq raw data to search in.
            lead (str): Sequence of the probe to seek in reads sequence.
            position (int): Nucleotide position after the codon matching.
            ignore (pd.DataFrame): Gen and Reference codon to ignore.

        Returns:
            (pd.Serie): A Pandas data serie with gen, position, read, Phred's quality, and
                        codons for each matching.
        """
        df: pd.DataFrame = pd.DataFrame(reads.split('\n\n'))
        df = df[0].str.split("\n", expand=True)[[1, 3]]
        df.rename(columns={1: 'Read', 3: 'Quality'}, inplace=True)
        df.dropna(inplace=True)
        
        if not df.empty:
            df['Ends'] = df['Read'].apply(lambda read: self.find_near(lead, read, position))
            df.dropna(inplace=True)
       
        if not df.empty:
            df['Codons'] = df.apply(lambda row: self.codons(row, ignore), axis=1)
        
        if not df.empty:
            df['Phreds'] = df.apply(lambda row: self.phreds(row), axis=1)
            df.drop(columns=['Quality', 'Phreds'], inplace=True)
        
        df.dropna(inplace=True)

        if not df.empty:
            df1: pd.Series = (df.duplicated(keep=False)
                .groupby(df['Codons'])
                .size()
                .rename('Counts')
                .to_frame()
                .reset_index())
            df1.insert(0, "Gen", gen, allow_duplicates=False)
            df1.insert(2, "Ends", df['Ends'], allow_duplicates=False)
            df1.insert(3, "Read", df['Read'], allow_duplicates=False)
            return df1.values
        return np.array([None, None, None, None])


    def find_near(self, lead: str, read: str, position: int) -> Optional[int]:
        """Find near matches of a lead in a read with 1 incidence

        Args:
            lead (str): Sequence of the probe to seek in reads sequence.
            read (str): fastq raw data to search in.
            position (int): Nucleotide position after the codon matching.

        Returns:
            (int): Nucleotide position after the codon matching.
        """
        find = find_near_matches(lead, str(read), max_l_dist=1)
        if find == []:
            return None
        return find[0].end + int(position) - 1


    def codons(self, df: pd.DataFrame, ignore: pd.DataFrame) -> Optional[str]:
        """Take the nucleotide triplet found and compare with reference codon and ask
        if is a mutate.

        Args:
            df (pd.DataFrame): Full data for each matching found.
            ignore (pd.DataFrame): Gen and Reference codon to ignore.

        Returns:
            (str): Reference and Mutated codon found
        """
        codon: str = df['Read'][int(df['Ends']):int(df['Ends']) + 3]

        if codon == '':
            return None
        elif len(codon) != 3:
            return None
        elif not ignore['Reference Codon'].empty and ignore['Reference Codon'].values[0]:
            return f'{codon}/{ignore["Reference Codon"].values[0]}'
        return f'{codon}/'


    def phreds(self, df: pd.DataFrame) -> Optional[str]:
        """Filter the quality of the reads based on Phred's quality

        Args:
            df (pd.DataFrame): Full data for each matching found.

        Returns:
            (str): Phred's quality if it pass the filter or None in other case. 
        """
        quality: pd.Series = df['Quality'][int(df['Ends']):int(df['Ends']) + 3]
        if pd.Series(quality).str.contains('^[@?A-Z]*$')[0] == True:
            return quality
        return None


    def aminoacids_frequencies(self) -> pd.DataFrame:
        """Translate the finding codons to aminoacid using Biopython translate module.

        Returns:
            (pd.DataFrame): Full data for each matching found, including reference and mutated aminoacid.
        """
        df_aa: pd.DataFrame = self.forward.explode()
        df_aa.dropna(inplace=True)
        df_aa = pd.DataFrame(df_aa.tolist(), columns=['Genes', 'Codons', 'Position', 'Read', 'Counts'])
        df_aa.dropna(inplace=True)
        codon: pd.DataFrame = df_aa['Codons'].str.split('/', expand=True)
        codon.columns = ['Mutated Codon', 'Reference Codon']
        df_aa = pd.concat([df_aa, codon], axis=1)
        df_aa['Frequencies'] = df_aa['Counts'] * 100 / df_aa['Counts'].sum()
        df_aa['Reference Aminoacid'] = df_aa['Reference Codon'].apply(lambda codon: f'{Seq(codon[:3]).translate()}')
        df_aa['Mutated Aminoacid'] = df_aa['Mutated Codon'].apply(lambda codon: f'{Seq(codon[:3]).translate()}')
        df_aa.drop(columns=['Codons'], inplace=True)
        return df_aa


if __name__ == '__main__':
    try:
        heteroresistence('Probes_MTB.csv')
    except:
        pass
