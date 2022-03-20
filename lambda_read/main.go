package main

import (
	"context"
	"errors"

	"github.com/aws/aws-lambda-go/events"
	runtime "github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/lambda"
)

var client = lambda.New(session.New())

var sess = session.Must(session.NewSessionWithOptions(session.Options{
	SharedConfigState: session.SharedConfigEnable,
}))

var svc = NewDynamoRepository(sess)

var cryp, err = NewShaEncrypter()

func handleRequest(ctx context.Context, event events.APIGatewayProxyRequest) (string, error) {

	if err != nil {
		return "", err
	}

	id := event.PathParameters["uuid"]

	password, views, err := svc.Get(id)

	if err != nil {
		return "", err
	}

	if views <= 0 {
		return "", errors.New("No password found")
	}

	views = views - 1

	defer svc.UpdateView(id, views)

	if views == 0 {
		svc.Remove(id)
	}

	decryptedPassword, err := cryp.Decrypt(password)

	if err != nil {
		return "", err
	}

	return decryptedPassword, err

}

func main() {
	runtime.Start(handleRequest)
}
