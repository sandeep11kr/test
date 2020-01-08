import pandas as pd, numpy as np, re, sparse_dot_topn.sparse_dot_topn as ct, time
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import math
import argparse, sys
import warnings
warnings.filterwarnings("ignore")


def ngrams(string, n=3):
    string = (re.sub(r'[,-./]|\sBD',r'', string)).upper()
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

def awesome_cossim_top(A, B, ntop, lower_bound=0):
  # force A and B as a CSR matrix.
  # If they have already been CSR, there is no overhead
  A = A.tocsr()
  B = B.tocsr()
  M, _ = A.shape
  _, N = B.shape

  idx_dtype = np.int32

  nnz_max = M * ntop

  indptr = np.zeros(M + 1, dtype=idx_dtype)
  indices = np.zeros(nnz_max, dtype=idx_dtype)
  data = np.zeros(nnz_max, dtype=A.dtype)

  ct.sparse_dot_topn(
      M, N, np.asarray(A.indptr, dtype=idx_dtype),
      np.asarray(A.indices, dtype=idx_dtype),
      A.data,
      np.asarray(B.indptr, dtype=idx_dtype),
      np.asarray(B.indices, dtype=idx_dtype),
      B.data,
      ntop,
      lower_bound,
      indptr, indices, data)
  return csr_matrix((data, indices, indptr), shape=(M, N))

def get_matches_df(sparse_matrix, A, B, textA, textB, top=100, treshold = 0.89):
  output = pd.DataFrame()
  like_df =  pd.DataFrame()
  print("A: ", A.columns)
  print("B: ", B.columns)
  colsA = list(A.columns)
  colsB = list(B.columns)
  non_zeros = sparse_matrix.nonzero()
  sparserows = non_zeros[0]
  sparsecols = non_zeros[1]
  print("\n\n Creating match df :")
  if top:
      nr_matches = top
  else:
      nr_matches = sparsecols.size
  left_side = np.empty([nr_matches, len(colsA)], dtype=object)
  not_matched_left = np.empty([nr_matches, len(colsA)], dtype=object)
  right_side = np.empty([nr_matches, len(colsB)], dtype=object)
  similarity = np.zeros(nr_matches)
  not_matched_filtered =  np.zeros(nr_matches)
  for index in range(0, nr_matches):
    for i in range(0, len(colsA) if (len(colsA)>len(colsB)) else len(colsB)):
      if (i<len(colsA)):
        left_side[index][i] = A[colsA[i]][sparserows[index]]
        if sparse_matrix.data[index]<=treshold:
          not_matched_left[index][i] = A[colsA[i]][sparserows[index]]
      if (i<len(colsB)):
        right_side[index][i] = B[colsB[i]][sparsecols[index]]
    similarity[index] = sparse_matrix.data[index]
    if sparse_matrix.data[index]<=treshold:
      # print(sparse_matrix.data[index])
      not_matched_filtered[index] = sparse_matrix.data[index]
  print('np array created')
  for i in range(0, len(colsA) if (len(colsA)>len(colsB)) else len(colsB)):
    if (i<len(colsA)):
      output[textA+'_'+colsA[i]] = left_side[:,i]
      like_df[colsA[i]] = not_matched_left[:,i]
    if (i<len(colsB)):
      output[textB+'_'+colsB[i]] = right_side[:,i]
  output['similarity'] = similarity
  print("printing output", output)
  like_df['similarity_1st'] =  not_matched_filtered
  return output, like_df.dropna(thresh=3).reset_index()

def bucketizer(df, rangeA, rangeB, column_name):
    print(rangeA," : " , rangeB," : ", len(df[(df[column_name]>=rangeA) & (df[column_name]<=rangeB)]))
    return df[(df[column_name]>=rangeA) & (df[column_name]<=rangeB)].reset_index(drop=True)

