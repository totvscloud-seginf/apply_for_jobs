package main

import (
	"os"
	"strconv"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
)

func NewDynamoRepository(session *session.Session) Repository {

	return dynamoRepository{
		dynamodb.New(session),
	}
}

type dynamoRepository struct {
	svc *dynamodb.DynamoDB
}

func (d dynamoRepository) Get(id string) (string, int, error) {
	result, err := d.svc.GetItem(&dynamodb.GetItemInput{
		TableName: aws.String(os.Getenv("TABLE_NAME")),
		Key: map[string]*dynamodb.AttributeValue{
			"uuid": {
				N: aws.String(id),
			},
		},
	})

	if err != nil {
		return "", 0, err
	}

	viewsData := result.Item["views"].N

	views, err := strconv.Atoi(*viewsData)

	if err != nil {
		return "", 0, err
	}

	return *result.Item["password"].N, views, nil
}

func (d dynamoRepository) Remove(id string) error {
	_, err := d.svc.DeleteItem(&dynamodb.DeleteItemInput{
		TableName: aws.String(os.Getenv("TABLE_NAME")),
		Key: map[string]*dynamodb.AttributeValue{
			"uuid": {
				N: aws.String(id),
			},
		},
	})

	return err
}

func (d dynamoRepository) UpdateView(id string, views int) error {
	_, err := d.svc.UpdateItem(&dynamodb.UpdateItemInput{
		TableName: aws.String(os.Getenv("TABLE_NAME")),
		Key: map[string]*dynamodb.AttributeValue{
			"uuid": {
				N: aws.String(id),
			},
		},
		UpdateExpression: aws.String("SET views = :v"),
		ExpressionAttributeValues: map[string]*dynamodb.AttributeValue{
			":v": {
				N: aws.String(strconv.Itoa(views)),
			},
		},
	})

	return err
}
