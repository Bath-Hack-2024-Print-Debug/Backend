import pandas as pd
import zoopla as zoopla

def getPropertiesArea():
    propertyIds = pd.read_csv('bath_ids.csv')
    propertyDetails = pd.DataFrame(
                    columns=['id','url','propertyType','name','publishedOn',
                            'uuid','postalCode','description','address',
                            'listingCondition','listingStatus','latitude',
                            'longitude','category','price',
                            'priceActual','priceMax','priceMin','sqft',
                            'councilTaxBand','floorArea','livingRooms',
                            'beds','bedsMax','bedsMin','baths',
                            'isRetirementHome','isSharedOwnership',
                            'studentFriendly','images','features','additionalLinks',
                            'floorPlan','agentAddress','agentName','agentPhone',
                            'availableFrom'])
    propertyDetails = propertyDetails.set_index('id', inplace=True)

    for id in propertyIds['id']:
        temp = zoopla.getPropertyDetails(id)
        propertyDetails = pd.concat([propertyDetails,pd.DataFrame([temp])], ignore_index=True)

    propertyDetails.to_csv('bath_property_details.csv')

propertyDetails = pd.read_csv('bath_property_details.csv')
propertyDetails = propertyDetails.set_index('id', inplace=False)
#fill in propertyType NaN values with terraced
propertyDetails['propertyType'].fillna('terraced', inplace=True)

#drop all columns with nan values
propertyDetails.drop(columns=['sqft', 'baths', 'agentPhone', 'availableFrom', 'floorArea'], inplace=True)

#drop columns not needed for regressing the rent price
propertyDetails.drop(columns=['uuid','postalCode','listingCondition',
                              'listingStatus','category','images',
                              'additionalLinks','floorPlan','agentAddress',
                              'agentName'], inplace=True)
propertyDetails.to_csv('bath_ml.csv')
print("run")