# %%
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import ast

def safe_eval(val):
    if pd.isna(val):  # Check for NaN
        return val
    try:
        return ast.literal_eval(val)
    except ValueError:
        return val

def cleanColumn(column):
    # Eliminar les categories que apareixen menys d'un 5% de les vegades
    value_counts = column.value_counts()
    threshold = value_counts.max() * 0.05
    to_replace = value_counts[value_counts < threshold].index
    return column.replace(to_replace, 'Others')




# Map the 'ImageData.style.stories.summary.label' column to numeric values
story_mapping = {
    '1_story': 1,
    '1.5_stories': 1.5,
    '2_stories': 2,
    '2.5_stories': 2.5,
    '3_stories_or_more': 3
}


def mastegar(data, file_name):
        # print(data['ImageData.style.stories.summary.label'].unique())
    data['ImageData.style.stories.summary.label'] = data['ImageData.style.stories.summary.label'].map(story_mapping)
    print(data['ImageData.style.stories.summary.label'].unique())

    # %%
    data['Structure.YearBuilt'].unique()

    # %%
    # # replace edge case 
    # data['Structure.YearBuilt'] = data['Structure.YearBuilt'].replace(190., np.nan)

    # # convert 0 to nan on Structure.YearBuilt to remove 0 values
    # data['Structure.YearBuilt'] = data['Structure.YearBuilt'].replace(0, np.nan)


    # %%
    #data segmentation
    columnes_numeriques = data.select_dtypes(include=['number'])  # Selecciona columnes numèriques
    # add ListingId to the numeric columns
    columnes_numeriques = pd.concat([data['Listing.ListingId'], columnes_numeriques], axis=1)

    columnes_categoriques = data.select_dtypes(exclude=['number'])  # Selecciona columnes no numèriques (categòriques)


    # %%

    # Treballar amb cada columna numèrica una a una
    for columna in columnes_numeriques.columns:
        if(columna in ['Listing.ListingId']): continue
        # Calcular Q1, Q3 i IQR per a la columna actual (ignorant els NaN)
        Q1 = columnes_numeriques[columna].quantile(0.1)
        Q3 = columnes_numeriques[columna].quantile(0.9)
        IQR = Q3 - Q1
        
        # Límits per identificar outliers
        lower_bound = Q1 - 2 * IQR
        upper_bound = Q3 + 2 * IQR
        
        # Filtrar files dins dels límits, mantenint files amb NaN
        mask = (columnes_numeriques[columna].isna()) | \
            ((columnes_numeriques[columna] >= lower_bound) & (columnes_numeriques[columna] <= upper_bound))
        
        columnes_numeriques = columnes_numeriques[mask]

    columnes_numeriques

    # %%
    # canviar els NaN per la mitjana de la columna
    columnes_numeriques = columnes_numeriques.apply(lambda col: col.fillna(col.mean(skipna=True)) if col.dtype in ['float64', 'int64'] else col)
    columnes_numeriques

    # %%
    # normalize all numeric columns except ListingId and ClosePrice
    # scaler = MinMaxScaler()
    # columnes_numeriques = pd.DataFrame(scaler.fit_transform(columnes_numeriques), columns=columnes_numeriques.columns)
    # columnes_numeriques

    # %%
    columnes_categoriques

    # %%
    # for every column see how many unique values it has and its count
    for col in columnes_categoriques.columns:
        print(columnes_categoriques[col].value_counts())
        print()

    # %% [markdown]
    # INUTILS o REDUNDANTS -> BORRAR

    # %%
    # some fine tuning
    # drop columns with too many unique values
    # drop Listing.ListingId
    columnes_categoriques = columnes_categoriques.drop('Listing.ListingId', axis=1)

    # drop postalcodeplus4
    columnes_categoriques = columnes_categoriques.drop('Location.Address.PostalCodePlus4', axis=1)

    # drop location number Location.Address.StreetNumber
    # numero independent del preu
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StreetNumber', axis=1)

    # DROP Location.Address.StateOrProvince
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StateOrProvince', axis=1)

    # DROP Location.Address.UnparsedAddress
    columnes_categoriques = columnes_categoriques.drop('Location.Address.UnparsedAddress', axis=1)

    # DROP Location.Address.StreetDirectionSuffix
    # nombre d'ocurrencies no es prou gran per cada categoria
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StreetDirectionSuffix', axis=1)

    # DROP UnitNumber
    # nombre d'ocurrencies no es prou gran per cada categoria
    columnes_categoriques = columnes_categoriques.drop('Location.Address.UnitNumber', axis=1)

    # DROP Location.Address.StreetSuffix
    # no es rellevant
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StreetSuffix', axis=1)

    #drop Location.Address.StreetDirectionPrefix
    # no es rellevant
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StreetDirectionPrefix', axis=1)

    # DROP Location.Address.StreetName
    # nombre d'ocurrencies no es prou gran per cada categoria
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StreetName', axis=1)

    # DROP Location.Area.SubdivisionName
    # no es rellevant
    columnes_categoriques = columnes_categoriques.drop('Location.Area.SubdivisionName', axis=1)

    # DROP Location.School.HighSchoolDistrict
    # no es rellevant
    columnes_categoriques = columnes_categoriques.drop('Location.School.HighSchoolDistrict', axis=1)

    #DRop postalcode
    # no es rellevant
    columnes_categoriques = columnes_categoriques.drop('Location.Address.PostalCode', axis=1)

    columnes_categoriques = columnes_categoriques.drop('Location.Address.City', axis=1)
    columnes_categoriques = columnes_categoriques.drop('Location.Address.CountyOrParish', axis=1)


    # %% [markdown]
    # CHUNGAS BORRAR (TEMPORAL)

    # %%
    # DROP  
    # columnes_categoriques = columnes_categoriques.drop('UnitTypes.UnitTypeType', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('Structure.ParkingFeatures', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('Structure.Heating', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('Structure.Cooling', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('Structure.Basement', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('ImageData.room_type_reso.results', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('ImageData.features_reso.results', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('Characteristics.LotFeatures', axis=1)


    # %% [markdown]
    # Raras borrar (temporal)

    # %%
    # Drop all census
    columnes_categoriques = columnes_categoriques.drop('Location.Address.CensusBlock', axis=1)
    columnes_categoriques = columnes_categoriques.drop('Location.Address.CensusTract', axis=1)

    # drop Listing.Date.CloseDate
    columnes_categoriques = columnes_categoriques.drop('Listing.Dates.CloseDate', axis=1)

    # %%
    columnes_categoriques

    # %% [markdown]
    # Chungas start

    # %%
    columnes_categoriques

    # %%


    columnes_categoriques2 = columnes_categoriques.copy()

    # Optimized processing for "chunga" columns
    chunga_columns = [
        'UnitTypes.UnitTypeType',
        'Structure.ParkingFeatures',
        'Structure.Heating',
        'Structure.Cooling',
        'Structure.Basement',
        'ImageData.room_type_reso.results',
        'ImageData.features_reso.results',
        'Characteristics.LotFeatures'
        'Listing.Dates.CloseDate',
    ]

    # Step 1: Process "chunga" columns
    for columna in columnes_categoriques.columns:
        if columna in chunga_columns:
            if(columna == 'Listing.Dates.CloseDate'):
                # convert dates to months
                columnes_categoriques[columna] = pd.to_datetime(columnes_categoriques[columna]).dt.month
            # Safely parse and explode the column
            columnes_categoriques[columna] = columnes_categoriques[columna].map(safe_eval)
            data_exploded = columnes_categoriques[columna].explode()
            
            # Clean and create dummies
            data_exploded = cleanColumn(data_exploded)
            dummies = pd.get_dummies(data_exploded, prefix=columna, prefix_sep='=')

            # Aggregate dummies back to the original DataFrame
            dummies = dummies.groupby(level=0).sum()

            # Add dummies to the main DataFrame and drop the original column
            columnes_categoriques = pd.concat([columnes_categoriques, dummies], axis=1)
            columnes_categoriques.drop(columns=[columna], inplace=True)

        else:
            # Process non-"chunga" columns normally
            columnes_categoriques[columna] = cleanColumn(columnes_categoriques[columna])
            dummies = pd.get_dummies(columnes_categoriques[columna], drop_first=True)
            columnes_categoriques = pd.concat([columnes_categoriques, dummies], axis=1)
            columnes_categoriques.drop(columns=[columna], inplace=True)

        print(f"Processed column: {columna}")

    # %%



    # %%
    # for every column see how many unique values it has and its count
    for col in columnes_categoriques.columns:
        print(columnes_categoriques[col].value_counts())
        print()

    # %%
    # add ListingId to the categorical columns
    columnes_categoriques = pd.concat([data['Listing.ListingId'], columnes_categoriques], axis=1)

    # %%
    # natural join of the two dataframes
    data_final = pd.merge(columnes_numeriques, columnes_categoriques, on='Listing.ListingId')
    data_final = data_final.drop('Listing.ListingId', axis=1)

    # %%
    data_final.to_csv(file_name, index=False)

