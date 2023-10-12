import random
import json
import numpy

def generate_random(length:int=50, volume_chance:float=0.1, domain:float=numpy.linspace(start=-1,stop=1,num=20), output_file="tmp.json"):
    if volume_chance>1.0 or length<1:
        return
    data=[]
    for i in range(length):
        random_value=random.random()
        if random_value<=volume_chance:
            data.append(generate_random_volume(domain))
        else:
            data.append([generate_random_point(domain)])

    dump_data(data,output_file)

def generate_random_volume(domain):
    if random.random()<0.5:
            return generate_tetrahedra(domain)
    else:
        return generate_cuboid(domain)


def generate_tetrahedra(domain):
    random_point_a=generate_random_point(domain)
    random_point_b=generate_random_point(domain)
    random_point_c=generate_random_point(domain)
    random_point_d=generate_random_point(domain)
    return [[random_point_a,random_point_b],[random_point_a,random_point_c],[random_point_a,random_point_d],
            [random_point_b,random_point_c],[random_point_b,random_point_d],
            [random_point_c,random_point_d]]


def generate_cuboid(domain):
    random_scale=random.random()
    random_shift=domain[random.randrange(0,len(domain),1)]
    data_object=[[-1,-1,-1],[-1,-1,1],[-1,1,-1],[-1,1,1],[1,-1,-1],[1,-1,1],[1,1,-1],[1,1,1]]
    vert_0=[(data_object[0][0])*random_scale+random_shift,(data_object[0][1])*random_scale+random_shift,(data_object[0][2])*random_scale+random_shift]
    vert_1=[(data_object[1][0])*random_scale+random_shift,(data_object[1][1])*random_scale+random_shift,(data_object[1][2])*random_scale+random_shift]
    vert_2=[(data_object[3][0])*random_scale+random_shift,(data_object[3][1])*random_scale+random_shift,(data_object[3][2])*random_scale+random_shift]
    vert_3=[(data_object[2][0])*random_scale+random_shift,(data_object[2][1])*random_scale+random_shift,(data_object[2][2])*random_scale+random_shift]
    vert_4=[(data_object[4][0])*random_scale+random_shift,(data_object[4][1])*random_scale+random_shift,(data_object[4][2])*random_scale+random_shift]
    vert_5=[(data_object[5][0])*random_scale+random_shift,(data_object[5][1])*random_scale+random_shift,(data_object[5][2])*random_scale+random_shift]
    vert_6=[(data_object[7][0])*random_scale+random_shift,(data_object[7][1])*random_scale+random_shift,(data_object[7][2])*random_scale+random_shift]
    vert_7=[(data_object[6][0])*random_scale+random_shift,(data_object[6][1])*random_scale+random_shift,(data_object[6][2])*random_scale+random_shift]

    cuboid=[[vert_0,vert_1],[vert_0,vert_3],[vert_0,vert_4],
                        [vert_1,vert_2],[vert_1,vert_5],
                        [vert_2,vert_3],[vert_2,vert_6],
                        [vert_3,vert_7],
                        [vert_4,vert_5],[vert_4,vert_7],
                        [vert_5,vert_6],
                        [vert_6,vert_7]
                        ]
    return cuboid

def generate_random_point(domain):
    return [domain[random.randrange(0,len(domain),1)],
             domain[random.randrange(0,len(domain),1)],
             domain[random.randrange(0,len(domain),1)]]


def dump_data(data, output_file):
    dictionary={"version":0.1,
                "data":data}
    with open(output_file,"w") as file:
        json.dump(dictionary,fp=file)

generate_random()




