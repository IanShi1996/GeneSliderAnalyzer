import pandas as pd


class BinaryPairPredictor:
    """
    BinaryPairPredictor makes predictions of binary pairs, based on binding
    motif data, and gff information for Arabidopsis thaliana.

    Based on code from Karin Isaev

    Attributes:
        self.indexed_gff (DataFrame): The pandas DataFrame containing
            information about Arabidopsis gff which indexed by gene id.
        motif_data (DataFrame): The pandas DataFrame containing motif
            information.
        binary_pairs (List): The list of successfully matched binary pairs.
    """

    def __init__(self, gff_file_name, motif_data_file_name):
        """(BinaryPairPredictor, String, String) -> None

        Initialize the binary pair predictor object, and open the required
        data files for analysis.

        Args:
            gff_file_name (String): The name of the csv file containing gff
                information.
            motif_data_file_name (String): The name of the csv file
                containing binding motif information.
        """
        # Open required data files
        self.indexed_gff = open_gff_file(gff_file_name)
        self.motif_data = open_motif_file(motif_data_file_name)
        # Create list of results
        self.binary_pairs = []

    def execute(self):
        """ (BinaryPairPredictor) -> None

        Predicts binary pairs for the data files.
        """

        for i in self.motif_data.index:
            # Get gene ids
            gene_1_agi = self.motif_data.agi1[i]
            gene_2_agi = self.motif_data.agi2[i]

            # Ensures that genes are also in gff data set
            try:
                # Get gene information
                gene_1_info = self.get_gene_info(gene_1_agi)
                gene_2_info = self.get_gene_info(gene_2_agi)

                # Get the strand for genes
                gene_1_strand = gene_1_info[3]
                gene_2_strand = gene_2_info[3]
                # Get gene start positions
                gene_1_start = gene_1_info[1]
                gene_2_start = gene_2_info[1]

                # Get motif id, end
                motif = self.motif_data.motifid[i]
                motif_end = int(self.motif_data.motifend[i])

                # Assign possible binary pair
                bin_pair_1 = (motif, gene_1_agi)
                bin_pair_2 = (motif, gene_2_agi)

                # Check if two genes are on the same strand
                if gene_1_strand == gene_2_strand:
                    self.process_same(bin_pair_1, bin_pair_2, gene_1_strand,
                                      gene_1_start, gene_2_start, motif_end)

                elif gene_1_strand != gene_2_strand:
                    self.process_diff(bin_pair_1, bin_pair_2, gene_1_strand,
                                      gene_2_strand, gene_1_start,
                                      gene_2_start, motif_end)
            except KeyError:
                continue

    def process_same(self, bp1, bp2, strand, g1_start, g2_start, m_end):
        """ (BinaryPairPredictor, Tuple, Tuple, String, int, int, int) -> None

        Append binary pair of (motif, gene 1) or (motif, gene 2) if the
        conditions for excepting a predicted binary pair is met. Handles
        these predictions of same strands.

        Args:
            bp1 (Tuple): The pair of (motif, gene1)
            bp2 (Tuple): The pair of (motif, gene2)
            strand (String): Either + or -, the strand to consider
            g1_start (Int): The starting index of gene 1
            g2_start (Int): The starting index of gene 2
            m_end (Int): The ending index of the motif
        """
        if strand == '+':
            if m_end < g1_start:
                distance = g1_start - m_end
                if distance <= 3000 and bp1 not in self.binary_pairs:
                    # Pairs motif to gene which comes after it
                    self.binary_pairs.append(bp1)
            if m_end < g2_start:
                distance = g2_start - m_end
                if distance <= 3000 and bp2 not in self.binary_pairs:
                    self.binary_pairs.append(bp2)
        elif strand == '-':
            if m_end > g1_start:
                distance = m_end - g1_start
                if distance <= 3000 and bp1 not in self.binary_pairs:
                    # Pairs motif to gene which comes after it
                    self.binary_pairs.append(bp1)
            if m_end > g2_start:
                distance = m_end - g2_start
                if distance <= 3000 and bp2 not in self.binary_pairs:
                    self.binary_pairs.append(bp2)

    def process_diff(self, bp1, bp2, g1_strand, g2_strand, g1_start,
                     g2_start, m_end):
        """ (BinaryPairPredictor, Tuple, Tuple, String, String, int, int,
        int) -> None

        Append binary pair of (motif, gene 1) or (motif, gene 2) if the
        conditions for excepting a predicted binary pair is met. Handles
        these predictions of different strands.

        Args:
            bp1 (Tuple): The pair of (motif, gene1)
            bp2 (Tuple): The pair of (motif, gene2)
            g1_strand (String): The strand of gene 1
            g2_stand (String): The strand of gene 2
            g1_start (Int): The starting index of gene 1
            g2_start (Int): The starting index of gene 2
            m_end (Int): The ending index of the motif
        """
        if g1_strand == '-' and g2_strand == '+':
            if m_end > g1_start:
                distance = m_end - g1_start
                if distance <= 3000 and bp1 not in self.binary_pairs:
                    self.binary_pairs.append(bp1)
            if m_end < g2_start:
                distance = g2_start - m_end
                if distance <= 3000 and bp2 not in self.binary_pairs:
                    self.binary_pairs.append(bp2)
        elif g1_strand == '+' and g2_strand == '-':
            if m_end < g1_start:
                distance = g1_start - m_end
                if distance <= 3000 and bp1 not in self.binary_pairs:
                    self.binary_pairs.append(bp1)
            if m_end > g2_start:
                distance = m_end - g2_start
                if distance <= 3000 and bp2 not in self.binary_pairs:
                    self.binary_pairs.append(bp2)

    def get_gene_info(self, gene_agi):
        """ (BinaryPairPredictor, String) -> ndarray

        Return an ndarray of the gene specified by the gene_agi.

        Args:
            gene_agi (String): The agi of the gene to search for.
        Return:
            An ndarray which contains gene data.
        """
        # Find the target gene, and drop any duplicated isoforms
        gene_info = self.indexed_gff.loc[gene_agi].drop_duplicates()

        # Check what type/how many data points were found
        if isinstance(gene_info, pd.Series):
            # Return values as nd array
            return gene_info.values
        elif isinstance(gene_info, pd.DataFrame):
            # Check if only one element remains
            if gene_info.size == 4:
                # Return values as nd array
                return gene_info.values[0]
            # Return the smallest isoform to use
            return get_smallest_isoform(gene_info)

    def get_gene_start(self, gene):
        """ (BinaryPairPredictor, String) -> String

        Return the start position of the target gene by querying the indexed
        gff file

        Args:
            gene (String): The agi to query
        """
        gene_start_query = self.indexed_gff.genestart.loc[[gene]]
        gene_start = int(gene_start_query.drop_duplicates().iloc[0])
        return gene_start

    def get_gene_strand(self, gene):
        """ (BinaryPairPredictor, String) -> String

        Return the stand of the gene by querying the indexed gff file

        Args:
            gene (String): The agi to query
        """
        gene_strand_query = (self.indexed_gff.strand.loc[[gene]])
        gene_strand = str(gene_strand_query.drop_duplicates()[0])
        return gene_strand


