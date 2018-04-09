import json
import pdb
import sys

def reverse_map_id(data_dir, embed_dir, prefix, id_map):
        class_map = json.load(open(data_dir + "/" + prefix +"-class_map.json"))
        if id_map:
                reverse_map = json.load(open(data_dir + "/" + prefix  + "-id_map.json"))
        else:
                reverse_map = json.load(open(data_dir + "/" + prefix  + "-reverse_map.json"))
        output = []
        with open(embed_dir + "/val.txt") as fp:
                for i, line in enumerate(fp):
                        #if i==0: continue
        		output.append([reverse_map[line.strip()], class_map[line.strip()]])
        with open(embed_dir + "/reverse_val.txt", "w") as fp:
                for ele in output:
                        fp.write(str(ele[0]) + "\t" + str(ele[1][0]) + "\n")


if __name__ == "__main__":
        #python reverse_map.py dbis unsup-dbis/graphsage_mean_small_0.000010/ dbis t
        data_dir = sys.argv[1] #"./example_data/cora-n/ 
        embed_dir = sys.argv[2] #./unsup-cora-n/graphsage_mean_small_0.000010/
        prefix = sys.argv[3]
        id_map = sys.argv[4]
        reverse_map_id(data_dir, embed_dir, prefix, id_map)
	
