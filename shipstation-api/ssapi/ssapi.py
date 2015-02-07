'''
Created on Jan 30, 2015

@author: grovesr
'''

import requests
from requests.auth import HTTPBasicAuth

# Create your models here.
class ssapi(object):
    """
    abstract class that facilitates ShipStation API calls
    """
    API_KEY=''
    API_SECRET=''
    API_ENDPOINT='https://ssapi.shipstation.com/'
    response=requests.Response()
    query=requests.Request()
    status_msg={}
    status_msg[200]='OK - The request was successful (some API calls may return 201 instead).'
    status_msg[201]='Created - The request was successful and a resource was created.'
    status_msg[204]='No Content - The request was successful but there is no representation to return (that is, the response is empty).'
    status_msg[400]='Bad Request - The request could not be understood or was missing required parameters.'
    status_msg[401]='Unauthorized - Authentication failed or user does not have permissions for the requested operation.'
    status_msg[403]='Forbidden - Access denied.'
    status_msg[404]='Not Found - Resource was not found.'
    status_msg[405]='Method Not Allowed - Requested method is not supported for the specified resource.'
    status_msg[429]='Too Many Requests - Exceeded ShipStation API limits. When the limit is reached, your application should stop making requests until X-Rate-Limit-Reset seconds have elapsed.'
    status_msg[500]='Internal Server Error - ShipStation has encountered an error.'
    
    def __init__(self,api_key='',api_secret='',api_endpoint=API_ENDPOINT):
        self.API_KEY=api_key
        self.API_SECRET=api_secret
        self.API_ENDPOINT=api_endpoint
    
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
    
class get(ssapi):
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
        Args:
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
        reqUrl=self.API_ENDPOINT+'orders'
        filterCriteria='?'
        for filterName,filterValue in kwargs.iteritems():
            filterCriteria+=filterName+'='+str(filterValue)+'&'
        reqUrl+=filterCriteria[:-1]
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200 and resp.status_code != 201:
            return 'Shipstation API error: '+str(resp.status_code)+' '+resp.status_msg[resp.status_code]
        self.response=resp
        return ''
    
    def orders_orderId(self,orderId):
        """
        ShipStation orders/orderId API
        Arg:
            orderId
        """
        reqUrl=self.API_ENDPOINT+'orders/'+str(orderId)
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200 and resp.status_code != 201:
            return 'Shipstation API error: '+str(resp.status_code)+' '+self.status_msg[resp.status_code]
        self.response=resp
        return ''
    
    def warehouses(self):
        """
        ShipStation GET warehouses API
        """
        reqUrl=self.API_ENDPOINT+'warehouses'
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200 and resp.status_code != 201:
            return 'Shipstation API error: '+str(resp.status_code)+' '+self.status_msg[resp.status_code]
        self.response=resp
        return ''
    
    def warehouses_warehousId(self,warehouseId):
        """
        ShipStation warehouse API
        Arg:
            warehouseId
        """
        reqUrl=self.API_ENDPOINT+'warehouses/'+str(warehouseId) 
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200 and resp.status_code != 201:
            return 'Shipstation API error: '+str(resp.status_code)+' '+self.status_msg[resp.status_code]
        self.response=resp
        return ''
    
    def customers(self,**kwargs):
        """
        ShipStation GET customers API
        Args:
            stateCode=stateCode
            countryCode=countryCode
            tagId=tagId
            marketplaceId=marketplaceId
            page=page
            pageSize=pageSize
        """
        reqUrl=self.API_ENDPOINT+'customers'
        filterCriteria='?'
        for filterName,filterValue in kwargs.iteritems():
            filterCriteria+=filterName+'='+str(filterValue)+'&'
        reqUrl+=filterCriteria[:-1]
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200 and resp.status_code != 201:
            return 'Shipstation API error: '+str(resp.status_code)+' '+self.status_msg[resp.status_code]
        self.response=resp
        return ''

    def customers_customerId(self,customerId):
        """
        ShipStation customers/customerId API
        Arg:
            customerId
        """
        reqUrl=self.API_ENDPOINT+'customers/'+str(customerId) 
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200 and resp.status_code != 201:
            return 'Shipstation API error: '+str(resp.status_code)+' '+self.status_msg[resp.status_code]
        self.response=resp
        return ''
    
    def accounts_listtags(self):
        """
        ShipStation accounts/listtags API
        """
        reqUrl=self.API_ENDPOINT+'accounts/listtags' 
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200 and resp.status_code != 201:
            return 'Shipstation API error: '+str(resp.status_code)+' '+self.status_msg[resp.status_code]
        self.response=resp
        return ''
    
    def shipments(self,**kwargs):
        """
        ShipStation GET shipments API
        Args:
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
        reqUrl=self.API_ENDPOINT+'shipments'
        filterCriteria='?'
        for filterName,filterValue in kwargs.iteritems():
            filterCriteria+=filterName+'='+str(filterValue)+'&'
        reqUrl+=filterCriteria[:-1]
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200 and resp.status_code != 201:
            return 'Shipstation API error: '+str(resp.status_code)+' '+self.status_msg[resp.status_code]
        self.response=resp
        return ''
    
    def stores(self):
        """
        ShipStation GET stores API
        """
        reqUrl=self.API_ENDPOINT+'stores'
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            print e
            return e.message
        if resp.status_code != 200 and resp.status_code != 201:
            return 'Shipstation API error: '+str(resp.status_code)+' '+self.status_msg[resp.status_code]
        self.response=resp
        return ''
    
    def stores_storeId(self,storeId):
        """
        ShipStation warehouse API
        Arg:
            storeId
        """
        reqUrl=self.API_ENDPOINT+'stores/'+str(storeId) 
        try:
            resp=requests.get(reqUrl,auth=HTTPBasicAuth(self.API_KEY,self.API_SECRET))
        except Exception as e:
            return e.message
        if resp.status_code != 200 and resp.status_code != 201:
            return 'Shipstation API error: '+str(resp.status_code)+' '+self.status_msg[resp.status_code]
        self.response=resp
        return ''
    