def open_gff_file(gff_file_name):
    """ (String) -> DataFrame

    Return a pandas DataFrame containing information from a gff file which
    has been processed for further analysis

    Args:
        gff_file_name (String): The name of the gff file
    """

    # Open gff file using tabs as delimiter
    gff = pd.read_csv(gff_file_name, delimiter='\t')
    # Slices the agi from the gene id column
    gff['geneid'] = gff['geneid'].str[3:12]
    # Sets column names
    gff.columns = ['chromonumb', 'genestart', 'geneend', 'strand', 'geneid']
    # Creates an indexed gff file
    indexed_gff = gff.set_index('geneid')

    return indexed_gff


def open_motif_file(motif_file_name):
    """ (String) -> DataFrame

    Return a pandas DataFrame containing information from a motif data file
    which has been processed for further analysis

    Args:
        motif_file_name (String): The name of the motif data file
    """

    # Open motif file using tabs as delimiter
    motif_file = pd.read_csv(motif_file_name, delimiter='\t')
    # Extracts the agi-agi boundary of the motif as two agi
    motif_file['agi1'] = motif_file['gene ids'].str.extract('(.........-)')
    motif_file['agi2'] = motif_file['gene ids'].str.extract('(-.........)')
    # Delete boundary column
    del motif_file['gene ids']
    # Create two new columns containing the agi-agi boundaries
    motif_file['agi1'] = motif_file['agi1'].str[:9]
    motif_file['agi2'] = motif_file['agi2'].str[1:]
    # Set column names
    motif_file.columns = ['motifid', 'strand', 'motifstart', 'motifend',
                          'agi1', 'agi2']
    return motif_file


def get_smallest_isoform(gene_data_frame):
    """ (DataFrame) -> ndarray

    Return the shortest gene isoform contained in a given DataFrame.

    Args:
        gene_data_frame (DataFrame): The DataFrame containing multiple genes
            to compare.

    Return: The ndarray with containing the values of the shortest gene
    """

    # List of gene distances
    gene_distances = []
    # Gets each ndarray stored in the DataFrame
    for isoform_data in gene_data_frame.values:
        # Get start and end values from ndarray
        gene_end = isoform_data[2]
        gene_start = isoform_data[1]
        gene_distances.append(gene_end-gene_start)
    # Get index of gene with smallest distance
    smallest_gene_index = gene_distances.index(min(gene_distances))
    # return data of gene with smallest distance as nd array
    return gene_data_frame.values[smallest_gene_index]


if __name__ == "__main__":
    bpp = BinaryPairPredictor("gff.csv", "weirauch_2.csv")
    bpp.execute()
    open("output_data.csv.txt", "w").write("\n".join(("\t".join(item)) for
                                                     item in bpp.binary_pairs))