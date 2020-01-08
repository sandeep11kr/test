import re
import pandas as pd

class Extractor:
    
    def __init__(self, attrib_df,ingridients ):
        self.df = attrib_df
        self.ingridients = ingridients
        #print(attrib_df.columns)

    def generate_ngrams(self, s, n=2):
        # Convert to lowercases
        s = s.lower()
        # # Break sentence in the token, remove empty tokens
        tokens = [token for token in s.split() if token != ""]
        # Use the zip function to help us generate n-grams
        # Concatentate the tokens into ngrams and return
        ngrams = zip(*[tokens[i:] for i in range(n)])
        return [" ".join(ngram) for ngram in ngrams]

    def common_member(self, a, b):
        # returns common members of a and b list
        a_set = set(a)
        b_set = set(b)
        #print(a_set, b_set)
        if (a_set & b_set): 
            
            return list(a_set & b_set) 
        else: 
            #print("No common elements")
            return -1

    def get_item_type(self, input_str):
        # returns items name if found else possible product attributs
        a = input_str.split()
        items = list(set(self.df['Item'].values))
        item = list(set(self.df['Item_mod'].values))
        item.extend(items)
        i = self.common_member(a,list(set(item)))
        j = []
        attributes = {}
        if i ==-1:
            common_attribs = self.common_member(a, list(self.df['Values_mod'].values))
            if common_attribs!=-1:
                print(j)
                print(common_attribs)
                for k in common_attribs:
                    print("\t"+str(k))
                    attributes[str(k)] = self.df[(self.df['Values_mod']==k)]['Attribute'].values[0]
        return i, attributes

    def get_attributes(self, input_str, items, attry):
        # returns attributes for a particutar items identified
        a = input_str.split()
        b = self.generate_ngrams(input_str, 2)
        c = self.generate_ngrams(input_str, 3)
        a = a+b+c
        attrib_dict = attry
        #print(common_members, '\n')
        for i in items:
            common_members =  self.common_member(a, filter(lambda x: x != '', list(self.df[(self.df['Item']==i) | (self.df['Item_mod']==i)]['Values_mod'])))
            #print("common_members",common_members)
            if common_members!=-1:
                for j in common_members:
                    attrib_dict[j] = self.df[((self.df['Item']==i) | (self.df['Item_mod']==i))& (self.df['Values_mod']==j)]['Attribute'].values[0]
            else:
                pass
        common_members =  self.common_member(a, list(self.ingridients['Item_mod']))
        if common_members!=-1:
            attrib_dict['ingridients'] = common_members
        #print(attrib_dict, '\n')
        return attrib_dict

    def process_input(self, input_str):
        # processes the imput string
        input_str = str(input_str).lower()
        input_str  = re.sub(r"\.|\(|\)|\||\[|\]|\$|,|<|>|=", " ", input_str)
        items, attributes = self.get_item_type(input_str)
        #print(items)
        if items ==-1:
            print('No such item found')
            items = "Unkown"
        #else:
        attributes = self.get_attributes(input_str, items, attributes)
        #print(*items)
        attributes['items'] = items
        #print(attributes)
        return attributes