def get_ranges(df1, df2, column1, column2, no_buckets = 10, compare_range = 0.33):
    df1[column1] = df1[column1].astype('str').str.extract("([0-9]+\.?([0-9]+)?)").fillna(0).astype('float')
    df1 = df1.sort_values(column1)
    df2[column2] = df2[column2].astype('str').str.extract("([0-9]+\.?([0-9]+)?)").fillna(0).astype('float')
    df2 = df2.sort_values(column2)
    combined = list(set(list(df1[column1])+list(df2[column2])))
    combined.sort()
    bucketA = []
    bucketB = []
    c_i = math.ceil(max(combined)/no_buckets)
    for i in range(no_buckets):
        if i==0:
          bucketA.append((0.1, c_i))
          bucketB.append((0.0, c_i*(1+compare_range)))
        else:
          bucketA.append(((i* c_i), ((i+1)* c_i)))
          bucketB.append((c_i*(i-compare_range), c_i*(i+(1+compare_range))))
    return bucketA, bucketB

def match_name_desc(df_dirty, df_clean, args, df_dirty_1, df_clean_1,df_dirty_0, df_clean_0, weight):
    matches_df = pd.DataFrame()
    #name run
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
    tf_idf_matrix_clean = vectorizer.fit_transform(df_clean['name'])
    tf_idf_matrix_dirty = vectorizer.transform(df_dirty['name'])

    t1 = time.time()
    matches = awesome_cossim_top(tf_idf_matrix_dirty, tf_idf_matrix_clean.transpose(), 1, 0)
    
    t = time.time()-t1
    print("1st run SELF TIMED (Names):", t)
    print(str(args.file1), re.search("^([A-Za-z]+)_([A-Za-z]+)_([A-Za-z]+)", str(args.file1)))
    m = re.search("([A-Za-z]+)_([A-Za-z]+)_([A-Za-z]+)", str(args.file1))
    n = re.search("([A-Za-z]+)_([A-Za-z]+)_([A-Za-z]+)", str(args.file2))
    textA = m.group(2)#'DoorDash'
    textB = n.group(2)#'Fazoli'
    matches_df1, not_exact_df = get_matches_df(matches, df_dirty_0, df_clean_0, textA, textB,  top=0)
    matched_names, not_exact_df = get_matches_df(matches, df_dirty_1, df_clean_1, textA, textB,  top=0)
    print(matched_names)
    #desc run
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
    tf_idf_matrix_clean = vectorizer.fit_transform(df_clean['description'].fillna(df_clean['name']))
    tf_idf_matrix_dirty = vectorizer.transform(df_dirty['description'].fillna(df_dirty['name']))
    t1 = time.time()
    matches = awesome_cossim_top(tf_idf_matrix_dirty, tf_idf_matrix_clean.transpose(), 1, 0)
    t = time.time()-t1
    print("2nd run SELF TIMED (Description):", t)
    matches_df2, not_exact_df = get_matches_df(matches, df_dirty, df_clean, textA, textB,  top=0)
    matched_desc, not_exact_df = get_matches_df(matches, df_dirty_1, df_clean_1, textA, textB,  top=0)
    #matches_df2 = matches_df2.reindex(sorted(matches_df.columns), axis=1)

    #Comparing the matches using name and description and stitching it together
    for i in range(len(matches_df1)):
      row_df1 = matches_df1.iloc[i]
      row_df2 = matches_df2.iloc[i]
      row_name = matched_names.iloc[i]
      row_desc = matched_desc.iloc[i]
      #if names are similar, pass
      if row_df1['similarity']>=0.99:
        matches_df = matches_df.append(row_name)
      else:
        if row_df1[textA +'_name']==row_df2[textA +'_name']:
          if row_df1[textB +'_name']==row_df2[textB +'_name']:
            row_name['similarity'] = weight * row_df1['similarity'] + (1-weight)*row_df2['similarity']
            matches_df = matches_df.append(row_name)
          else:
            if row_name['similarity']>=row_desc['similarity']:
              row_name['similarity'] = weight * row_name['similarity']
              matches_df = matches_df.append(row_name)
            else:
              row_desc['similarity'] = (1-weight) * row_desc['similarity']
              matches_df = matches_df.append(row_desc)
    return matches_df, textA, textB

