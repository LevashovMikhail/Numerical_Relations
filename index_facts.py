import json

def extract_num(relations, entity, keyword):
    entities = relations.get('entities')
    entity_idx = -1
    for i in range(len(entities)):
        if entities[i].get('argument') == entity:
            entity_idx = i
            break
    keywords = relations.get('keywords')
    keyword_idx = -1
    num_idx = -1
    if entity_idx > -1:
        for j in range(len(keywords)):
            if keywords[j].get('argument') == keyword:
                keyword_idx = j
                keyword_rels = keywords[j].get('relations')
                for r in keyword_rels:
                    if r.get('entity_id') == entity_idx:
                        num_idx = r.get('num_id')
                        break
                break
    if keyword_idx > -1 and entity_idx > -1:
        num_rels = relations.get('nums')
        num_value = num_rels[num_idx].get('argument')
        return num_value
    return None

def get_key_by_arg(arg):
    if arg == "entities":
        return "entity_id"
    if arg == "keywords":
        return "keyword_id"
    if arg == "nums":
        return "num_id"
    return None

def extract_list(relations,arg_name,rel_arg_1,rel_arg_2,arg):
    rels = relations.get(arg_name)
    rels_list = None
    for l in rels:
        if l.get('arg') == arg:
            rels_list = l.get('relations')
    if rels_list is None:
        return None
    rels_1 = relations.get(rel_arg_1)
    rels_2 = relations.get(rel_arg_2)
    key_1 = get_key_by_arg(rel_arg_1)
    key_2 = get_key_by_arg(rel_arg_2)
    rels_words = []
    for r in rels_list:
        word1 = rels_1[r.get(key_1)].get("argument")
        word2 = rels_2[r.get(key_2)].get("argument")
        rels_words.append({"word1":word1,"word2":word2})
    if len(rels_words) > 0:
        return rels_words
    return None

def arg_idx(relations, arg_name, arg):
    entity_idx = -1
    for e in range(len(relations.get(arg_name))):
        if relations.get('entities')[e].get('argument') == arg:
            entity_idx = e
            break
    return entity_idx

def already_exists(relations, entity, keyword, num):
    entity_exists = False
    keyword_exists = False
    num_exists = False
    if arg_idx(relations,"entities",entity) > -1:
        entity_exists = True
    if arg_idx(relations,"keywords",keyword) > -1:
        keyword_exists = True
    if arg_idx(relations,"nums",num) > -1:
        num_exists = True
    if entity_exists and keyword_exists and num_exists:
        return True
    return False

def write_rel(entity, keyword, num):
    try:
        file_relations = open('c:\\Users\\User\\Numerical_Relation_Extraction\\data\\ruwiki_2018\\relations.json', 'r')
        relations = json.loads(file_relations.read())
        file_relations.close()
        if already_exists(relations, entity, keyword, num):
            print("Данное отношение уже содержится в базе фактов")
        entity_idx = arg_idx(relations, "entities", entity)
        if entity_idx < 0:
            new_entity = {'argument': entity, 'relations': []}
            relations.get('entities').append(new_entity)
            entity_idx = len(relations.get('entities')) - 1
        keyword_idx = arg_idx(relations, "keywords", keyword)
        if keyword_idx < 0:
            new_keyword = {'argument': keyword, 'relations': []}
            relations.get('keywords').append(new_keyword)
            keyword_idx = len(relations.get('keywords')) - 1
        num_idx = arg_idx(relations, "nums", num)
        if num_idx < 0:
            new_num = {'argument': num, 'relations': []}
            relations.get('nums').append(new_num)
            num_idx = len(relations.get('nums')) - 1
        relations.get('entities')[entity_idx].get('relations').append({'keyword_id': keyword_idx, 'num_id': num_idx})
        relations.get('keywords')[keyword_idx].get('relations').append({'entity_id': entity_idx, 'num_id': num_idx})
        relations.get('nums')[entity_idx].get('relations').append({'entity_id': entity_idx, 'keyword_id': keyword_idx})
        file_relations = open('c:\\Users\\User\\Numerical_Relation_Extraction\\data\\ruwiki_2018\\relations.json', 'w')
        file_relations.write(json.dumps(relations))
    except:
        print('Создаётся файл relations.json')
        file_relations = open('c:\\Users\\User\\Numerical_Relation_Extraction\\data\\ruwiki_2018\\relations.json', 'w',
                              encoding='utf-8')
        relations = {'entities': [], 'keywords': [], 'nums': []}
        relations.get('entities').append({'argument': entity, 'relations': [{'keyword_id': 0, 'num_id': 0}]})
        relations.get('keywords').append({'argument': keyword, 'relations': [{'entity_id': 0, 'num_id': 0}]})
        relations.get('nums').append({'argument': num, 'relations': [{'entity_id': 0, 'keyword_id': 0}]})
        file_relations.write(json.dumps(relations))
        # file_relations.close()
    finally:
        file_relations.close()
# print("Введите тройку \"сущность-ключевое слово-число\"")
# k = input().split(' ')
# k[2] = float(k[2])
k = [u'объект',u'свойство',1]
file_exists = True
try:
    file_relations = open('c:\\Users\\User\\Numerical_Relation_Extraction\\data\\ruwiki_2018\\relations.json','r')
    relations = json.loads(file_relations.read())
    print(relations)
    print(extract_num(relations,"объект","свойство"))
    file_relations.close()
    file_relations = open('c:\\Users\\User\\Numerical_Relation_Extraction\\data\\ruwiki_2018\\relations.json', 'w')
    k2 = [u'объект2',u'свойство2',2]
    # relations = json.loads(file_relations.read())
    relations.get('entities').append({'argument': k[0], 'relations': [{'keyword_id': 1, 'num_id': 1}]})
    relations.get('keywords').append({'argument': k[1], 'relations': [{'entity_id': 1, 'num_id': 1}]})
    relations.get('nums').append({'argument': k[2], 'relations': [{'entity_id': 1, 'keyword_id': 1}]})
    file_relations.write(json.dumps(relations))
except:
    print('Создаётся файл relations.json')
    file_relations = open('c:\\Users\\User\\Numerical_Relation_Extraction\\data\\ruwiki_2018\\relations.json','w',encoding='utf-8')
    file_exists = False
    relations = {'entities': [], 'keywords': [], 'nums': []}
    relations.get('entities').append({'argument': k[0], 'relations': [{'keyword_id': 0, 'num_id': 0}]})
    relations.get('keywords').append({'argument': k[1], 'relations': [{'entity_id': 0, 'num_id': 0}]})
    relations.get('nums').append({'argument': k[2], 'relations': [{'entity_id': 0, 'keyword_id': 0}]})
    file_relations.write(json.dumps(relations))
    # file_relations.close()
finally:
    file_relations.close()