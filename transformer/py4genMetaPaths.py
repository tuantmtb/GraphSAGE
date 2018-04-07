import sys
import os
import random
from collections import Counter
import networkx as nx
import json, io
import numpy as np
from networkx.readwrite import json_graph


class MetaPathGenerator:
    def __init__(self):
        self.id_author = dict()
        self.id_conf = dict()
        self.author_coauthorlist = dict()
        self.conf_authorlist = dict()
        self.author_conflist = dict()
        self.paper_author = dict()
        self.author_paper = dict()
        self.conf_paper = dict()
        self.paper_conf = dict()
        self.walks = []
        self.id_map = dict()

    def read_data(self, dirpath):
        with open(dirpath + "/id_author.txt") as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    self.id_author[toks[0]] = toks[1].replace(" ", "")

                    # print "#authors", len(self.id_author)

        with open(dirpath + "/id_conf.txt") as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    newconf = toks[1].replace(" ", "")
                    self.id_conf[toks[0]] = newconf

                    # print "#conf", len(self.id_conf)

        with open(dirpath + "/paper_author.txt") as pafile:
            for line in pafile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    p, a = toks[0], toks[1]
                    if p not in self.paper_author:
                        self.paper_author[p] = []
                    self.paper_author[p].append(a)
                    if a not in self.author_paper:
                        self.author_paper[a] = []
                    self.author_paper[a].append(p)

        with open(dirpath + "/paper_conf.txt") as pcfile:
            for line in pcfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    p, c = toks[0], toks[1]
                    self.paper_conf[p] = c
                    if c not in self.conf_paper:
                        self.conf_paper[c] = []
                    self.conf_paper[c].append(p)

        sumpapersconf, sumauthorsconf = 0, 0
        conf_authors = dict()
        for conf in self.conf_paper:
            papers = self.conf_paper[conf]
            sumpapersconf += len(papers)
            for paper in papers:
                if paper in self.paper_author:
                    authors = self.paper_author[paper]
                    sumauthorsconf += len(authors)

        print("#confs  ", len(self.conf_paper))
        print("#papers ", sumpapersconf, "#papers per conf ", sumpapersconf / len(self.conf_paper))
        print("#authors", sumauthorsconf, "#authors per conf", sumauthorsconf / len(self.conf_paper))

    def generate_random_aca(self, outfilename, numwalks, walklength):
        for conf in self.conf_paper:
            self.conf_authorlist[conf] = []
            for paper in self.conf_paper[conf]:
                if paper not in self.paper_author: continue
                for author in self.paper_author[paper]:
                    self.conf_authorlist[conf].append(author)
                    if author not in self.author_conflist:
                        self.author_conflist[author] = []
                    self.author_conflist[author].append(conf)
                    # print "author-conf list done"

        outfile = open(outfilename, 'w')
        for conf in self.conf_authorlist:
            conf0 = conf
            for j in range(0, numwalks):  # wnum walks
                outline = self.id_conf[conf0]
                for i in range(0, walklength):
                    authors = self.conf_authorlist[conf]
                    numa = len(authors)
                    authorid = random.randrange(numa)
                    author = authors[authorid]
                    outline += " " + self.id_author[author]

                    # append walks
                    self.walks.append([self.id_map[int(conf0)], self.id_map[int(conf0)]])  # conf_author*
                    confs = self.author_conflist[author]
                    numc = len(confs)
                    confid = random.randrange(numc)
                    conf = confs[confid]
                    outline += " " + self.id_conf[conf]

                    self.walks.append([self.id_map[int(conf)], self.id_map[int(author)]])  # conf*_author
                outfile.write(outline + "\n")
        outfile.close()
        return self.walks


# python py4genMetaPaths.py 1000 100 net_aminer output.aminer.w1000.l100.txt
# python py4genMetaPaths.py 1000 100 net_dbis   output.dbis.w1000.l100.txt

# dirpath = "net_aminer"
# OR 
# dirpath = "net_dbis"