if __name__ == "__main__":
    # initiate the parser
    parser = argparse.ArgumentParser()

    # add long and short argument
    parser.add_argument("--file1", "-f", help="location of the file 1 eg. Doordash")
    parser.add_argument("--file2", "-F", help="location of the file 2 eg. Fazoli website")
    parser.add_argument("--weight", "-n", help="weight for name for similarity")
    parser.add_argument("--skip1", "-s", help= 'number of rows/lines to skip from file1. eg. 0')
    parser.add_argument("--skip2", "-S", help= 'number of rows/lines to skip from file2. eg. 0')
    parser.add_argument("--divergence_factor", "-d", help= 'range for comparing')
    # parser.add_argument("--weight_desc", "-n", help="weight for weight_desc")
    # read arguments from the command line
    args = parser.parse_args()

    ## Parameters
    no_price_buckets = 10
    
    weight = 0.8
    # threshold  = 0.77
    
    if args.weight:
        print('weight: ', args.weight, type(args.weight))
        weight = float(args.weight)
    if args.skip1==None:
        args.skip1 = 3
    if args.skip2==None:
        args.skip2 = 0
    if args.divergence_factor==None:
        args.divergence_factor = 0.33
    compare_price_range = float(str(args.divergence_factor))
    matches_df = pd.DataFrame()
    # check for --files
    if args.file1 and args.file2:
        print(args.file1,args.file2)
        df_dirty = pd.read_csv(str(args.file1), skiprows=int(args.skip1), encoding = "ISO-8859-1")
        df_dirty.columns = map(str.lower, df_dirty.columns)
        df_dirty['price'] = df_dirty['price'].astype('str').str.\
                            extract("([0-9]+\.?([0-9]+)?)").fillna(0).astype('float')
        df_dirty = df_dirty.sort_values("price").reset_index(drop=True)
        df_dirty_1 = df_dirty.copy()
        #{"name":["half dozen bread sticks","buns","berger","fettuccine","ceasar","abbasasdfzz","zsdfzl"]}
        # '/content/Fazoli_DoorDash_Austin_78717.csv'
        df_clean = pd.read_csv(str(args.file2), skiprows=int(args.skip2))
        df_clean.columns = map(str.lower, df_clean.columns)
        df_clean['price'] = df_clean['price'].astype('str').str.\
                            extract("([0-9]+\.?([0-9]+)?)").fillna(0).astype('float')
        df_clean = df_clean.sort_values("price").reset_index(drop=True)
        df_clean_1 = df_clean.copy()
        # /content/fazoli_austin_78727.csv
        #{"name":["half fries sticks","bing","bums","faccunie", 'cesar']}
        m = re.search("([A-Za-z]+)_([A-Za-z]+)_([A-Za-z]+)", str(args.file1))
        n = re.search("([A-Za-z]+)_([A-Za-z]+)_([A-Za-z]+)", str(args.file2))
        textA = m.group(2)#'DoorDash'
        textB = n.group(2)#'Fazoli'
        print('Successfully Loaded!')
        # Preprocessing
        df_clean.columns = map(str.lower, df_clean.columns)
        df_dirty.columns = map(str.lower, df_dirty.columns)
        df_dirty["price"] = df_dirty["price"].fillna(0).astype('float')

        df_clean['description'] = df_clean['description'].fillna(df_clean['name'])
        df_dirty['description'] = df_dirty['description'].fillna(df_dirty['name'])
        #name
        df_dirty['name'] = df_dirty['name'].\
            str.replace(r'^[0-9]+\. ', '').\
            str.replace(r'[^a-zA-Z0-9]', ' ').\
            str.lower()
        df_clean['name'] = df_clean['name'].\
            str.replace(r'[^a-zA-Z0-9]', ' ').\
            str.lower()
        #creating a copy
        df_dirty_0 = df_dirty.copy()
        df_clean_0 = df_clean.copy()

        #description
        df_dirty['description'] = df_dirty['description'].\
            str.replace(r'[^a-zA-Z0-9]', ' ', regex=True).\
            str.replace(r'\(|\)|\[|\]', ' ', regex=True).\
            str.replace(r'^[ ]*\d{1,2}[ ]*$', ' ', regex=True).\
            str.lower().\
            str.strip()
        df_dirty['description'] = df_dirty.apply(lambda x:str(x['description']).\
            replace('',  x['name']) if len(str(x['description']))==0 else str(x['description']),
            axis=1)
        
        df_clean['description'] = df_clean['description'].\
            str.replace(r'[^a-zA-Z]', ' ').\
            str.lower()
        df_clean['description'] = df_clean.apply(lambda x:str(x['description']).\
            replace('',  x['name']) if len(str(x['description']))==0 else str(x['description']),
            axis=1)
        # creates price buckets
        bucketA, bucketB = get_ranges(df_dirty, df_clean, "price", "price",
                                    no_buckets = no_price_buckets, compare_range = compare_price_range)
        
        for i in range(-1, no_price_buckets):
            matches_df_temp = pd.DataFrame()
            print(bucketizer(df_dirty, bucketA[i][0], bucketA[i][1], 'price')[["name", "description"]])
            # -1 is the condition where list 1 has no price for filtering
            if i==-1 and len(df_dirty[df_dirty['price']==0])>0:
                matches_df_temp, textA, textB = match_name_desc(df_dirty[df_dirty['price']==0].reset_index(drop=True),
                                        df_clean, args, df_dirty_1[df_dirty['price']==0].reset_index(drop=True), 
                                        df_clean_1, df_dirty_0[df_dirty['price']==0].reset_index(drop=True),
                                        df_clean_0, weight)
            
            # when list 2 has no price
            elif len(bucketizer(df_dirty, bucketA[i][0], bucketA[i][1], 'price'))>0 and len(df_clean[df_clean['price']==0])==0:
                matches_df_temp, textA, textB = match_name_desc(bucketizer(df_dirty, bucketA[i][0], bucketA[i][1], 'price'),
                                        bucketizer(df_clean, bucketB[i][0], bucketB[i][1], 'price'), args, bucketizer(df_dirty_1, bucketA[i][0], bucketA[i][1], 'price'), 
                                        bucketizer(df_clean_1, bucketB[i][0], bucketB[i][1], 'price'), bucketizer(df_dirty_0, bucketA[i][0], bucketA[i][1], 'price'),
                                        bucketizer(df_clean_0, bucketB[i][0], bucketB[i][1], 'price'), weight)
            
            elif len(bucketizer(df_dirty, bucketA[i][0], bucketA[i][1], 'price'))>0 and len(df_clean[df_clean['price']==0])>0:
                df_clean_0_temp = pd.DataFrame()
                df_clean_1_temp = pd.DataFrame()
                df_clean_temp = pd.DataFrame()
                #print("------\n Dirty :\n-------\n", bucketizer(df_dirty, bucketA[i][0], bucketA[i][1], 'price'))
                df_clean_temp = df_clean_temp.append(bucketizer(df_clean, bucketB[i][0], bucketB[i][1], 'price'))
                df_clean_temp = df_clean_temp.append(df_clean[df_clean['price']==0])
                df_clean_1_temp = df_clean_1_temp.append(bucketizer(df_clean_1, bucketB[i][0], bucketB[i][1], 'price'))
                df_clean_1_temp = df_clean_1_temp.append(df_clean_1[df_clean_1['price']==0])
                df_clean_0_temp = df_clean_0_temp.append(bucketizer(df_clean_0, bucketB[i][0], bucketB[i][1], 'price'))
                df_clean_0_temp = df_clean_0_temp.append(df_clean_0[df_clean_0['price']==0])
                #print("------\nClean :\n-------\n", df_clean_0_temp, df_clean_1_temp, df_clean_temp)
                matches_df_temp, textA, textB = match_name_desc(bucketizer(df_dirty, bucketA[i][0], bucketA[i][1], 'price'),
                    df_clean_temp.reset_index(drop=True), args, bucketizer(df_dirty_1, bucketA[i][0], bucketA[i][1], 'price'), 
                    df_clean_1_temp.reset_index(drop=True), bucketizer(df_dirty_0, bucketA[i][0], bucketA[i][1], 'price'),
                    df_clean_0_temp.reset_index(drop=True), weight)
            else:
                pass
            matches_df = matches_df.append(matches_df_temp)
            print(i)
        #print(list(df_dirty['description']), "\n\n\n", list(df_clean['description']))
        matches_df.to_csv(textA + '_vs_' + textB +'_'+m.group(3) +'.csv', index = False)
        print('successfully written!')
    
    else:
        print('#### Please enter the file names appropriately!! ####')
