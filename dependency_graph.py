class DependencyGraph():
    def __init__(self,tokens,dependencies,lang="ru"):
        self.__sentence_tokens = tokens
        self.__sent_dependents = dict()
        self.__sent_governors = dict()
        self.__lang = lang
        for dep in dependencies:  # add ROOT node
            if dep.get('dep') == "ROOT":
                # self.__sent_dependents[dep.get('governor')] = [{dep.get('dependent'): dep.get('dep')}]
                self.__sent_dependents[dep.get('governor')] = [{'index': dep.get('dependent'), 'dep': dep.get('dep')}]
                self.__sent_governors[dep.get('dependent')] = {'index': dep.get('governor'), 'dep': dep.get('dep')}
                break
        for token in self.__sentence_tokens:  # add token`s nodes
            token_deps = []
            token_index = token.get('index')
            for dep in dependencies:
                if token_index == dep.get('governor'):
                    # token_deps.append({dep.get('dependent'): dep.get('dep')})
                    token_deps.append({'index': dep.get('dependent'), 'dep': dep.get('dep')})
                if token_index == dep.get('dependent'):
                    self.__sent_governors[token_index] = {'index': dep.get('governor'), 'dep': dep.get('dep')}
            self.__sent_dependents[token_index] = token_deps

    @property
    def lang(self):
        return self.__lang
    @lang.setter
    def lang(self,lang):
        self.__lang = lang

    @property
    def tokens(self):
        return self.__sentence_tokens

    @property
    def dependencies(self):
        return self.__sent_dependents

    @property
    def governors(self):
        return self.__sent_governors

    def __str__(self):
        sent_str = ""
        for token in self.__sentence_tokens:
            # print(token.get('index'), token.get('word'), token.get('pos') in preps)
            if self.lang == "ru":
                is_prep = token.get('pos') == "PUNCT"
            if self.lang == "en":
                is_prep = token.get('pos') == set(",.?!:;)]}|*\"`'\\/")
            is_1 = token.get('index') == 1
            if (is_prep or not is_1) and (not is_prep or is_1):
                sent_str += " "
            sent_str += token.get('originalText')
        return sent_str

    def path_to_root(self, start):
        print(start)
        path = []
        root = False
        if start < 0:
            return path
        if not self.__governors_tree.get(start) is None:
            while not root:
                if len(path) < 1:
                    path.append({start: "none"})
                    print("add first")
                else:
                    if not self.__governors_tree.get(start) is None:
                        if start == 0:
                            root = True
                        else:
                            next_node = self.__governors_tree.get(start).get('index')
                            if next_node > 0:
                                path.append(self.__governors_tree.get(start))
                            start = next_node
                    else:
                        break
        return path

    def shortest_tree_path(self, start, end):
        path_start_root, path_end_root = [], []
        if type(start) == type(""):
            start = int(start)
        if type(end) == type(""):
            end = int(end)
        path_start_root = self.path_to_root(start)
        # print(path_start_root)
        path_end_root = self.path_to_root(end)
        # print(path_end_root)
        if len(path_start_root) < 2 and len(path_end_root) < 2:
            return None
        if len(path_start_root) == 1:
            path_end_root.reverse()
            # path_start_root.extend(path_end_root)
            return path_end_root
        if len(path_end_root) == 1:
            # path_start_root.extend(path_end_root)
            return path_start_root
        join_start, join_end, first_join_word = 0, 0, False
        start_root_len, end_root_len = len(path_start_root), len(path_end_root)
        min_path_len = min(start_root_len, end_root_len)
        len_diff_start, len_diff_end = start_root_len - end_root_len, 0
        if len_diff_start < 0:
            len_diff_end = -len_diff_start
            len_diff_start = 0
        for i in reversed(range(min_path_len)):
            if path_start_root[i + len_diff_start].get('index') != path_end_root[i + len_diff_end].get('index'):
                join_start += 1
                break
            else:
                join_start = i + len_diff_start
                join_end = i + len_diff_end
        if join_start == 0 and join_end == 0:
            return None
        elif join_start == 0:
            del path_end_root[join_end:end_root_len]
        elif join_end == 0:
            del path_start_root[join_start:start_root_len]
        else:
            del path_start_root[join_start:start_root_len]
            del path_end_root[join_end:end_root_len]
        path_end_root.reverse()
        # print(path_start_root,type(path_start_root),len(path_start_root))
        # print(path_end_root,type(path_end_root),len(path_end_root))
        path_start_root.extend(path_end_root)
        # print(path_start_root)
        return path_start_root

if __name__ == "__main__":
    print("Class \"Graph of tokens and dependencies of sentence\"")