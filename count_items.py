import subprocess
import argparse
import codecs
##This application will receive a list of lemmas or tokens and so on and check a given database to find their counts

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('token_list_file',
            action="store", help="file with a list of tokens")

    parser.add_argument('dep_search_path',
            action="store", help="path to dep search installation")

    parser.add_argument('db_path',
            action="store", help="path to the database")

    parser.add_argument('-l', '--lemma', action='store_true', help='search for lemmas')

    args = parser.parse_args()

    inf = codecs.open(args.token_list_file,'rt','utf8')
    token_list = [l.strip() for l in inf] 
    inf.close()

    arg_list = token_list[:]
    if args.lemma: 
        arg_list = [u'L=' + t for t in token_list]

    for b in range(0, len(arg_list)):
        batch(arg_list[b],args,token_list[b],)

def batch(arg_list, args, token_list):

    token_counts = [0 for t in token_list]
    query = '|'.join(arg_list)
    dep_search_dir = args.dep_search_path
    db = args.db_path
    #Get the data
    query_cmd = dep_search_dir + 'query.py'
    iargs = [query_cmd, '-d', db, '-m', '0', query.encode('utf-8')]
    #print iargs
    p = subprocess.Popen(iargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    for l in out.split('\n'):
        if '\t' in l:
            try:
                token = l.split('\t')[1].decode('utf8')
                if args.lemma:
                    token = l.split('\t')[2].decode('utf8')
                if token in token_list:
                    token_counts[token_list.index(token)] += 1
            except:
                pass
    for l, c in zip(token_list, token_counts):
        print l.encode('utf8'), c
main()
