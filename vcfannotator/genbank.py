from Bio import SeqIO


class GenBank(object):
    def __init__(self, gb=False):
        self.__gb = SeqIO.read(open(gb, 'r'), 'genbank')
        self._index = None
        self.feature = None
        self.build_position_index()
        self.gene_codons = {}
        
    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, value):
        self._index = self.__position_index[value-1]
        self.__set_feature()
        
    def build_position_index(self):
        self.__position_index = [None] * len(self.__gb.seq)
        for i in xrange(len(self.__gb.features)):
            if self.__gb.features[i].type == "CDS":
                start = int(self.__gb.features[i].location.start)
                end = int(self.__gb.features[i].location.end)
                self.__position_index[start:end] = [i] * (end - start)
                
    def __set_feature(self):
        if self._index is None:
            self.feature_exists = False
            self.feature = None
        else:
            self.feature_exists = True
            self.feature = self.__gb.features[self._index]

    def codon_by_position(self, pos): 
        if self._index not in self.gene_codons: self.split_into_codons()   
        gene_position = self.position_in_gene(pos)        
        codon_position = gene_position/3
        return [self.gene_codons[self._index][codon_position], gene_position%3, codon_position+1]
        
    def split_into_codons(self):
        seq = self.__gb.seq[self.feature.location.start:self.feature.location.end]
        if self.feature.strand == -1:
            seq = seq.reverse_complement()
        self.gene_codons[self._index] = [seq[i:i+3] for i in range(0,len(seq),3)]
            
    def position_in_gene(self, pos):
        if self.feature.strand == 1:
            return pos-self.feature.location.start-1
        else:
            return self.feature.location.end-pos
        
    def base_by_pos(self, pos):
        print self.__gb.seq[pos-1]
        
    def get_flanking_region(self, alt_base, pos, length):
        
        genome_length = len(self.__gb.seq)
        start = pos-length-1
        end = pos+length
        start = 0 if start < 0 else start
        end = genome_length if end > genome_length else end
        return '{0}{1}{2}'.format(
            self.__gb.seq[start:pos-1],
            str(alt_base).lower(),
            self.__gb.seq[pos:end]
        )

