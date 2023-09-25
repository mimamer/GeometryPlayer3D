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