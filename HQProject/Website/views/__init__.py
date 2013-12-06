from Transaction import *
from Profile import *
from Inventory import *
from Restock import *
from Store import *
from Sync import *
from Product import *
from Login import *
from decimal import *
from chartit import DataPool, PivotDataPool, Chart, PivotChart
import random
import simplejson

def storename(store_id):
    return store_id