def mastegar_test(data, file_name):
        # print(data['ImageData.style.stories.summary.label'].unique())
    data['ImageData.style.stories.summary.label'] = data['ImageData.style.stories.summary.label'].map(story_mapping)
    print(data['ImageData.style.stories.summary.label'].unique())

    # %%
    data['Structure.YearBuilt'].unique()

    # %%
    # # replace edge case 
    # data['Structure.YearBuilt'] = data['Structure.YearBuilt'].replace(190., np.nan)

    # # convert 0 to nan on Structure.YearBuilt to remove 0 values
    # data['Structure.YearBuilt'] = data['Structure.YearBuilt'].replace(0, np.nan)


    # %%
    #data segmentation
    columnes_numeriques = data.select_dtypes(include=['number'])  # Selecciona columnes numèriques
    # add ListingId to the numeric columns
    columnes_numeriques = pd.concat([data['Listing.ListingId'], columnes_numeriques], axis=1)

    columnes_categoriques = data.select_dtypes(exclude=['number'])  # Selecciona columnes no numèriques (categòriques)

    # %%
    # canviar els NaN per la mitjana de la columna
    columnes_numeriques = columnes_numeriques.apply(lambda col: col.fillna(col.mean(skipna=True)) if col.dtype in ['float64', 'int64'] else col)
    columnes_numeriques

    # %% [markdown]
    # INUTILS o REDUNDANTS -> BORRAR

    # %%
    # some fine tuning
    # drop columns with too many unique values
    # drop Listing.ListingId
    # columnes_categoriques = columnes_categoriques.drop('Listing.ListingId', axis=1)

    # drop postalcodeplus4
    columnes_categoriques = columnes_categoriques.drop('Location.Address.PostalCodePlus4', axis=1)

    # drop location number Location.Address.StreetNumber
    # numero independent del preu
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StreetNumber', axis=1)

    # DROP Location.Address.StateOrProvince
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StateOrProvince', axis=1)

    # DROP Location.Address.UnparsedAddress
    columnes_categoriques = columnes_categoriques.drop('Location.Address.UnparsedAddress', axis=1)

    # DROP Location.Address.StreetDirectionSuffix
    # nombre d'ocurrencies no es prou gran per cada categoria
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StreetDirectionSuffix', axis=1)

    # DROP UnitNumber
    # nombre d'ocurrencies no es prou gran per cada categoria
    columnes_categoriques = columnes_categoriques.drop('Location.Address.UnitNumber', axis=1)

    # DROP Location.Address.StreetSuffix
    # no es rellevant
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StreetSuffix', axis=1)

    #drop Location.Address.StreetDirectionPrefix
    # no es rellevant
    columnes_categoriques = columnes_categoriques.drop('Location.Address.StreetDirectionPrefix', axis=1)

    # DROP Location.Area.SubdivisionName
    # no es rellevant
    columnes_categoriques = columnes_categoriques.drop('Location.Area.SubdivisionName', axis=1)

    # DROP Location.School.HighSchoolDistrict
    # no es rellevant
    columnes_categoriques = columnes_categoriques.drop('Location.School.HighSchoolDistrict', axis=1)

    #DRop postalcode
    # no es rellevant
    columnes_categoriques = columnes_categoriques.drop('Location.Address.PostalCode', axis=1)

    columnes_categoriques = columnes_categoriques.drop('Location.Address.City', axis=1)
    columnes_categoriques = columnes_categoriques.drop('Location.Address.CountyOrParish', axis=1)


    # %% [markdown]
    # CHUNGAS BORRAR (TEMPORAL)

    # %%
    # DROP  
    # columnes_categoriques = columnes_categoriques.drop('UnitTypes.UnitTypeType', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('Structure.ParkingFeatures', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('Structure.Heating', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('Structure.Cooling', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('Structure.Basement', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('ImageData.room_type_reso.results', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('ImageData.features_reso.results', axis=1)
    # columnes_categoriques = columnes_categoriques.drop('Characteristics.LotFeatures', axis=1)


    # %% [markdown]
    # Raras borrar (temporal)

    # %%
    # Drop all census
    columnes_categoriques = columnes_categoriques.drop('Location.Address.CensusBlock', axis=1)
    columnes_categoriques = columnes_categoriques.drop('Location.Address.CensusTract', axis=1)

    # drop Listing.Date.CloseDate
    columnes_categoriques = columnes_categoriques.drop('Listing.Dates.CloseDate', axis=1)

    # %%
    columnes_categoriques

    # %% [markdown]
    # Chungas start

    # %%
    columnes_categoriques

    # %%


    columnes_categoriques2 = columnes_categoriques.copy()

    # Optimized processing for "chunga" columns
    chunga_columns = [
        'UnitTypes.UnitTypeType',
        'Structure.ParkingFeatures',
        'Structure.Heating',
        'Structure.Cooling',
        'Structure.Basement',
        'ImageData.room_type_reso.results',
        'ImageData.features_reso.results',
        'Characteristics.LotFeatures',
        'Listing.Dates.CloseDate'
    ]

    # Step 1: Process "chunga" columns
    for columna in columnes_categoriques.columns:
        if columna in chunga_columns:
            if(columna == 'Listing.Dates.CloseDate'):
                # convert dates to months
                columnes_categoriques[columna] = pd.to_datetime(columnes_categoriques[columna]).dt.month
            # Safely parse and explode the column
            columnes_categoriques[columna] = columnes_categoriques[columna].map(safe_eval)
            data_exploded = columnes_categoriques[columna].explode()
            
            # Clean and create dummies
            data_exploded = cleanColumn(data_exploded)
            dummies = pd.get_dummies(data_exploded, prefix=columna, prefix_sep='=')

            # Aggregate dummies back to the original DataFrame
            dummies = dummies.groupby(level=0).sum()

            # Add dummies to the main DataFrame and drop the original column
            columnes_categoriques = pd.concat([columnes_categoriques, dummies], axis=1)
            columnes_categoriques.drop(columns=[columna], inplace=True)

        else:
            # Process non-"chunga" columns normally
            if (columna == 'Listing.ListingId'): continue

            columnes_categoriques[columna] = cleanColumn(columnes_categoriques[columna])
            dummies = pd.get_dummies(columnes_categoriques[columna], drop_first=True)
            columnes_categoriques = pd.concat([columnes_categoriques, dummies], axis=1)
            columnes_categoriques.drop(columns=[columna], inplace=True)

        print(f"Processed column: {columna}")

    # %%



    # %%
    # for every column see how many unique values it has and its count
    for col in columnes_categoriques.columns:
        print(columnes_categoriques[col].value_counts())
        print()

    # %%
    # natural join of the two dataframes
    data_final = pd.merge(columnes_numeriques, columnes_categoriques, on='Listing.ListingId')

    data_final

    # %%
    data_final.to_csv(file_name, index=False)
# %%
# Load the data
rawdata = pd.read_csv("train.csv", low_memory=False)
rawdata.drop_duplicates() # remove duplicates
mastegar(rawdata, 'train_final.csv')

rawdata = pd.read_csv("test.csv", low_memory=False)
rawdata.drop_duplicates() # remove duplicates
mastegar_test(rawdata, 'test_final.csv')