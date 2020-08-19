import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import re


def main_check(df):
    # list of unvalid quantities
    print("quantity_validity - Quantity",quantity_validity(df, "Quantity"))
    print("quantity_validity -QtyInPackage",quantity_validity(df, "QtyInPackage"))
    # list of unvalid prices
    print("price_validity (smaller than 0",price_validity(df))
    # all col with same exact field
    #print("isOnePerCol- ChainID",isOnePerCol(df,"ChainID"))
    #print("isOnePerCol- ChainID",isOnePerCol(df,"SubChainID"))
    # all col with digits only
    print("itemOnlyDigits- ChainID",itemOnlyDigits(df, "ChainID"))
    print("itemOnlyDigits - SubChainID",(itemOnlyDigits(df, "SubChainID")))
    print("itemOnlyDigits - StoreId",itemOnlyDigits(df, "StoreID"))
    print("itemOnlyDigits - BikoretNo",itemOnlyDigits(df, "BikoretNo"))
    print("itemOnlyDigits - ItemCode",itemOnlyDigits(df, "ItemCode"))
    print("itemOnlyDigits - ItemType",itemOnlyDigits(df, "ItemType"))
    try:
        print("itemOnlyDigits bIsWeighted ",itemOnlyDigits(df, "BisWeighted"))
    except:
        pass
    try:
        print("itemOnlyDigits - IsGiftItem",itemOnlyDigits(df, "IsGiftItem"))
    except:
        pass
    # all col with numbers only
    print("itemOnlyNumber - Quantity",itemOnlyNumber(df, "Quantity"))
    print("itemOnlyNumber - QtyInPackage",itemOnlyNumber(df, "QtyInPackage"))
    #print("itemOnlyNumber - ItemPrice",itemOnlyNumber(df, "ItemPrice"))
    #print("itemOnlyNumber - UnitOfMeasurePrice",itemOnlyNumber(df,
    # "UnitOfMeasurePrice"))
    print("itemOnlyNumber - AllowDiscount",itemOnlyNumber(df, "AllowDiscount"))
    print("itemOnlyNumber - ItemStatus",itemOnlyNumber(df, "itemStatus"))
    print("itemOnlyNumber - SubChainID",itemOnlyNumber(df, "SubChainID"))
    # try:
    #     print("itemOnlyNumber - RewardType",itemOnlyNumber(df, "RewardType"))
    # except:
    #     print("there's no  RewardType col in file\n ",filename)
    # try:
    #     print("itemOnlyNumber - AllowMultipleDiscounts",itemOnlyNumber(df, "AllowMultipleDiscounts"))
    # except:
    #     print("there's no AllowMultipleDiscounts col in file\n ", filename)

    #print("itemOnlyNumber - PromotionId",itemOnlyNumber(df, "PromotionId"))
    #print("itemOnlyNumber - MinQty",itemOnlyNumber(df, "MinQty"))
    #print("itemOnlyNumber - MaxQty",itemOnlyNumber(df, "MaxQty"))
    #print("itemOnlyNumber - DiscountRate",itemOnlyNumber(df, "DiscountRate"))
    #print("itemOnlyNumber - DiscountType",itemOnlyNumber(df, "DiscountType"))
    #print("itemOnlyNumber - MinPurchaseAmnt",itemOnlyNumber(df, "MinPurchaseAmnt"))
    #print("itemOnlyNumber - DiscountedPrice",itemOnlyNumber(df, "DiscountedPrice"))
    #print("itemOnlyNumber - MinPurchaseAmnt",itemOnlyNumber(df, "MinPurchaseAmnt"))
    #print("itemOnlyNumber - DiscountedPricePerMida",itemOnlyNumber(df, "DiscountedPricePerMida"))

    # all col with letters only
    print("itemOnlyletters - UnitQty",itemOnlyLetters(df,"UnitQty")) # returns a list list of bad items


def price_validity(df):
    """func: applies logic validity test: prices has to be positive"""
    invalid_price = []
    for idx, price in enumerate(df["ItemPrice"]):
        if price < 0:
            invalid_price.append(idx)
    return invalid_price


def quantity_validity(df, col):
    """func: applies logic validity test: quantity must be between (0,
    10,000), because the units are normalized by 10^4 factor (mil or
    kilo)."""
    invalid_quantity = []
    for idx, quant in enumerate(df[col]):
        if not 0 < quant and not quant < 1000:
            invalid_quantity.append(idx)
    return invalid_quantity


def dict_code_name(df):
    """func: saves a dictionary with key=item_code, value =
    item_name.
     useage: barcode check within file and dict for between files"""
    item_dict = dict()
    multi_usage_of_barcode = []
    names = list(df["ItemName"])
    for idx, code in enumerate(df["ItemCode"]):
        if len(str(code)) < 8 :  # longer codes are parsed wrong.
            clean_barcode = code
            if item_dict.get(clean_barcode):
                multi_usage_of_barcode.append(clean_barcode)  # same barcode for
                # different items
            else:
                item_dict[clean_barcode] = names[idx]
    return multi_usage_of_barcode, item_dict


