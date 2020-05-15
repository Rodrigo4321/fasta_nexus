#!/usr/bin/env python3

import sys

if("-help" in sys.argv):
	sys.stderr.write("example: python fasta_nexus.py outgroup ngen \n")
	sys.exit(1)
else:
	fasta_file = sys.stdin
	outgroup = sys.argv[1] #cria variável outgroup que guarda o primeiro argumento
	ngen = int(sys.argv[2]) #cria variável ngen que guarda o segundo argumento


Dicionario = {}


def dic(fasta_file, Dicionario):
	'''
	Função que vai guardar as sequencia e os seus nomes do ficheiro fasta num 
	dicionário não podendo os nome ser maiores que 99 caracteres
	recebe 2 argumentos sendo um o ficheiro fasta (fasta_file) e o outro, um Dicionario
	vazio onde seram guardados as informações do ficheiro fasta, que por fim o retorna.
	'''
	with fasta_file as fl:
		for line in fl:
			line = line.strip()
			if not line:
				continue
			if line.startswith(">"):
				taxa = line[1:]
				if taxa not in Dicionario:
					Dicionario[taxa] = ""
				continue
			sequence = line
			Dicionario[taxa] += sequence
	for key in Dicionario.keys():
		if len(key) > 99:
			key = key[:99]
	return Dicionario


def header(Dicionario):
	'''
	função header é onde vais ser criado a parte inicial do ficheiro nexus
	recebe um argumento o Dicionario já com as informações do ficheiro fasta
	'''
	global body
	header = "#NEXUS\n\nBEGIN DATA;\n"
	Dimensions = "Dimensions NTAX=%d " % len(Dicionario.keys())
	for bases in Dicionario.values():
		NCHAR = len(bases)
		break
	Dimensions2 = "NCHAR=%d;\n" % NCHAR
	Format = "FORMAT DATATYPE=DNA MISSING=N GAP=-;\nMATRIX"
	nexus_file= header + Dimensions + Dimensions2 + Format
	print(nexus_file)
	

def body(Dicionario):
	'''
	função body diz respeito ao corpo do ficheiro nexus recebe o Dicionario como argumento
	 e onde é feito o ajuste das sequencias e seus nomes à direita. 
	'''
	dna = ""
	biggest_taxa = [max(Dicionario.keys(), key=len)]
	max_lenght = len(biggest_taxa[0])
	for chaves, sequences in Dicionario.items():
			offset = max_lenght - len(chaves)
			dna += " "*offset + chaves + "  " + sequences + "\n"
	print (dna)


def end(outgroup, ngen):
	'''
	função end recebe  outgroup e ngen como argumentos onde um é o outgroup do taxa
	 e o outro o valor do ngen, nesta função finaliza-se o ficheiro fasta e ainda se adiciona
	 um pequeno "MrBayes Block" no fim.
	 '''
	end = ""
	start = "  ;\nEND;\n\nbegin mrbayes;\n  set autoclose=yes;\n"
	outgroups = "  outgroup %s;\n" % outgroup
	ngens = "  mcmcp ngen=%d " % ngen 
	rest1 = "printfreq=1000 samplefreq=100 diagnfreq=1000 nchains=4 savebrlens=yes filename=MyRun01;\n  mcmc;\n  sumt filename=MyRun01;\nend;"
	end = start + outgroups + ngens + rest1
	print(end)


dic(fasta_file, Dicionario)
header(Dicionario)
body(Dicionario)
end(outgroup, ngen)