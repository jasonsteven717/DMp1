# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 21:18:26 2019

@author: TsungYuan
"""
import csv 
import time
def load_data(file):
      data_set = []
      i = 0
      with open(file, newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if i == 0: 
                i+=1 
                continue
            data_set.append(row)
      return data_set
 
def is_apriori(Ck_item, Lksub1):
      for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
          return False
      return True
 
def create_Ck(Lksub1, k):
      Ck = set()
      len_Lksub1 = len(Lksub1)
      list_Lksub1 = list(Lksub1)
      for i in range(len_Lksub1):
        for j in range(1, len_Lksub1):
          l1 = list(list_Lksub1[i])
          l2 = list(list_Lksub1[j])
          l1.sort()
          l2.sort()
          if l1[0:k-2] == l2[0:k-2]:
            Ck_item = list_Lksub1[i] | list_Lksub1[j]
            if is_apriori(Ck_item, Lksub1):
              Ck.add(Ck_item)
      return Ck
 
def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
      Lk = set()
      item_count = {}
      for t in data_set:
        for item in Ck:
          if item.issubset(t):
            if item not in item_count:
              item_count[item] = 1
            else:
              item_count[item] += 1
      t_num = float(len(data_set))
      for item in item_count:
        if (item_count[item] / t_num) >= min_support:
          Lk.add(item)
          support_data[item] = item_count[item] / t_num
      return Lk
 
def generate_L(data_set, min_support):
      support_data = {}
      C1 = set()
      for t in data_set:
        for item in t:
          item_set = frozenset([item])
          C1.add(item_set)
      L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
      Lksub1 = L1.copy()
      L = []
      L.append(Lksub1)
      i= 0
      while True:
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        if Li == set():
            break
        Lksub1 = Li.copy()
        L.append(Lksub1)
        i+=1
      return L, support_data
 
def generate_rules(L, support_data, min_conf):
      big_rule_list = []
      sub_set_list = []
      for i in range(0, len(L)):
        for freq_set in L[i]:
          for sub_set in sub_set_list:
            if sub_set.issubset(freq_set):
              conf = support_data[freq_set] / support_data[freq_set - sub_set]
              big_rule = (freq_set - sub_set, sub_set, conf)
              if conf >= min_conf and big_rule not in big_rule_list:
                big_rule_list.append(big_rule)
          sub_set_list.append(freq_set)
      return big_rule_list

if __name__ == "__main__":
    start = time.clock()
    data_set = load_data('adult.csv')
    L, support_data = generate_L(data_set,min_support=0.2)
    big_rules_list = generate_rules(L, support_data, min_conf=0.9)
    end = time.clock()
    for Lk in L:
        print ("-"*50)
        print (str(len(list(Lk)[0])) + "-itemsets")
        for freq_set in Lk:
            print (freq_set,"\nsupport : " ,support_data[freq_set])
    print ("-"*50)
    print(len(big_rules_list),"rules")
    for item in big_rules_list:
        print (item[0], "=>", item[1], "conf: ", item[2])
    print("time cost : ",end-start)