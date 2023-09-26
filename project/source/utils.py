import json

def read_data(path):
    with open(path) as file:
        data=json.load(file)
        return data

def get_new_lims(lim_tuple):#problems when diff is very small
    diff=lim_tuple[1]-lim_tuple[0]
    diff=diff/10
    print("DIFFERENZ",diff)
    left_lim=lim_tuple[0]+diff
    right_lim=lim_tuple[1]-diff
    if left_lim>=lim_tuple[0] and right_lim<=lim_tuple[1] and left_lim!=right_lim and left_lim!=lim_tuple[0] and right_lim!=lim_tuple[1]:
        print("LIMS CHANGED", lim_tuple, "to", left_lim, right_lim)
        return left_lim,right_lim
    else:
        print("LIMS COULD NOT BE CHANGED", lim_tuple)
        return (lim_tuple[0], lim_tuple[1])
    
def greater_compare(a,bound):
    return a>bound

def smaller_compare(a,bound):
    return a<bound

def both_bound_compare(a,bound):
    bound=abs(bound)
    return a>-bound and a<bound

def set_compare_function(meaning):
    if meaning=="both":
        return both_bound_compare
    elif meaning=="+":
        return smaller_compare
    elif meaning=="-":
        return greater_compare
    else:
        raise Exception("unknown meaning string", meaning)