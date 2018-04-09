import numpy as np


# paper _1
# author _2
# conf _3
def normalize_author_dbis(dirpath, dir_new_path):
    id_author_new = dir_new_path + 'id_author.txt'
    file = open(id_author_new, 'w')
    with open(dirpath + "id_author.txt") as adictfile:
        for line in adictfile:
            toks = line.strip().split("\t")
            if len(toks) == 2:
                file.write("2" + toks[0] + "\t" + toks[1] + "\n")
                print(toks)
    file.close()
    print('ok')


def normalize_conf_dbis(dirpath, dir_new_path):
    id_author_new = dir_new_path + 'id_conf.txt'
    file = open(id_author_new, 'w')
    with open(dirpath + "id_conf.txt") as adictfile:
        for line in adictfile:
            toks = line.strip().split("\t")
            if len(toks) == 2:
                file.write("3" + toks[0] + "\t" + toks[1] + "\n")
                print(toks)
    file.close()
    print('ok')

def normalize_paper_author_dbis(dirpath, dir_new_path):
    id_author_new = dir_new_path + 'paper_author.txt'
    file = open(id_author_new, 'w')
    with open(dirpath + "paper_author.txt") as adictfile:
        for line in adictfile:
            toks = line.strip().split("\t")
            if len(toks) == 2:
                file.write("1" + toks[0] + "\t" + "2"+toks[1] + "\n")
                print(toks)
    file.close()
    print('ok')

def normalize_paper_conf_dbis(dirpath, dir_new_path):
    id_author_new = dir_new_path + 'paper_conf.txt'
    file = open(id_author_new, 'w')
    with open(dirpath + "paper_conf.txt") as adictfile:
        for line in adictfile:
            toks = line.strip().split("\t")
            if len(toks) == 2:
                file.write("1" + toks[0] + "\t" + "3"+toks[1] + "\n")
                print(toks)
    file.close()
    print('ok')


dir_path = '/Volumes/DATA/AUS/2018/code/git/GraphSAGE/dbis_data/origin_net_dbis/'
dir_new_path = '/Volumes/DATA/AUS/2018/code/git/GraphSAGE/dbis_data/new_net_dbis/'
# normalize_author_dbis(dirpath=dir_path, dir_new_path=dir_new_path)
# normalize_conf_dbis(dirpath=dir_path, dir_new_path=dir_new_path)
# normalize_paper_author_dbis(dirpath=dir_path, dir_new_path=dir_new_path)
normalize_paper_conf_dbis(dirpath=dir_path, dir_new_path=dir_new_path)
