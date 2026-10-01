def group_anagrams(words: list[str]) -> list[list[str]]:
    groups = {}
    
    for word in words:
        key = "".join(sorted(word)) # у анаграмм после сортировки получается одинаковый ключ
        
        if key not in groups:
            groups[key] = []
            
        groups[key].append(word)
    
    # сортируем слова внутри каждой готовой группы (не уверена, что надо, но в примере так)    
    for group in groups.values():
        group.sort()
        
    return sorted(groups.values(), key=len)
