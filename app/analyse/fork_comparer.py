def compare_on_files(fork1, fork2):
    """
        Args:
            fork1: ProjectFork
            fork2: ProjectFork
        Return:
            The common degree: intersection / union
            A list contains the common path of the two forks.
    """

    return 1.0 * len(set(fork1.file_list).intersection(set(fork2.file_list))) / len(set(fork1.file_list).union(set(fork2.file_list)))

    """
    common_path = set()
    
    for fork1_file_name in :
        if fork1_file_name in :

    f2_path_list = []
    for fork2_file_name in fork2.file_list:
        fork2_dirs = fork2_file_name.split('/')
        current_path = ""
        for d in fork2_dirs:
            current_path += '/' + d
            f2_path_list.append(current_path)

    for fork1_file_name in fork1.file_list:
        fork1_dirs = fork1_file_name.split('/')
        current_path = ""
        deepest_common_path = ""
        for d in fork1_dirs:
            current_path += '/' + d
            if current_path in f2_path_list:
                deepest_common_path = current_path
        if deepest_common_path:
            common_path.add(deepest_common_path)

    return list(common_path)
    """


def compare_on_key_words(fork1, fork2):
    """
        Args:
            fork1: ProjectFork
            fork2: ProjectFork
        Return:
            Number of common key words of the two forks.       
    """
    return len(set(fork1.key_words).intersection(set(fork2.key_words)))


def get_similar_fork(fork_list, fork1):
    """
        Args:
            fork_list
            fork1
        Return:
            A list contains the similar forks with fork1 (Top 5)    
    """
    if (fork_list is None) or (fork1 is None):
        return None
    
    sort_list = {}
    param_list = {}
    for fork2 in fork_list:
        if fork2.full_name == fork1.full_name:
            continue
        if (fork2.total_changed_file_number is None) or (fork2.total_changed_file_number == 0):
            continue

        value_common_words = compare_on_key_words(fork1, fork2)
        value_common_files = compare_on_files(fork1, fork2)

        # print(n_common_words, n_dep_commpn_files)
        param_list[fork2.fork_name] = [value_common_words, value_common_files]

    norm_list = None
    param_number = 0
    for fork in param_list:
        if norm_list is None:
            norm_list = [[x,x] for x in param_list[fork]]
            param_number = len(norm_list)
        else:
            for i in range(param_number):
                norm_list[i][0] = min(norm_list[i][0], param_list[fork][i])
                norm_list[i][1] = max(norm_list[i][1], param_list[fork][i])

    for fork in param_list:
        value = []
        for i in range(param_number):
            value.append(1.0 * (param_list[fork][i] - norm_list[i][0]) / (norm_list[i][1] - norm_list[i][0] + 1))
        sort_list[fork] = value[0] + value[1] * 3
    result = [(x,y) for x, y in sorted(sort_list.items(), key=lambda x: x[1], reverse=True)]
    result = [(x,y) for x, y in filter(lambda x: x[1] > 0, result)]
    return result[:5]