# numwalks = int(sys.argv[1])
# walklength = int(sys.argv[2])
#
# numwalks = 1000
# walklength = 100


# dirpath = sys.argv[3]
# outfilename = sys.argv[4]


def main():
    # dirpath = "/Users/tuantmtb/Documents/AUS/metapath2vec/net_dbis"
    # numwalks = 5
    # walklength = 5
    # outfilename = '/Users/tuantmtb/Documents/AUS/metapath2vec/output/out.txt'
    # mpg = MetaPathGenerator()
    # mpg.read_data(dirpath)
    # mpg.generate_random_aca(outfilename, numwalks, walklength)
    config = {'output_dbis_data_folder': '/Volumes/DATA/AUS/2018/code/git/GraphSAGE/dbis_data/'}
    transform_graphsage(config=config)


def transform_graphsage(config):
    dirpath = "/Volumes/DATA/AUS/2018/code/git/GraphSAGE/dbis_data/net_dbis"
    numwalks = 5
    walklength = 5
    outfilename = '/Users/tuantmtb/Documents/AUS/metapath2vec/output/out.txt'
    mpg = MetaPathGenerator()
    mpg.read_data(dirpath)

    # set id article, author, conf, venue

    G_data = dict()
    G_data['directed'] = False
    G_data['graph'] = {'name': 'disjoint_union( ,  )'}
    G_data['multigraph'] = False

    # insert all nodes
    G_data['nodes'] = []
    G_data['links'] = []
    nodes = []
    edges = []
    class_map = dict()
    for paper_id in mpg.paper_conf:
        nodes.append(paper_id)
        edges.append({paper_id: mpg.paper_conf[paper_id]})

    for conf_id in mpg.id_conf:
        nodes.append(conf_id)

    for author_id in mpg.id_author:
        nodes.append(author_id)

    id_map = dict()
    index = 0
    for node in nodes:
        # node_object = {'feature': [], 'id': int(node), 'label': [], 'test': False, 'val': False}
        node_object = {'feature': [], 'id': index, 'label': [], 'test': False, 'val': False}
        id_map[int(node)] = index
        # print(node_object)
        G_data['nodes'].append(node_object)
        index += 1

    # class_map
    for paper_id in mpg.paper_conf:
        id = id_map[int(paper_id)]
        class_map[id] = [0, 0, 1] #paper

    for conf_id in mpg.id_conf:
        id = id_map[int(conf_id)]
        class_map[id] = [0, 1, 0] #conf
    for author_id in mpg.id_author:
        id = id_map[int(author_id)]
        class_map[id] = [1, 0, 1] #author

    # insert all edge
    for pap_au in mpg.paper_author:
        edges.append({pap_au: mpg.paper_author[pap_au][0]})

    for edge in edges:
        source_index = id_map[int(edge.keys()[0])]
        target_index = id_map[int(edge.values()[0])]

        edge_object = {'source': source_index, 'target': target_index, 'test_removed': False,
                       'train_removed': False}
        G_data['links'].append(edge_object)

    mpg.id_map = id_map

    # export file
    with io.open(config['output_dbis_data_folder'] + 'cora-G.json', 'w', encoding="utf-8") as f:
        f.write(unicode(json.dumps(G_data, ensure_ascii=False)))

    with io.open(config['output_dbis_data_folder'] + 'cora-id_map.json', 'w', encoding="utf-8") as f:
        f.write(unicode(json.dumps(id_map, ensure_ascii=False)))

    with io.open(config['output_dbis_data_folder'] + 'cora-class_map.json', 'w', encoding="utf-8") as f:
        f.write(unicode(json.dumps(class_map, ensure_ascii=False)))

    walks = mpg.generate_random_aca(outfilename, numwalks, walklength)

    np.savetxt(config['output_dbis_data_folder'] + 'cora-walks.txt', mpg.walks, fmt='%d')

    G = json_graph.node_link_graph(G_data)

    print("ok")
    # todo: feats, class_map
    return G, id_map, walks


if __name__ == "__main__":
    main()
