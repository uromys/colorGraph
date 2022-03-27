import sys
import itertools
import networkx as nx
import matplotlib.pyplot as plt
vertices = []
edges = []

import subprocess




def read_graph(filename):
    graph=nx.Graph()
    with open(filename) as f:
        for line in f.read().splitlines():
            if line:
                arrayOfNode=line.split(" ")
                graph.add_edge(int(arrayOfNode[0]),int(arrayOfNode[1]))
    nx.draw(graph,with_labels=True)
    plt.savefig("filename.png")
    plt.close()
    return graph


def create_graph_with_color(graph,dictOfColor):
    color_map=[]
    graph2=graph
    for index,node in enumerate(graph2):
            color_map.append(dictOfColor[index]['color'])

    nx.draw(graph2, node_color=color_map, with_labels=True)
    plt.show()
    plt.savefig("graphcolor.png")
    plt.close()


    # for index,node in enumerate(graph.nodes()):
    #     graph.nodes[node]['nodetype']=dictOfColor[index]['color']
    #
    # color_map= [u[1] for u in graph.nodes(data="nodetype")]
    # nx.draw(graph,with_labels=True,node_color=color_map)
    # plt.savefig("graphcolor.png")





def write_cnf(cnf, filename):

    # find the maximum number of a variable used
    variables = max(map(abs, itertools.chain(*cnf)))
    # concatenate clauses into a string
    cnf_str = '\n'.join(map(lambda c: ' '.join(map(str, c)) + ' 0', cnf))

    print('CNF created, it has %d variables and %d clauses' %
          (variables, len(cnf)))

    with open(filename, 'w') as f:
        # write basic CNF information
        f.write('p cnf %d %d\n' % (variables, len(cnf)))
        f.write(cnf_str)
        f.write("\n")


correspondance={
    0 :"red",
    1 : "green",
    2 : "blue"
}
def generate_cnf(vertices, edges):
    nbrColor=3
    clauses = []
    dictClauses={}
    def p(i, j):
        value=i*nbrColor + j + 1
        dictClauses[value] = {"node":i,"color":correspondance[j]}
        return value
    #chaque sommet a au moins une couleur

    clauses += [[p(i, j) for j in range(nbrColor)] for i in range(len(vertices))]

    #au plus une couleur
    for i in range(len(vertices)):
        for c in range(nbrColor - 1):
                for d in range(c+1, nbrColor):
                    clauses += [[-p(i, c), -p(i, d)]]



    #pas edge de la même couleur

    for i,j in edges:
        u = int(i) - 1
        v = int(j) - 1
        for c in range(nbrColor):
            clauses += [[-p(u, c), -p(v, c)]]
    # print(dictClauses)
    return clauses,dictClauses


if __name__ == '__main__':
    nbrColor = 3
    graph = read_graph(sys.argv[1])
    cnf,dictCorrespondance = generate_cnf(graph.nodes, graph.edges)
    write_cnf(cnf, sys.argv[1] + '-' + '-col.cnf')
    command=["gophersat",sys.argv[1] + '-' + '-col.cnf']

    p = subprocess.run(command, capture_output=True, text=True)
    gophersat = p.stdout.split("v")[2]
    gophersat = gophersat.split(" ")
    print(gophersat)
    gophersat = [int(x) for x in gophersat[1:len(gophersat)-1]]
    print(gophersat)
    for element in gophersat:
        if element>0:
            dictCorrespondance[abs(element)]["true"]=True
        else:
            dictCorrespondance[abs(element)]["true"]=False

    dictCorrespondance={v['node']: v for k, v in dictCorrespondance.items() if v["true"]}
    print(dictCorrespondance)
    create_graph_with_color(graph,dictCorrespondance)
