import dependency_graph

dependency_graph = dependency_graph.DependencyGraph(list(),dict())

def extract_num_rel(tokens,dependents,governors,entity_id,keyword_id,ignore_year=True,ignore_percent=False,change_words=[]):
    paths = []
    modified_relations = {'nmod', 'amod', 'adjmod', 'obj', 'advcl', 'nummod','nsubj','nsubj:pass'}
    for token in tokens:
        if token.get('pos') == "NUM" or token.get('pos') == "CD":
            paths.append(dependency_graph.shortest_tree_path(governors,entity_id,token.get('index')))
    if len(paths) == 0:
        return None
    shortest_path = None
    keyword_near_path = False
    for path in paths:
        keyword_on_path = False
        keyword_is_modifier = False
        change_word_in_path = False
        num_is_year = False
        percent_on_path = False
        governor_num = governors.get(path[-1].get('index'))
        for token in tokens:
            if token.get('index') == governor_num.get('index'):
                if ignore_year and token.get('lemma') == "год":
                    num_is_year = True
                    break
                if ignore_percent and token.get('originalText') == "%":
                    percent_on_path = True
                    break
        if num_is_year or percent_on_path:
            continue
        for word in path:
            for token in tokens:
                if token.get('index') == word.get('index'):
                    if token.get('lemma') in change_words:
                        change_word_in_path = True
                        break
                    if token.get('index') == keyword_id:
                        keyword_on_path = True
                        break
            if change_word_in_path:
                break
        if not keyword_on_path:
            for word_governor in path:
                token_dependents = dependents.get(word_governor.get('index'))
                keyword_is_modifier = False
                for dependent in token_dependents:
                    if dependent.get('index') == keyword_id:
                        if dependent.get('dep') in modified_relations:
                            keyword_is_modifier = True
                            break
                    elif dependent.get('dep') in modified_relations:
                        token_dependents_2 = dependents.get(dependent.get('index'))
                        keyword_is_modifier_2 = False
                        for dependent_2 in token_dependents_2:
                            if dependent_2.get('index') == keyword_id:
                                if dependent_2.get('dep') in modified_relations:
                                    keyword_is_modifier_2 = True
                                    break
                        if keyword_is_modifier_2:
                            keyword_is_modifier = True
                            break
                if keyword_is_modifier:
                    break
        if (keyword_on_path or keyword_is_modifier) and not (path is None):
            keyword_near_path = True
            if shortest_path is None:
                shortest_path = path
            elif len(path) < len(shortest_path):
                shortest_path = path
            elif len(path) == len(shortest_path):
            # если длина пути к какому-то другому числу совпадает с
            #уже имеющимся кратчайшим путём, то из них выбирается тот, в котором наименьшая разница
            #между индексами токенов (слов) сущности и числа, т.е. между каким числом меньше всего слов в предложении
                diff_of_index_sp = abs(entity_id - shortest_path[-1].get('index'))
                diff_of_index_p = abs(entity_id - path[-1].get('index'))
                print(shortest_path[-1].get('index'), path[-1].get('index'))
                print(diff_of_index_sp, diff_of_index_p)
                if diff_of_index_p < diff_of_index_sp:
                    shortest_path = path
    if keyword_near_path and not (shortest_path is None):
        return entity_id, keyword_id, shortest_path[-1].get('index')
    else:
        return None

def word_id_in_list(list_word,word_id,return_index=False):
    word_in_list = False
    if return_index:
        word_idx = -1
        for idx in range(len(list_word)):
            if list_word[idx].get('index') == word_id:
                word_in_list = True
                word_idx = idx
                break
        if word_in_list:
            return word_idx
    for word in list_word:
        if word.get('index') == word_id:
            word_in_list = True
            break
    return word_in_list

def extract_num_rel_2(tokens,dependents,governors,entity_id,keyword_id1,keyword_id2,ignore_year=True,ignore_percent=False,change_words=[]):
    paths = []
    modified_relations = {'nmod', 'amod', 'adjmod', 'obj', 'advcl', 'nummod','nsubj','nsubj:pass'}
    for token in tokens:
        if token.get('pos') == "NUM" or token.get('pos') == "CD":
            paths.append(dependency_graph.shortest_tree_path(governors,entity_id,token.get('index')))
    if len(paths) == 0:
        return None
    shortest_path = None
    keywords_near_path = False
    for path in paths:
        keyword_on_path = False
        keyword_is_modifier = False
        change_word_in_path = False
        num_is_year = False
        percent_on_path = False
        governor_num = governors.get(path[-1].get('index'))
        for token in tokens:
            if token.get('index') == governor_num.get('index'):
                if ignore_year and token.get('lemma') == "год":
                    num_is_year = True
                    break
                if ignore_percent and token.get('originalText') == "%":
                    percent_on_path = True
                    break
        if num_is_year or percent_on_path:
            continue
        for word in path:
            for token in tokens:
                if token.get('index') == word.get('index'):
                    if token.get('lemma') in change_words:
                        change_word_in_path = True
                        break
            if change_word_in_path:
                break
            if word.get('index') == keyword_id1:
                id1_dependents = dependents.get(keyword_id1)
                if word_id_in_list(id1_dependents,keyword_id2):
                    keywords_near_path = True
                    break
            if keywords_near_path:
                break
        if not keyword_near_path and not change_word_in_path:
            for word_governor in path:
                token_dependents = dependents.get(word_governor.get('index'))
                keyword_is_modifier = False
                keyword_idx = word_id_in_list(token_dependents,keyword_id1,True)
                if keyword_idx > -1:
                    if token_dependents[keyword_idx].get('dep') in modified_relations:
                        token_dependents_2 = dependents.get(word_governor.get('index'))
                        if word_id_in_list(token_dependents_2, keyword_id2):
                            keywords_near_path = True
                            break
                if keywords_near_path:
                    keyword_is_modifier = True
                    break
        if (keyword_on_path or keyword_is_modifier) and not (path is None):
            keyword_near_path = True
            if shortest_path is None:
                shortest_path = path
            elif len(path) < len(shortest_path):
                shortest_path = path
            elif len(path) == len(shortest_path):
            # если длина пути к какому-то другому числу совпадает с
            #уже имеющимся кратчайшим путём, то из них выбирается тот, в котором наименьшая разница
            #между индексами токенов (слов) сущности и числа, т.е. между каким числом меньше всего слов в предложении
                diff_of_index_sp = abs(entity_id - shortest_path[-1].get('index'))
                diff_of_index_p = abs(entity_id - path[-1].get('index'))
                print(shortest_path[-1].get('index'), path[-1].get('index'))
                print(diff_of_index_sp, diff_of_index_p)
                if diff_of_index_p < diff_of_index_sp:
                    shortest_path = path
    if keyword_near_path and not (shortest_path is None):
        return entity_id, keyword_id1, keyword_id2, shortest_path[-1].get('index')
    else:
        return None