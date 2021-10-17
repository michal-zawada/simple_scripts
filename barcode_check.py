import argparse
import os
import sys

"""
The script is accepting a barcode as input and comparing given barcode with given list of barcodes in a txt file (one line per barcode). 
It is accepting 2 missmaches in the barcode and checking also reverse complememtary barcode from the list.
The output is given to the terminal as barcode from the list per line, which has not more that 2 mismatches. 
Bases that do not match are given to the terminal as lower case. 

 """


parser = argparse.ArgumentParser()
parser.add_argument('--barcode', help='input barcode', dest='barcode', action='store')
parser.add_argument('--filepath', help='complete file path', dest='file', action='store')

args = parser.parse_args()


def check_barcode(barcode,filepath):
	print("Given barcode: {}".format(args.barcode))

	with open(filepath) as file:
		barcodes_l=file.readlines()
		barcodes_l=[line.rstrip() for line in barcodes_l]
		barcodes_l=filter(None,barcodes_l)
		barcode=barcode.upper()

		all_barcodes=[]
		for b in barcodes_l:
			if len(b)<len(barcode):
				print("Barcode {} is too short and will be excluded".format(b))
				continue
			b=b.upper()
			correct_bases=0
			barcode_list=[]
			correct_bases_reverse=0
			barcode_list_reverse=[]
			new_barcode_string=""
			new_barcode_string_reverse=""
			for i in range(0,len(barcode)):
				#print(i)
				if barcode[i]==b[i]:
					correct_bases=correct_bases+1
					new_barcode_string+=b[i]

					#print(barcode[i],b[i])
				else:
					#print(barcode,b,barcode[i],b[i])
					new_barcode_string+=b[i].lower() #if for a base is a mismatch, then mark it wit lower case
			if correct_bases > len(barcode)-3: #only 2 mismatches are allowed, so if there are 3, the barcode from the list is excluded 
				barcode_list.append(b)
				barcode_list.append(new_barcode_string)
				barcode_list.append(len(barcode)-correct_bases)
				all_barcodes.append(barcode_list)
			#reverse complementary
			#rc_b=b[::-1]
			#Checking the reverse complementary barcode:
			rc_b=""
			for n in b:
				if n=="A":
					rc_b="T"+rc_b
				elif n=="T":
					rc_b="A"+rc_b
				elif n=="G":
					rc_b="C"+rc_b
				elif n=="C":
					rc_b="G"+rc_b
				else:
					print("{} not recognized as a nucleotide".format(n))
			for i in range(0,len(barcode)):
				#print(i)
				if barcode[i]==rc_b[i]:
					correct_bases_reverse=correct_bases_reverse+1
					new_barcode_string_reverse+=rc_b[i]

					#print(barcode[i],rc_b[i])
				else:
					#print(barcode,rc_b,barcode[i],rc_b[i])
					new_barcode_string_reverse+=rc_b[i].lower()
			if correct_bases_reverse > len(barcode)-3:
				barcode_list_reverse.append("{}{}{}".format(rc_b," rev. comp. to ",b))
				barcode_list_reverse.append(new_barcode_string_reverse)
				barcode_list_reverse.append(len(barcode)-correct_bases_reverse)
				all_barcodes.append(barcode_list_reverse)


			

			#print(b)
			#print(rc_b)

		print("\nNumber_of_mismatches compared_barcode original_barcode")
		for i in all_barcodes:
			print(i[2],i[1],i[0])


	



#check_barcode("AGTTCC","BC_sheet.txt")

if os.path.exists(args.file):
	check_barcode(args.barcode,args.file)
else:
	print("The file path {} doesn't exist. Process terminated.".format(args.file))
	sys.exit()



