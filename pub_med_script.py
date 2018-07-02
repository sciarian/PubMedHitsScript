#####################################################################################
#
# This script is used to find the number hits that come when a cell lines
# primary name and each one of it's aliases are searched with a list of search terms 
# based on the primary site of the cell line. 
#
# @Author: Anthony Sciarini
# @Verion: 6/28/2018 
#
#####################################################################################



###############
#IMPORTED LIBS#
###############
import csv                              #Comma seperated values lib
from Bio import Entrez			#Make queries from Pub Med database

##########################################
#USED TO BUILD SEARCH QUERIES FOR PUB MED#
##########################################
query_builder = {
			'autonomic_ganglia' : ['nueroblastoma'],
			'biliary_tract' : ['cholangiocarcinoma'],
			'bone' : ['bone', 'sarcoma'],
			'breast' : ['breast cancer'],
			'central_nervous_system' : ['glioblastoma','glioma','astrocytoma'],
			'endometrium' : ['uterine'],
			'haematopoietic_and_lymphoid_tissue' : ['leukaemia'],
			'kidney' : ['renal cancer'],
			'large_intestine' : ['colon cancer'],
			'liver' : ['hepatocellular carcinoma','hepatoblastoma','adenocarcinoma'],
			'lung' : ['carcinoma'], 
			'oesophagus' : ['esophageal cancer'],
			'ovary' : ['ovarian cancer'],
			'pancreas' : ['pancreatic cancer'],
			'pleura' : ['mesothelioma'],
			'prostate' : ['prostatic cancer'],
			'salivary_gland' : ['carcinoma'],
			'skin' : ['melanoma'],
			'small_intestine' : ['carcinoma'],
			'soft_tissue' : ['sarcoma','soft tissue'],
			'stomach' : ['gastric'],
			'thyroid' : ['carcinoma'],
			'upper_aerodigestive_tract' : ['squamous'],
			'urinary_tract' : ['carcinoma']
 		 }

################################
#HOW THE RESULTS WILL BE STORED#
################################
'''

results = {}

results = {
		'CELL LINE NAME' : {
					'QUERY' : NUM_HITS
					'QUERY' : NUM_HITS
					'QUERY' : NUM_HITS
				   }
	  }
'''

#################################
#HOW THE RESULTS WILL BE QUERIED#
#################################

'''	EXAMPLE QUERY
		#Cell line: 143B
		#Aliases: 143b, 143 B, 143B TK-, 143BTK-, 143TK-, HOS-143B, HOS-143b, GM05887
		#Search Terms 143B due to having 'bone' as its site primary value: bone, sarcoma
		#Resulting queries for the cell line primary name and for each alias...

		(143B AND bone) OR (143B and sarcoma)
		... 
'''

##################################################################################
#
# This function takes a search query as string and returns a dictionary
# containing the results of the query from the pub med database.
#
# @Param query ~ String containing the search query
# @Return results ~ Dictionary containing the seach results
# @Reference ~ https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/
#
#################################################################################
def search(query):
    Entrez.email = 'sciarian@mail.gvsu.edu'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='100',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


#Open a csv file containing the names of all the spread sheets
with open('cell_lines.csv') as csvfile:
	#Make a csv reader
        reader = csv.DictReader(csvfile)

        #For each cell line primary name that was scanned by the reader...
	for row in reader:
		
		#####################	
		#PUT ALIASES IN LIST#		
		#####################		

		#Grab cell primary name
		primary_name = row['\xef\xbb\xbfCell line primary name']
		cell_als = [] 
		cell_als.append(primary_name)
		
		#Grab the synonyms for the cell
		cell_als_string = row['Cell line aliases']
		aliases = cell_als_string.split(';')
		cell_als += aliases

		####################################
		#MAKE QUERIES BASED ON PRIMARY SITE#
		####################################
		
		#Grab primary site
		primary_site = row['Site Primary']
		
		#Grab list of quoted strings from query builder dictionary
		if primary_site == '':
			break
		search_terms = query_builder[primary_site]

		#Build strings and store results
		and_str = ' AND '
		or_str = ' OR '
		open_par = '('
		close_par = ')'

		#Make a query for each cell line alias.
		alias_results = {}
		for alias in cell_als:
			query = ''
			#Add each search term to the query.
			for term in search_terms:

				#If there is more than one search term
				if query != '':
					query += or_str

				#Add search term to query
				query += open_par + alias + and_str + term + close_par

			#Search pub med with built query
			result = search(query)

			#Add the result of the search to the alias results dictionary
			alias_results[query] = result['Count']
	
		#############################################################################
		#ADD NUM HITS DATA FOR EACH ALIAS OF THE CELL LINE TO THE RESULTS DICTIONARY#
		#############################################################################		
		results[primary_name] = alias_results

############################# 				 			
#PRINT RESULTS IN CSV FORMAT#
#############################

#Make columns headers
hd_1_str = 'Cell.alias'
hd_2_str = 'Mentions'
hd_str = 'Primary.Name'
for x in range(1,51):
	hd_str += ',' + hd_1_str + str(x) +','+ hd_2_str + str(x)

#Print headers for spread sheet in a comma seperated value format.
print hd_str

#Print search term results for each cell line in csv format.
for key in results:
	row_str = key
	for key_2 in results[key]:
		row_str += ',' + key_2 +','+ results[key][key_2]	
	print row_str
	
###########
#TEST ZONE#
###########
'''
query = '(143B AND bone) OR (143B AND Sarcoma)'
results = search(query)
print 'Results for searching' + query
print results['Count']
'''
