#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 21:15:32 2021

@author: Robinson Montes
"""
from time import time
from glob import glob
from os import popen
import pandas as pd
from fuzzysearch import find_near_matches
from Bio.Seq import Seq
from easygui import diropenbox, msgbox
from datetime import datetime


class heteroresistence:
    """Preliminary stage of a Bioinformatic tool to find a Heteroresistance of MTB addressing the heteroresistance in TB.
    """
    def __init__(self, reference_file):
        """Constructor for heteroresistence class.

        Args:
            reference_file (str): Input file that contains genes, probes, positions, and reference codons.
        """
        reference = pd.read_csv('Probes_MTB.csv')
        reference.dropna(subset=['Probe'], inplace=True)
        reference.to_csv('forward.csv', columns=['Gen-Position', 'Probe', 'Position'], index=False)
        self.ignore = reference[['Gen-Position', 'Reference Codon']]
        reference.drop(columns=['Position', 'Mutated Codon', 'Reference Aminoacid', 'Mutated Aminoacid'], inplace=True)

        self.forward = self.running('forward.csv')
        df_final = self.aminoacids_frequencies()
        df_final.reset_index(inplace=True)
        final = reference.merge(df_final, on='Reference Codon', how='right')
        final.fillna('', inplace=True)
        final = final[['Gen', 'Gen-Position', 'Gen AA', 'Mutation type', 'Probe', 'Position', 'Read', 'Reference Codon',
                    'Mutated Codon', 'Counts', 'Frequencies', 'Reference Aminoacid', 'Mutated Aminoacid', 'Drug Resistance',
                    'Notes', 'forward_SONDA', 'Gen.1', 'nucleotido', 'nucleotid', 'en']]
        date = datetime.today().strftime('%Y-%m-%d-%H-%M')
        final.to_excel(f'Merged_Report_{date}.xlsx', index=False)
        df_final.to_excel(f'Unmerged_Report_{date}.xlsx', index=False)
        reference.to_excel(f'Reference_Report_{date}.xlsx', index=False)


    def running(self, file_name):
        """Call the AWK process and take it dataframe results called file to mapping the data
        and retuns a dataframe with full data for each probe.  

        Args:
            file_name (str): Filename of the csv with probes and position to search.
            ignore (dataframe): Gen and Reference codon to ignore.

        Returns:
            (dataframe): Dataframe called file with full data for each finding probe in the fastq files.
        """
        start = time()
        file = self.nawkProcess(file_name)
        file['Raw'].replace('\n', float('NaN'), inplace=True)
        file.dropna(subset=['Raw'], inplace=True)
        df = file.apply(lambda df: self.mappingData(df['Gen-Position'],
                                                    df['Raw'],
                                                    df['Probe'],
                                                    df['Position'],
                                                    self.ignore.loc[self.ignore['Gen-Position'] == df['Gen-Position']]),
                                                    axis=1)
        print(f'Total time to {file_name[:-4]} process:  {time() - start} seconds')
        msgbox(title='Liponium: An MTB-Heterorresistence app',
               msg=f"""The reports were created successfully!\n\nTotal time for the {file_name[:-4]} process:  {time() - start} seconds'""",
               ok_button='Done',
               image=None)
        return df


    def nawkProcess(self, file_name):
        """Run a Blast searching on CLI injecting a AWK command to find lead considences in
        the fastq files.

        Args:
            file_name (str): Filename of the csv with probes and position to search.

        Returns:
            (dataframe): Dataframe called file with the raw data of reads finding in the AWK process.
        """
        file = pd.read_csv(file_name)
        file['Position'] = file['Position'].str.strip('[]')
        file = file.assign(pos=file['Position'].str.split('-')).explode('pos')
        file.dropna(inplace=True)
        file.drop(columns='Position', inplace=True)
        file.rename(columns={'pos': 'Position'}, inplace=True)
        file.insert(2, 'Raw', None, allow_duplicates=False)
        path = diropenbox(title="Liponium",
        		          msg="Select the fastq folder",
                          default='./')

        files = ' '.join(glob(f'{path}/*.fastq'))

        start = time()
        nawk = f"""cut -d',' -f2 {file_name}|tail --lines=+2|parallel -j12 \
            nawk -v pattern={{}} \\''BEGIN {{
                RS="@ER";
                probe = "";
                probe = pattern;
                for (i=0; i<=length(pattern); i++)
                    pp=substr(pattern,1,i-1) "." substr(pattern, i+1);
                    probe = probe "|" substr(pattern,1,i-1) "." substr(pattern, i+1);
                    print "~~~~"pattern"~~~~"
        }}
        $0 ~ probe'\\' {files}"""
        reads = popen(nawk).read()
        raw_data = reads.split('~~~~')[1:]
        
        data = {}
        for index in range(len(raw_data) - 1):
            data[raw_data[index]] = raw_data[index + 1]

        for index, row in file.iterrows():
            file.loc[index, 'Raw'] = data[row['Probe']]
        
        print(f'Time for AWK in Gen:  {time() - start} seconds')
        return file


    def mappingData(self, gen, reads, lead, position, ignore):
        """Mapping and transform the data in the raw dataframe obtained in AWK process to
        be processed, traduced, and filtered.

        Args:
            gen (str): Name of the gen to search in the fastq files.
            reads (str): fastq raw data to search in.
            lead (str): Sequence of the probe to seek in reads sequence.
            position (int): Nucleotide position after the codon matching.
            ignore (dataframe): Gen and Reference codon to ignore.

        Returns:
            (DataSerie): A Pandas data serie with gen, position, read, Phred's quality, and
                        codons for each matching.
        """
        df = pd.DataFrame(reads.split('\n\n'))
        df = df[0].str.split("\n", expand=True)[[1, 3]]
        df.rename(columns={1: 'Read', 3: 'Quality'}, inplace=True)
        df.dropna(inplace=True)
        
        df['Ends'] = df['Read'].apply(lambda read: self.findNear(lead, read, position))
        df.dropna(inplace=True)
        
        df['Codons'] = df.apply(lambda df: self.codons(df, self.ignore), axis=1)
        df['Phreds'] = df.apply(lambda df: self.phreds(df), axis=1)
        df.drop(columns=['Quality', 'Phreds'], inplace=True)
        df.dropna(inplace=True)
        df1 = (df.duplicated(keep=False)
            .groupby(df['Codons'])
            .size()
            .rename('Counts')
            .to_frame()
            .reset_index())
        df1.insert(0, "Gen", gen, allow_duplicates=False)
        df1.insert(2, "Ends", df['Ends'], allow_duplicates=False)
        df1.insert(3, "Read", df['Read'], allow_duplicates=False)
        return df1.values


    def findNear(self, lead, read, position):
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


    def codons(self, df, ignore):
        """Take the nucleotide triplet found and compare with reference codon and ask
        if is a mutate.

        Args:
            df (dataframe): Full data for each matching found.
            ignore (dataframe): Gen and Reference codon to ignore.

        Returns:
            (str): Reference and Mutated codon found
        """
        codon = df['Read'][int(df['Ends']):int(df['Ends']) + 3]
        if codon == '':
            return None
        elif len(codon) != 3:
            return None
        elif not self.ignore['Reference Codon'].empty and len(self.ignore['Reference Codon'].values[0]) != 0\
            and codon in self.ignore['Reference Codon'].values[0]:
            return None
        elif not self.ignore['Reference Codon'].empty and len(self.ignore['Reference Codon'].values[0]) != 0:
            return f'{codon}/{self.ignore["Reference Codon"].values[0]}'
        return f'{codon}/'


    def phreds(self, df):
        """Filter the quality of the reads based on Phred's quality

        Args:
            df (dataframe): Full data for each matching found.

        Returns:
            (str): Phred's quality if it pass the filter or None in other case. 
        """
        quality = df['Quality'][int(df['Ends']):int(df['Ends']) + 3]
        if pd.Series(quality).str.contains('^[@?A-Z]*$')[0] == True:
            return quality
        return None


    def aminoacids_frequencies(self):
        """Translate the finding codons to aminoacid using Biopython translate module.

        Args:
            df (dataframe): Full data for each matching found.

        Returns:
            (dataframe): Full data for each matching found, including reference and mutated aminoacid.
        """
        df_aa = self.forward.explode()
        df_aa.dropna(inplace=True)
        df_aa = pd.DataFrame(df_aa.tolist(), columns=['Genes', 'Codons', 'Position', 'Read', 'Counts'])
        df_aa.dropna(inplace=True)
        codon = df_aa['Codons'].str.split('/', expand=True)
        codon.columns = ['Mutated Codon', 'Reference Codon']
        df_aa = pd.concat([df_aa, codon], axis=1)
        df_aa['Frequencies'] = df_aa['Counts'] * 100 / df_aa['Counts'].sum()
        df_aa['Reference Aminoacid'] = df_aa['Reference Codon'].apply(lambda codon: f'{Seq(codon[:3]).translate()}')
        df_aa['Mutated Aminoacid'] = df_aa['Mutated Codon'].apply(lambda codon: f'{Seq(codon[:3]).translate()}')
        df_aa.drop(columns=['Codons'], inplace=True)
        return df_aa


if __name__ == '__main__':
    results = heteroresistence('Probes_MTB.csv')
