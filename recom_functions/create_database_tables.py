"""
This file creates all recommendation tables in the pgAdmin database
"""

from .connect import connection
from .create_recom_behaviour import collaborativefilter
from .create_recom_price_range import  wipetablepricerange,getpricerange,getcatandpricedata,insertpriceclass
from .recom_aanbiedingen_4_2 import select_combinations,create_new_table,select_data_for_inserts
from .recom_aanbiedingen_4_1 import insert_into_tables
from .recom_aanbiedingen_4_1 import create_new_table as cr_recom_4_1
from .recom_simple_popular import create_new_table as cr_recom_simple
from .recom_simple_popular import insert_different_tables as ins_recom_simple

con, cur = connection('opdracht2_final', 'kip12345')
# Create recom table for behaviour
collaborativefilter(False,con,cur)

# create recom table for similars
wipetablepricerange(con,cur)
pricerange = getpricerange(con,cur)
datapriceclass = getcatandpricedata(pricerange,con,cur)
insertpriceclass(datapriceclass,con,cur)

# Create recom aanbieding 4_2
select_combinations(con,cur)
create_new_table(con,cur)
select_data_for_inserts(con,cur)

# Create recom aanbieding 4_1
cr_recom_4_1(con,cur)
insert_into_tables(con,cur)

# Create recom_simple
cr_recom_simple(con,cur)
ins_recom_simple(con,cur)