def helper_one_dict_to_all_items(all_items, one_dict):
    """func: checks barcodes between files"""
    all_none_injective = [[],[]]
    for key in one_dict.keys():
        if all_items.get(key,one_dict[key]) != one_dict[key]:
            all_none_injective[0].append(key)
            all_none_injective[1].append(one_dict[key])
        else:
            all_items[key] = one_dict[key]
    return all_items, all_none_injective


def isOnePerCol(df, colName):
    """ return a list of numbers in the given col"""
    colList = list(df[colName])
    num = colList[0]
    numSet = {num}  # all different numbers in given col
    for i in range(len(colList)):
        if colList[i] != num:
            # add to new number to numlist:
            numSet.add(colList[i])
    return list(numSet)


def isNumber(item):
    """
    :param item:given string
    :return: true if item is a number,false otherwise
    note - except spaces between or after number. except floats
    """
    array = re.findall(r'^\s*\d+(\.\d+)*\s*$', item)
    if len(array) == 0:
        return False
    elif len(array)==1:
        return True
    else:
        return False

def itemOnlyNumber(df, colName):
    """
    checks only numbers in given col (can be wrapped with spaces)
    :param df: dataFrame object
    :param colName: given col
    :return: list of bad items
    """
    colList = list(df[colName])
    badItems=[]
    for item in colList:
        if (abs(item-int(item))!=0):
            badItems.append(item)
    return badItems


def itemOnlyDigits(df, colName):
    """
    checks items in given col are gidits only
    :param df: dataFrame object
    :param colName: given col
    :return: list of bad items
    """
    colList = list(df[colName])
    badItems=[]
    for item in colList:
        if type(item)=="float":
            if item<0:
                badItems.append(item)
        elif type(item)=="str":
            if not item.isdigit():
                badItems.append(item)
    return badItems


def onlyLettersOrSpaces(item):
    """
    :param item: string
    :return: true if item is only alphabet and spaces
    """
    array = re.findall(r'^\s*[a-z]+(\s*[a-z]*\s*)*$', item)
    if len(array) == 0:
        return False
    elif len(array)==1:
        return True
    else:
        return False

def itemOnlyLetters(df,colName):
    """
    checks only letters or spaces in given col
    :param df: dataFrame object
    :param colName: given col
    :return: list of bad items
    """
    colList = list(df[colName])
    badItems=[]
    for item in colList:
        lst_str = str(item).split(" ")
        for it in lst_str:
            if it.isdigit():
               return "found: non alphabetic chars in "+colName
    return badItems


def plot_histogram_01(sir):
    """funct: plot for reality check"""
    np.random.seed(1)
    values_A = sir
    values_A_to_plot = [601 if i > 600 else i for i in values_A]
    bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650]
    fig, ax = plt.subplots(figsize=(9, 5))
    _, bins, patches = plt.hist(values_A_to_plot, color="#243380", bins=bins)
    xlabels = np.array(bins, dtype='str')
    xlabels[-1] = '600+'
    N_labels = len(xlabels)
    plt.xticks(50 * np.arange(N_labels))
    ax.set_xticklabels(xlabels)
    plt.title('Reality Check: prices are positive and distributed by '
              'Power-Law')
    plt.setp(patches, linewidth=0)
    plt.legend()
    fig.tight_layout()
    plt.show()
    plt.savefig('my_plot_01.png')
    plt.close()


# ------------- main -------------
if __name__ == '__main__':
    path = r'C:\Users\ASUS\PycharmProjects\HW2\ex2p_305219040\code\converted' # use your path
    all_files = glob.glob(path + "/*.csv")
    li = []

    item_code_name = dict() # once, building a dict of all items' code-names.

    for filename in all_files:
        print(filename)
        df1 = pd.read_csv(filename, index_col=None, header=0)
        print("there are missing values in this file",df1.isnull().values.any())
        # all barcode ,ultiplay useage in same store
        barcode_multi, dict_item = dict_code_name(df1)
        print("are they multiplay barcodes in file: " +str(set(barcode_multi)))

        main_check(df1)  # main checks for invalidity
        li.append(df1)
    # checks for none injective barcodes between files:
    all_items, none_injective = helper_one_dict_to_all_items(item_code_name, dict_item)
    print("none injective: ",none_injective)


    # concats all dataframes to one for ploting:
    df = pd.concat(li, axis=0, ignore_index=True)
    df=df.reset_index()
    priceSeries = df["ItemPrice"].value_counts()

    # plots for exploring the data:
    _= plt.hist(df["ItemPrice"].value_counts(), bins=50)
    plt.title('histogram of prices')
    plt.ylabel('num of items in given price')
    plt.xlabel('item prices')
    plt.show()
    # output plot for final reality check:
    plot_histogram_01(priceSeries)

