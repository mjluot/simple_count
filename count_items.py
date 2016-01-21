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
        batch([arg_list[b]], args,[token_list[b]],)

def batch(arg_list, args, token_list):

    token_counts = [0 for t in token_list]
    if not arg_list[0].startswith('L='):
         query = '"' + '|'.join(arg_list) + '"'
    else:
         query = '|'.join(arg_list)

    dep_search_dir = args.dep_search_path
    db = args.db_path
    #Get the data
    query_cmd = dep_search_dir + 'query.py'
    iargs = [query_cmd, '-d', db, '-m', '0', query.encode('utf-8')]
    p = subprocess.Popen(iargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    #print out, err
    #import pdb;pdb.set_trace()
    count = 0
    for l in err.split('\n'):
        if 'Total number of hits:' in l:
            count = int(l.split(':')[-1].strip())
            break
    print arg_list[0], count

main()
