### Food Matcher.v2

--------------------------

This contains a basic technique of mapping products for different food items based on the name and description.

Refer this <https://bergvca.github.io/2017/10/14/super-fast-string-matching.html>



##### Usage

--------------

> python Food_matcher.py --file1 ./data/Fazoli_DoorDash_Austin_78717.csv  --skip1 3  --file2 ./data/Fazoli_Website_Austin_78727.csv --weight 0.8 --divergence_factor 0.33



##### Installation

------------------------

> ```
> pip install -r requirements.txt
> ```
>
> 

for windows if you face any issue with installation of **sparse_dot_topn** use the wheel builds.



##### Roadmap

------------

To improve the algorithm to map the food items over time.



###### Requirements

- certifi==2019.11.28
- Cython==0.29.14
- joblib==0.14.0
- numpy==1.17.4
- pandas==0.25.3
- python-dateutil==2.8.1
- pytz==2019.3
- scikit-learn==0.22
- scipy==1.3.3
- six==1.13.0
- sklearn==0.0
- sparse-dot-topn==0.2.6
- wincertstore==0.2



-------------------------------------

For DB ingestion in JSON format, use Create_store_json.py

#### Create Json

-----------------------

###### Usage

```shell
>>> python Create_store_json.py --store_location_file "C:\Users\DRAGooN\Downloads\converse_now\fazoli data\doordash\Fazoli_DoorDash_Ankeny_50021.csv" --file "C:\Users\DRAGooN\Downloads\converse_now\melian\melian\Food_matcher\DoorDash_vs_Website_Ankeny.csv" --master_loc "master_menu.csv" --output_loc "ankeny.json"
```

##### Requirements

* pandas 
* json