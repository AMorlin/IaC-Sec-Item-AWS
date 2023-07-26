from pprint import pprint
import boto3 
import json
import logging

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    global dynamodb

    body = ""
    statusCode = 200
    
    if 'httpMethod' in event and 'resource' in event:
        rota = str(event['httpMethod']) + ' ' + str(event['resource'])
    else:
        statusCode = 400
        body = "Esta função Lambda deverá ser chamada via Proxy pelo API Gateway"
        return {
            'statusCode': statusCode,
            'body': body
        }      
    
    if rota == "PUT /item":

        if 'body' in event:
            
            #Transforma objeto em Json Sting
            jsonAjustado = json.dumps(event['body'])
            
            #Transforma Json String em Objeto Python com scapes
            jsonPut = json.loads(jsonAjustado)
            
            #Transforma objeto com scapes em objeto Python correto 
            jsonPut = json.loads(jsonPut)
            
            
            table = dynamodb.Table("IACSecItems")
            table.put_item(
                Item={
                    'id': jsonPut['id'],
                    'price': jsonPut['price']})
                    
            body = 'Put Item ' + jsonPut['id']
        else:
            statusCode = 500
            body = 'PUT sem objeto body'
            return {
                'statusCode': statusCode,
                'body': body
            }
        

    return {
        'statusCode': statusCode,
        'body': body
        }