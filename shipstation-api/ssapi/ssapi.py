'''
Created on Jan 30, 2015

@author: grovesr
'''

import requests
from requests.auth import HTTPBasicAuth

# Create your models here.
class ss(object):
    """
    abstract class that facilitates ShipStation API calls
    """
    API_KEY=''
    API_SECRET=''
    API_BASE_URL='https://ssapi.ssapi.com/'
    response=requests.Response()
    query=requests.Request()
    status_code=0
    
    def __init__(self,api_key='',api_secret='',api_base_url=API_BASE_URL):
        self.API_KEY=api_key
        self.API_SECRET=api_secret
        self.API_BASE_URL=api_base_url
    
    def __unicode__(self):
        return 'ss object:'+self.query()
    
    def json(self):
        """
        return the json data encoded in the response
        """
        return self.response.json()
    
    def query(self):
        if self.response.url:
            return self.response.url
        else:
            return ''
    
    def headers(self):
        """
        return a list of keys that can be used to access data in the json result
        """
        if self.response.status_code == None:
            return[]
        data=self.json()
        headerList={}
        if isinstance(data,dict):
            #turn a single response into a single element list
            data=[data]
        for item in data:
            for key,value in item.iteritems():
                keysList=self.get_header_key(key,value)
                for thisKey in keysList:
                    headerList[thisKey]=None
        return headerList.keys()
    
    def get_header_key(self,key,value):
        """
        recursively dive into each value until it only contains a single object
        """
        headerKey={}
        if isinstance(value,list):
            # this key holds a list of items, just look at the first list item
            if len(value) == 0:
                return []
            headerItems=self.get_header_key(key,value[0])
            for thisItem in headerItems:
                headerKey[thisItem]=None
            return headerKey.keys()
        if isinstance(value,dict):
            # this key holds a dictionary
            for subkey,subvalue in value.iteritems():
                headerItems=self.get_header_key(subkey,subvalue)
                for thisItem in headerItems:
                    headerKey[key+'_'+thisItem]=None
            return headerKey.keys()
        return [key]
    
class get(ss):
    """
    Class to implement ShipStation API GET requests
    """
    
    def __unicode__(self):
        return 'ss.get object:'+self.query()
    
    def __str__(self):
        return self.__unicode__()
    
    def orders(self,**kwargs):
        """
        ShipStation GET orders API
        kwargs holds the filter criteria
        customerName={customerName}
        itemKeyword={itemKeyword}
        modifyDateStart={modifyDateStart}
        modifyDateEnd={modifyDateEnd}
        orderDateStart={orderDateStart}
        orderDateEnd={orderDateEnd}
        orderNumber={orderNumber}
        orderStatus={orderStatus}
        paymentDateStart={paymentDateStart}
        paymentDateEnd={paymentDateEnd}
        storeId={storeId}
        page={page}
        pageSize={pageSize}
        """
        reqUrl=self.API_BASE_URL+'orders'
        filterCriteria='?'
        for filterName,filterValue in kwargs.iteritems():
            filterCriteria+=filterName+'='+str(filterValue)+'&'
        reqUrl+=filterCriteria[:-1]
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200:
            return 'Error: status_code '+str(resp.status_code)+" invalid filter criteria "
        self.response=resp
        return ''
    
    def orders_orderId(self,orderId):
        """
        ShipStation orders/orderId API
        """
        reqUrl=self.API_BASE_URL+'orders/'+str(orderId)
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200:
            return 'Error: status_code '+str(resp.status_code)+" invalid order number"
        self.response=resp
        return ''
    
    def warehouses(self):
        """
        ShipStation GET warehouses API
        """
        reqUrl=self.API_BASE_URL+'warehouses'
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200:
            return 'Error: status_code '+str(resp.status_code)+" invalid filter criteria "
        self.response=resp
        return ''
    
    def warehouses_warehousId(self,warehouseId):
        """
        ShipStation warehouse API
        """
        reqUrl=self.API_BASE_URL+'warehouses/'+str(warehouseId) 
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200:
            return 'Error: status_code '+str(resp.status_code)+" invalid filter criteria "
        self.response=resp
        return ''
    
    def customers(self,**kwargs):
        """
        ShipStation GET customers API
        stateCode=stateCode
        countryCode=countryCode
        tagId=tagId
        marketplaceId=marketplaceId
        page=page
        pageSize=pageSize
        """
        reqUrl=self.API_BASE_URL+'customers'
        filterCriteria='?'
        for filterName,filterValue in kwargs.iteritems():
            filterCriteria+=filterName+'='+str(filterValue)+'&'
        reqUrl+=filterCriteria[:-1]
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200:
            return 'Error: status_code '+str(resp.status_code)+" invalid filter criteria "
        self.response=resp
        return ''

    def customers_customerId(self,customerId):
        """
        ShipStation customers/customerId API
        """
        reqUrl=self.API_BASE_URL+'customers/'+str(customerId) 
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200:
            return 'Error: status_code '+str(resp.status_code)+" invalid filter criteria "
        self.response=resp
        return ''
    
    def accounts_listtags(self):
        """
        ShipStation accounts/listtags API
        """
        reqUrl=self.API_BASE_URL+'accounts/listtags' 
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200:
            return 'Error: status_code '+str(resp.status_code)+" invalid filter criteria "
        self.response=resp
        return ''
    
    def shipments(self,**kwargs):
        """
        ShipStation GET shipments API
        recipientName={recipientName}
        recipientCountryCode={recipientCountryCode}
        orderNumber={orderNumber}
        orderId={orderId}
        carrierCode={carrierCode}
        serviceCode={serviceCode}
        trackingNumber={trackingNumber}
        shipDateStart={shipDateStart}
        shipDateEnd={shipDateEnd}
        voidDateStart={voidDateStart}
        voidDateEnd={voidDateEnd}
        includeShipmentItems={includeShipmentItems}
        page={page}
        pageSize={pageSize}
        """
        reqUrl=self.API_BASE_URL+'shipments'
        filterCriteria='?'
        for filterName,filterValue in kwargs.iteritems():
            filterCriteria+=filterName+'='+str(filterValue)+'&'
        reqUrl+=filterCriteria[:-1]
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200:
            return 'Error: status_code '+str(resp.status_code)+" invalid filter criteria "
        self.response=resp
        return ''
    
    def stores(self):
        """
        ShipStation GET stores API
        """
        reqUrl=self.API_BASE_URL+'stores'
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200:
            return 'Error: status_code '+str(resp.status_code)+" invalid filter criteria "
        self.response=resp
        return ''
    
    def stores_storeId(self,storeId):
        """
        ShipStation warehouse API
        """
        reqUrl=self.API_BASE_URL+'stores/'+str(storeId) 
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200:
            return 'Error: status_code '+str(resp.status_code)+" invalid filter criteria "
        self.response=resp
        return ''