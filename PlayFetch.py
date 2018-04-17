import Doggo
import redis

def parse_username(url):
    if '"' == url[0]:
        url =  url[1:]
    if '"' == url[-1]:
        url = url[:-1]
    if 'twitter.com' not in url:
        raise Exception('wtf')
    beg = url.find('https://twitter.com/')
    end = url.find('?')
    if end == -1:
        result = url[beg+20:]
    else:
        result = url[beg+20:end]
    if '/' in result:
        if result[-1] == '/':
            result = result[:-1]
        else:
            raise Exception('wtf')
    return result

doggo = Doggo.Retriever()

with open('f_input.txt') as inp:
    for line in inp:
        contents = line.split('\t')

        if len(contents) == 1:
            handle = contents[0]
        elif len(contents) == 2:
            gvkey, handle = contents

        if progress % 100 == 0:
            print('n\\a count: {}'.format(nact))
            nact = 0

            print(progress)
            if workbook != None:
                workbook.close()
            workbook = xlsxwriter.Workbook('additional_book{}.xlsx'.format(int(progress/100)+1))
            worksheet = workbook.add_worksheet()
            row = 0
            col = 0
            for header in ['gvkey','id','time stamp',
                           'text','images','videos','hashtag',
                           'retweets','likes',
                           'join date','followers','following','total tweets']:
                worksheet.write(row, col, header)
                col += 1
            col = 0
            row += 1

        progress += 1

        if len(handle.split('/')) == 2:
            nact += 1
            continue

        try:
            handle = parse_username(handle.strip())
        except:
            print('bad url: {}'.format(handle), end='')
            continue

        try:
            for tweet in doggo.get_tweets(handle):
                worksheet.write(row, col, int(gvkey))
                for item in tweet:
                    col += 1
                    worksheet.write(row, col, item)
                row += 1
                col = 0     
        except Exception as e:
            print(e)
            continue                  
