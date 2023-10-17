from __future__ import annotations

class Limit():

    def __init__(self):
        self._min_lim=None
        self._max_lim=None

    def reset(self):
        self._min_lim=None
        self._max_lim=None

    def correct_limits_lists(self,xs:list,ys:list,zs:list):
        self._min_lim=compare_and_get(self._min_lim,xs,ys,zs,greater)
        self._max_lim=compare_and_get(self._max_lim,xs,ys,zs,less)
    
    def correct_limits_dictionary(self,dictionary:dict):
        self._min_lim=compare_and_get(self._min_lim,[dictionary["min_lim"][0]],[dictionary["min_lim"][1]],[dictionary["min_lim"][2]],greater)
        self._max_lim=compare_and_get(self._max_lim,[dictionary["max_lim"][0]],[dictionary["max_lim"][1]],[dictionary["max_lim"][2]],less)

    def correct_limits_limit(self, limit:Limit):
        min_lim=limit.get_min()
        max_lim=limit.get_max()
        if min_lim is None or max_lim is None:
            return
        self._min_lim=compare_and_get(self._min_lim,[min_lim[0]],[min_lim[1]],[min_lim[2]],greater)
        self._max_lim=compare_and_get(self._max_lim,[max_lim[0]],[max_lim[1]],[max_lim[2]],less)

    def get_min(self):
        return self._min_lim
    
    def get_max(self):
        return self._max_lim


def compare_and_get(ref,xs,ys,zs,comparator):#comparator -> change if less for example
    for i in range(len(xs)):
        if ref is None:
            ref=[xs[i],ys[i],zs[i]]
        if comparator(ref[0] , xs[i]):
            ref[0]=xs[i]
        if comparator(ref[1] , ys[i]):
            ref[1]=ys[i]
        if comparator(ref[2] , zs[i]):
            ref[2]=zs[i]
    return ref

def less(a,b):
    return a<b

def greater(a,b):
    return a>b
