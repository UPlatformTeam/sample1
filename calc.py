import math


def get_entropy(count, all):
    p = count / float(all)
    if p == 0:
        return 0
    return math.log(p, 2) * -p


def get_information(values, all):
    sum = 0
    for k in values:
        sum += values[k]['count'] / float(all) * values[k]['entropy']
    return sum


def get_gain(ent, info):
    return ent - info


def find_info_and_gain(data, length, header):
    yes = 0
    no = 0
    for row in data:
        if row[length] == 'Да':
            yes += 1
        else:
            no += 1
    ent = entropy(yes, len(data)) + entropy(no, len(data))
    if yes == 0:
        return []
    elif no == 0:
        return []

    result = []
    for i in range(1, length):
        unique = {}
        for row in data:
            if row[i] not in unique:
                unique[row[i]] = {'count': 1}
                if row[length] == 'Да':
                    unique[row[i]]['yes'] = 1
                    unique[row[i]]['no'] = 0
                else:
                    unique[row[i]]['no'] = 1
                    unique[row[i]]['yes'] = 0
            else:
                unique[row[i]]['count'] += 1
                if row[length] == 'Да':
                    unique[row[i]]['yes'] += 1
                else:
                    unique[row[i]]['no'] += 1

        counter = 0
        for k in unique:
            counter += 1
            e = entropy(unique[k]['yes'], unique[k]['count']) + entropy(unique[k]['no'], unique[k]['count'])
            unique[k]['entropy'] = e

        info = information(unique, len(data))
        g = gain(ent, info)

        inf = '\nInfo(X={0}, T) = '.format(header[i])
        for k in unique:
            inf += '{0}/{1} * {2} + '.format(unique[k]['count'], len(data), unique[k]['entropy'])
        inf = inf[:-2]
        inf += '= {0}'.format(info)

        result.append({'header': header[i], 'info': info, 'gain': g})
    return result


def remove_item(source, idx):
    del source[idx]
    return source
